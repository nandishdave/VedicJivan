from pydantic import BaseModel, Field, field_validator


class UnavailabilityCreate(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    start_time: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    end_time: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    is_holiday: bool = False
    reason: str = ""


class UnavailabilityResponse(BaseModel):
    id: str
    date: str
    start_time: str | None = None
    end_time: str | None = None
    is_holiday: bool
    reason: str = ""


class AvailableSlot(BaseModel):
    start: str
    end: str


# ── Business Hours Settings ──


class DayHours(BaseModel):
    """Business hours for a single day of the week."""

    day: int = Field(..., ge=0, le=6, description="0=Mon, 1=Tue, ..., 6=Sun")
    is_open: bool = True
    open_time: str = Field("10:00", pattern=r"^\d{2}:\d{2}$")
    close_time: str = Field("18:00", pattern=r"^\d{2}:\d{2}$")

    @field_validator("close_time")
    @classmethod
    def close_after_open(cls, v, info):
        open_time = info.data.get("open_time")
        if open_time and info.data.get("is_open"):
            oh, om = map(int, open_time.split(":"))
            ch, cm = map(int, v.split(":"))
            if ch * 60 + cm <= oh * 60 + om:
                raise ValueError("close_time must be after open_time")
        return v


class BusinessHoursSettings(BaseModel):
    """Full business hours configuration stored in db.settings."""

    timezone: str = "Asia/Kolkata"
    weekly_hours: list[DayHours] = Field(
        default_factory=lambda: [
            DayHours(day=0),
            DayHours(day=1),
            DayHours(day=2),
            DayHours(day=3),
            DayHours(day=4),
            DayHours(day=5),
            DayHours(day=6, is_open=False),
        ]
    )

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v):
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

        try:
            ZoneInfo(v)
        except (ZoneInfoNotFoundError, KeyError):
            raise ValueError(f"Invalid IANA timezone: {v}")
        return v

    @field_validator("weekly_hours")
    @classmethod
    def validate_weekly_hours(cls, v):
        if len(v) != 7:
            raise ValueError("weekly_hours must contain exactly 7 entries")
        days = sorted([d.day for d in v])
        if days != list(range(7)):
            raise ValueError("weekly_hours must contain days 0-6 exactly once")
        return sorted(v, key=lambda d: d.day)


class BusinessHoursResponse(BaseModel):
    """Response model for business hours settings."""

    timezone: str
    weekly_hours: list[DayHours]


class ReportSection(BaseModel):
    """A single configurable section in the Kundli report."""

    id: str
    label: str
    description: str
    is_paid: bool = True
    enabled: bool = True
    order: int


