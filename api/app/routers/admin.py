from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends

from app.database import get_db
from app.dependencies import require_admin
from app.models.booking import BookingStatus

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard")
async def dashboard(_admin: dict = Depends(require_admin)):
    db = get_db()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Today's bookings
    today_bookings = await db.bookings.count_documents({"date": today})

    # Upcoming confirmed bookings
    upcoming = await db.bookings.count_documents(
        {"date": {"$gte": today}, "status": BookingStatus.CONFIRMED}
    )

    # Total revenue (captured payments)
    pipeline = [
        {"$match": {"status": "captured"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount_inr"}}},
    ]
    revenue_result = await db.payments.aggregate(pipeline).to_list(1)
    total_revenue = revenue_result[0]["total"] if revenue_result else 0

    # Total bookings by status
    status_pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
    ]
    status_counts = {}
    async for doc in db.bookings.aggregate(status_pipeline):
        status_counts[doc["_id"]] = doc["count"]

    # Recent bookings
    recent_cursor = db.bookings.find().sort("created_at", -1).limit(10)
    recent_bookings = []
    async for doc in recent_cursor:
        recent_bookings.append(
            {
                "id": str(doc["_id"]),
                "user_name": doc["user_name"],
                "service_title": doc["service_title"],
                "date": doc["date"],
                "time_slot": doc["time_slot"],
                "status": doc["status"],
                "price_inr": doc["price_inr"],
            }
        )

    return {
        "today_bookings": today_bookings,
        "upcoming_bookings": upcoming,
        "total_revenue": total_revenue,
        "bookings_by_status": status_counts,
        "recent_bookings": recent_bookings,
    }


@router.get("/stats")
async def stats(_admin: dict = Depends(require_admin)):
    db = get_db()

    total_users = await db.users.count_documents({})
    total_bookings = await db.bookings.count_documents({})
    total_payments = await db.payments.count_documents({"status": "captured"})

    # Revenue by service
    service_pipeline = [
        {"$match": {"status": {"$in": ["confirmed", "completed"]}}},
        {
            "$group": {
                "_id": "$service_title",
                "count": {"$sum": 1},
                "revenue": {"$sum": "$price_inr"},
            }
        },
        {"$sort": {"revenue": -1}},
    ]
    services = []
    async for doc in db.bookings.aggregate(service_pipeline):
        services.append(
            {
                "service": doc["_id"],
                "bookings": doc["count"],
                "revenue": doc["revenue"],
            }
        )

    # Daily bookings for last 30 days
    today = datetime.now(timezone.utc)
    thirty_days_ago = (today - timedelta(days=29)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    daily_pipeline = [
        {"$match": {"date": {"$gte": thirty_days_ago, "$lte": today_str}}},
        {"$group": {"_id": "$date", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    daily_bookings: dict[str, int] = {}
    async for doc in db.bookings.aggregate(daily_pipeline):
        daily_bookings[doc["_id"]] = doc["count"]

    # Fill in missing days with 0
    daily_series = []
    for i in range(30):
        d = (today - timedelta(days=29 - i)).strftime("%Y-%m-%d")
        daily_series.append({"date": d, "bookings": daily_bookings.get(d, 0)})

    # Daily revenue for last 30 days
    daily_rev_pipeline = [
        {
            "$match": {
                "status": "captured",
                "created_at": {
                    "$gte": today - timedelta(days=29),
                },
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}
                },
                "revenue": {"$sum": "$amount_inr"},
            }
        },
        {"$sort": {"_id": 1}},
    ]
    daily_revenue: dict[str, int] = {}
    async for doc in db.payments.aggregate(daily_rev_pipeline):
        daily_revenue[doc["_id"]] = doc["revenue"]

    revenue_series = []
    for i in range(30):
        d = (today - timedelta(days=29 - i)).strftime("%Y-%m-%d")
        revenue_series.append({"date": d, "revenue": daily_revenue.get(d, 0)})

    return {
        "total_users": total_users,
        "total_bookings": total_bookings,
        "total_payments": total_payments,
        "revenue_by_service": services,
        "daily_bookings": daily_series,
        "daily_revenue": revenue_series,
    }
