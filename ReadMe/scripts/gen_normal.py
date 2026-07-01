"""Normal-people control databank — computed identically to the celebrities so the
famous-vs-normal comparison is apples-to-apples. Append new people to NORMAL."""
import json
import re

from app.services.kundli_calculator._core import (get_julian_day, calc_planet_positions, SIGN_NAMES)
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.nakshatra import calc_nakshatra
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

# name, sex, date, time(24h), place, lat, lon
NORMAL = [
    ("Rama G Dave", "Female", "1941-06-26", "11:30", "Bagar, Rajasthan, India", 28.1833, 75.5),
    ("Tushar G Dave", "Male", "1961-09-15", "16:30", "Jhunjhunu, Rajasthan, India", 28.1167, 75.3833),
    ("Heena T Dave", "Female", "1962-09-24", "22:30", "Kodinar, Gujarat, India", 20.7833, 70.7),
    ("Pratiksha", "Female", "1988-07-28", "11:30", "Amdapur, Maharashtra, India", 20.3833, 76.4167),
    ("Harshal Joshi", "Male", "1988-12-25", "19:55", "Mumbai, Maharashtra, India", 19.0667, 72.8667),
    ("Papu ben", "Female", "1972-06-16", "13:28", "Rishra, West Bengal, India", 22.7, 88.3333),
    ("Sonali Pagar", "Female", "1988-05-14", "12:40", "Malegaon, Maharashtra, India", 20.55, 74.5167),
    ("Rohan", "Male", "1985-12-23", "15:45", "Mumbai, Maharashtra, India", 19.0667, 72.8667),
    ("Prasad", "Male", "1987-03-17", "12:12", "Ahmednagar, Maharashtra, India", 19.3833, 74.65),
    ("Praveen", "Male", "1985-09-19", "14:10", "Radhanagari, Maharashtra, India", 16.3833, 74.0),
    ("Snehal J Chauhan", "Female", "1985-04-12", "22:10", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Sanjay M Raval", "Male", "1995-12-26", "18:12", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Bhargav M Raval", "Male", "1997-07-18", "08:42", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Harshad Patel", "Male", "1983-07-12", "14:30", "Mehsana, Gujarat, India", 23.5833, 72.3667),
    ("Mayank Kumar", "Male", "1979-10-14", "15:45", "Chandigarh, India", 30.7333, 76.7833),
    ("Bhargav", "Male", "1987-02-24", "20:20", "Bhavnagar, Gujarat, India", 21.7667, 72.15),
    ("Yatin Mirani", "Male", "1990-07-06", "04:20", "Bavla, Gujarat, India", 22.8333, 72.35),
    ("Priyal Parikh", "Male", "1991-05-24", "09:41", "Vadodara, Gujarat, India", 22.3, 73.2),
    ("Darshan", "Male", "1989-06-27", "21:34", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Varun Chaturvedi", "Male", "1984-11-12", "20:05", "Gorakhpur, Uttar Pradesh, India", 26.75, 83.3667),
    ("Riddhish Shah", "Male", "1988-02-09", "11:20", "Anand, Gujarat, India", 22.5667, 72.9167),
    ("Yaduvendra Chaurasia", "Male", "1997-05-23", "18:20", "Umaria, Madhya Pradesh, India", 23.8, 80.9167),
    ("Rupal Raghuvanshi", "Female", "1998-09-25", "11:30", "Dewas, Madhya Pradesh, India", 22.9667, 76.0667),
    ("Harsh Trivedi", "Male", "1992-05-03", "02:15", "Surendranagar, Gujarat, India", 22.6833, 71.6667),
    ("Aastha Sachin Raval", "Female", "1993-01-05", "03:05", "Dundlod, Rajasthan, India", 27.9167, 75.25),
    ("Ruchi Raval", "Female", "1989-10-03", "10:42", "Kota, Rajasthan, India", 25.2667, 77.3667),
    ("Shikha Kumari", "Female", "1987-04-05", "15:28", "Hajipur, Bihar, India", 25.6667, 85.2167),
    ("Bhupesh Kumar", "Male", "1982-10-23", "06:10", "Begusarai, Bihar, India", 25.4167, 86.1167),
    ("Dhruv Jani", "Male", "1987-11-24", "07:55", "Kodinar, Gujarat, India", 20.7833, 70.7),
    ("Jigisha Dhruv Jani", "Female", "1993-06-08", "11:35", "Amreli, Gujarat, India", 21.6167, 71.2167),
    ("Suraj Mehta", "Male", "1995-02-26", "09:35", "Hansi, Haryana, India", 29.1, 75.9667),
    ("Neha Khetrapal", "Female", "1990-12-25", "14:45", "Hansi, Haryana, India", 29.1, 75.9667),
    ("Vishal Khetrapal", "Male", "1984-06-21", "07:30", "Hansi, Haryana, India", 29.1, 75.9667),
    ("Rumna Saha", "Female", "1989-02-07", "10:00", "Durgapur, West Bengal, India", 25.5167, 88.1167),
    ("Partha Saha", "Male", "1985-04-23", "18:35", "Bardhaman, West Bengal, India", 23.45, 87.6167),
    ("Melvin Methew", "Male", "1991-08-11", "05:30", "Kollam, Kerala, India", 8.8667, 76.5833),
    ("Bishal Bose", "Male", "1985-09-17", "00:10", "Kolkata, West Bengal, India", 22.5667, 88.3667),
    ("Manish Singh", "Male", "1993-06-08", "23:00", "Jamshedpur, Jharkhand, India", 22.8, 86.1667),
    ("Venkat", "Male", "1990-10-19", "23:58", "Chennai, Tamil Nadu, India", 13.0833, 80.2667),
    ("Bhusan Savani", "Male", "1982-11-08", "12:02", "Amravati, Maharashtra, India", 20.9167, 77.75),
    ("Grandin Major Vincent", "Male", "1993-01-09", "01:45", "Tambaram, Tamil Nadu, India", 12.9167, 80.1167),
    ("Kaumil Bhavsar", "Male", "1988-07-13", "12:00", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Hardik Suchak", "Male", "1988-02-02", "19:30", "Savar Kundla, Gujarat, India", 21.3167, 71.3167),
    ("Yatin Punjabi", "Male", "1987-09-29", "05:42", "Nadiad, Gujarat, India", 22.6833, 72.8667),
    ("Janki Dave", "Female", "1987-04-21", "17:30", "Dwarka, Gujarat, India", 22.2333, 68.9667),
    ("Rahul R Joshi", "Male", "1991-10-10", "15:00", "Gandhinagar, Gujarat, India", 23.2167, 72.6667),
    ("Shikha Dave", "Female", "1992-08-16", "07:00", "Veraval, Gujarat, India", 20.8833, 70.3667),
    ("Riya Viraj Shah", "Female", "1997-02-01", "17:35", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Viraj Shah", "Male", "1996-08-09", "01:11", "Bharuch, Gujarat, India", 21.7, 72.9667),
    ("Varta Shah", "Female", "1989-03-16", "13:00", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Devang Shah", "Male", "1988-08-02", "12:51", "Ahmedabad, Gujarat, India", 23.0667, 72.6333),
    ("Nishit Parikh", "Male", "1985-03-12", "15:45", "Morbi, Gujarat, India", 22.8167, 70.8167),
    ("Arohi N Parikh", "Female", "1985-05-19", "19:00", "Gandhinagar, Gujarat, India", 23.2167, 72.6667),
    ("Priyesh Dave", "Male", "1959-08-07", "23:32", "Dundlod, Rajasthan, India", 27.9167, 75.25),
    ("Shobha Dave", "Female", "1965-08-14", "18:10", "Raigarh, Chhattisgarh, India", 21.8833, 83.4),
    ("Monika Pattanayak", "Female", "1993-02-14", "19:40", "Cuttack, Odisha, India", 20.45, 85.8667),
    ("Akash Zaveri", "Male", "1991-08-31", "16:25", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Harsh Shah", "Male", "1988-10-31", "10:21", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Aniket Shah", "Male", "1988-11-30", "01:30", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Nency A Shah", "Female", "1989-01-06", "06:20", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Ravi Shah", "Male", "1989-10-01", "14:02", "Andheri, Mumbai, Maharashtra, India", 19.1167, 72.8167),
    ("Dhara Ravi Shah", "Female", "1988-12-11", "14:10", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Karan Patel", "Male", "1988-09-05", "07:43", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Manthan", "Male", "1988-11-04", "11:26", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Shreya", "Female", "1988-02-17", "20:10", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Misika Butala", "Female", "1991-03-27", "21:32", "Modasa, Gujarat, India", 23.4667, 73.2833),
    ("Pooja Priya", "Female", "1989-07-02", "06:45", "Sheikhpura, Bihar, India", 25.1333, 85.8333),
    ("Lav Butala", "Male", "1991-04-16", "03:30", "Modasa, Gujarat, India", 23.4667, 73.2833),
    ("Sahil Jani", "Male", "1988-09-23", "18:50", "Jetpur, Gujarat, India", 23.0, 70.9),
    ("Bhavika Bhayani", "Female", "1992-07-15", "01:20", "Mithapur, Gujarat, India", 22.4, 69.0),
    ("Esha Shah", "Female", "1992-01-14", "07:45", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Nayan Shah", "Male", "1989-12-25", "20:30", "Viramgam, Gujarat, India", 23.1167, 72.0167),
    ("Vatsal Raicha", "Male", "1981-04-26", "01:25", "Bhilai, Chhattisgarh, India", 21.2167, 81.4167),
    ("Pooja Dave", "Female", "1986-07-12", "23:35", "Bharuch, Gujarat, India", 21.7, 72.9667),
    ("Harsh Raval", "Male", "1996-06-21", "02:15", "Dundlod, Rajasthan, India", 27.9167, 75.25),
    ("Jigar Mehta", "Male", "1988-10-19", "19:22", "Indore, Madhya Pradesh, India", 22.7167, 75.8167),
    ("Dipti Dave", "Female", "1966-10-10", "09:50", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Kandarp Dave", "Male", "1988-06-14", "20:30", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Shivani Kandarp Dave", "Female", "1988-02-16", "16:07", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Binal Shah", "Female", "1989-07-29", "07:17", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Krutik Shah", "Male", "1989-11-15", "19:13", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Moxta", "Female", "1992-04-13", "13:47", "Vadodara, Gujarat, India", 22.3, 73.2),
    ("Jainith Nayak", "Male", "1985-05-11", "16:40", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Vixita Nayak", "Female", "1986-11-18", "09:16", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Pragati Nayak", "Female", "1989-06-14", "08:45", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Jinal Shah", "Female", "1993-02-19", "18:30", "Sihor, Gujarat, India", 21.6833, 71.9667),
    ("Anmol Mehta", "Male", "1992-07-15", "15:31", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Dharini Anmol Mehta", "Female", "1994-05-27", "14:05", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Pooja Dhaval Shah", "Female", "1991-01-12", "05:10", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Dhaval J Shah", "Male", "1989-05-23", "17:16", "Mumbai, Maharashtra, India", 19.0667, 72.8667),
    ("Paras Gajjar", "Male", "1970-10-28", "12:00", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Viral Gajjar", "Female", "1977-01-30", "05:30", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Kushal Shah", "Male", "1988-04-22", "16:15", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Sneha Shah", "Female", "1988-09-24", "12:45", "Mumbai, Maharashtra, India", 19.0667, 72.8667),
    ("Helena Dave", "Female", "1987-10-15", "04:45", "Ahmedabad, Gujarat, India", 23.0333, 72.5833),
    ("Nandish Dave", "Male", "1988-11-11", "12:55", "Jetpur, Gujarat, India", 21.7167, 70.6167),
]
DRAW = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
VARGAS = ("D2", "D4", "D9", "D10", "D11", "D16", "D24", "D60")


def sn(s):
    return SIGN_NAMES[s]


out = []
for name, sex, dob, tob, place, lat, lon in NORMAL:
    jd = get_julian_day(dob, tob, lat, lon)
    pos = calc_planet_positions(jd, lat, lon)
    P, lag = pos["planets"], pos["lagna"]
    div = calc_divisional_charts(P, lag)
    nak = calc_nakshatra(P["Moon"]["longitude"])
    by = int(dob[:4])
    dasha = [{"planet": d["planet"], "start": d["start_date"], "end": d["end_date"],
              "age_start": int(d["start_date"][:4]) - by, "age_end": int(d["end_date"][:4]) - by}
             for d in calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]]
    d1 = {p: {"sign": sn(P[p]["sign"]), "house": P[p]["house"], "deg": round(P[p]["degree_in_sign"], 2),
              "dignity": P[p].get("dignity"), "retro": P[p].get("retrograde", False)} for p in DRAW}
    charts = {"D1": d1}
    for v in VARGAS:
        charts[v] = {p: sn(div[v][p]) for p in DRAW}
        charts[v]["Lagna"] = sn(div[v]["Lagna"])
    out.append({
        "slug": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"), "name": name, "sex": sex,
        "birth": {"date": dob, "time": tob, "place": place, "lat": lat, "lon": lon},
        "lagna": sn(lag["sign"]), "lagna_lord": lag.get("sign_lord"), "nakshatra": nak["name"],
        "charts": charts, "dasha": dasha,
    })

with open("/app/normal_people.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print(f"stored {len(out)} normal-people chart(s)")
for x in out:
    P = {p: x["charts"]["D1"][p] for p in DRAW}
    print(f"\n{x['name']} ({x['sex']}) {x['birth']['date']} {x['birth']['time']} {x['birth']['place']}")
    print(f"  Lagna {x['lagna']} (lord {x['lagna_lord']}) | Moon nak {x['nakshatra']}")
    for p in DRAW:
        d = P[p]
        print(f"    {p:8} {d['sign']:>11} {d['deg']:>5} H{d['house']:<2} {d['dignity']}")