DEFAULT_REPORT_SECTIONS: list[ReportSection] = [
    ReportSection(id="birth_chart",     label="Birth Chart",            description="North Indian Rashi Chakra SVG + full planet positions table.",                                is_paid=False, enabled=True, order=1),
    ReportSection(id="basic_details",   label="Basic Details",          description="Birth particulars, coordinates, time conversions, panchanga and luminary timings.",           is_paid=False, enabled=True, order=2),
    ReportSection(id="avkahada",        label="Avkahada Chakra",        description="Traditional Vedic chart attributes: varna, vasya, yoni, gana, nadi, paya, tatva.",            is_paid=False, enabled=True, order=3),
    ReportSection(id="favourable",      label="Favourable Points",      description="Lucky planets, days, numbers, colours, gemstones for the Lagna.",                              is_paid=False, enabled=True, order=4),
    ReportSection(id="ghatak",          label="Ghatak (Malefics)",      description="Inauspicious planets, days, nakshatras, tithis to avoid for the Lagna.",                       is_paid=False, enabled=True, order=5),
    ReportSection(id="planet_consideration", label="Planet Considerations", description="Per-planet narrative: sign, house, lordship, aspects given/received, interpretation + remedies.", is_paid=False, enabled=True, order=6),
    ReportSection(id="ascendant",       label="Ascendant",              description="Lagna explanation and your ascendant's character traits.",                                     is_paid=False, enabled=True, order=7),
    ReportSection(id="nakshatra",       label="Nakshatra",              description="Lunar mansion details, ruling deity, symbol, and pada interpretation.",                        is_paid=False, enabled=True, order=8),
    ReportSection(id="character_life",  label="Character & Life",       description="Personality traits, life patterns, and natural disposition.",                                  is_paid=False, enabled=True, order=9),
    ReportSection(id="yogas",           label="Yogas",                  description="Classical planetary combinations present in the chart.",                                       is_paid=False, enabled=True, order=10),
    ReportSection(id="doshas",          label="Doshas & Afflictions",   description="Kaal Sarp, Pitra, Guru Chandal, Mangal Dosha etc. + remedies.",                                is_paid=False, enabled=True, order=11),
    ReportSection(id="bhava_analysis",  label="Bhava (House) Analysis", description="House-by-house analysis of all 12 bhavas.",                                                    is_paid=False, enabled=True, order=12),
    ReportSection(id="manglik",         label="Mangal Dosha",           description="Manglik dosha check from Lagna and Moon, with severity and cancellations.",                    is_paid=False, enabled=True, order=13),
    ReportSection(id="sadesati",        label="Sade Sati",              description="Saturn's 7.5-year transit cycle through Moon's sign and adjacent signs.",                      is_paid=False, enabled=True, order=14),
    ReportSection(id="gochar",          label="Gochar (Transits)",      description="Current planetary transits over the natal chart.",                                             is_paid=False, enabled=True, order=15),
    ReportSection(id="dasha",           label="Mahadasha",              description="Vimshottari Mahadasha sequence — 120-year planetary period cycle.",                            is_paid=False, enabled=True, order=16),
    ReportSection(id="antardasha",      label="Antardasha",             description="Sub-periods within the current Mahadasha.",                                                    is_paid=False, enabled=True, order=17),
    ReportSection(id="pratyantar",      label="Pratyantar Dasha",       description="Sub-sub-periods (3rd level) within each Antardasha.",                                          is_paid=False, enabled=True, order=18),
    ReportSection(id="divisional",      label="Divisional Charts",      description="D9 (marriage), D10 (career), D7 (children) analysis.",                                         is_paid=False, enabled=True, order=19),
    ReportSection(id="friendship",      label="Friendship Table",       description="Permanent (Naisargika), Temporary (Tatkalika) and Compound (Panchadha) friendship matrices.", is_paid=False, enabled=True, order=20),
    ReportSection(id="shadbala",        label="Planetary Strength",     description="Shadbala — which planets are strong or weak and why.",                                         is_paid=False, enabled=True, order=21),
    ReportSection(id="western_aspects", label="Planetary Aspects (Western)", description="Western-style angular aspects (conjunction, opposition, trine, square, sextile, minor).", is_paid=False, enabled=True, order=22),
    ReportSection(id="graha_drishti",  label="Graha Drishti (Vedic Aspects)",description="Classical Vedic planetary aspects: 7th for all, plus Mars 4/8, Jupiter 5/9, Saturn 3/10, Rahu/Ketu 5/9.", is_paid=False, enabled=True, order=23),
    ReportSection(id="planet_positions",label="Planet Positions",       description="Complete planet ephemeris table with degrees, sign, nakshatra, dignity.",                      is_paid=False, enabled=True, order=24),
    ReportSection(id="numerology",      label="Numerology",             description="Moolank, Bhagyank, Namank and personal year analysis (Chaldean + Vedic).",                     is_paid=False, enabled=True, order=25),
    ReportSection(id="remedies",        label="Gemstone & Remedies",    description="Gemstone recommendations and personalised remedial measures.",                                 is_paid=False, enabled=True, order=26),
    # Reserved for the v2 paid narrative tier — disabled in free PDF until Phase 4 ships.
    ReportSection(id="predictions",     label="Life Area Predictions",  description="AI-generated combined-reading narrative across 15 life areas (v2 paid tier).",                 is_paid=True,  enabled=False, order=99),
]
