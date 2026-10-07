"""
Generate a comprehensive facilities.json from the merged Excel database.

Strategy:
  1. Keep all 159 existing facilities.json entries as-is (have coordinates + good data).
  2. For each row in Global_biomanufacturing_database.xlsx not yet in facilities.json,
     map Excel columns → JSON schema and geocode via hardcoded city lookup.
  3. Write data/facilities.json (replaces the old file).
"""
import json
import re
import openpyxl
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# ── Hardcoded geocoding lookup (city.lower(), country.lower()) → (lat, lng) ─
GEO: dict[tuple, tuple] = {
    # United States
    ("portsmouth", "united states"): (43.0718, -70.7626),
    ("hopkinton", "united states"): (42.2287, -71.5226),
    ("vacaville", "united states"): (38.3566, -121.9877),
    ("cranbury", "united states"): (40.3137, -74.5139),
    ("worcester", "united states"): (42.2626, -71.8023),
    ("bloomington", "united states"): (39.1653, -86.5264),
    ("madison", "united states"): (43.0731, -89.4012),
    ("research triangle park", "united states"): (35.8791, -78.7633),
    ("cary", "united states"): (35.7915, -78.7811),
    ("college station", "united states"): (30.6280, -96.3344),
    ("st. joseph", "united states"): (39.7675, -94.8467),
    ("fremont", "united states"): (37.5485, -121.9886),
    ("bothell", "united states"): (47.7601, -122.2054),
    ("boulder", "united states"): (40.0150, -105.2705),
    ("durham", "united states"): (35.9940, -78.8986),
    ("rockville", "united states"): (39.0840, -77.1528),
    ("baltimore", "united states"): (39.2904, -76.6122),
    ("lansing", "united states"): (42.7325, -84.5555),
    ("alachua", "united states"): (29.7555, -82.4974),
    ("marlborough", "united states"): (42.3459, -71.5523),
    ("oklahoma city", "united states"): (35.4676, -97.5164),
    ("plantation", "united states"): (26.1276, -80.2331),
    ("san diego", "united states"): (32.7157, -117.1611),
    ("waltham", "united states"): (42.3765, -71.2356),
    ("columbus", "united states"): (39.9612, -82.9988),
    ("grove city", "united states"): (39.8815, -83.0930),
    ("milford", "united states"): (42.1398, -71.5490),
    ("bedford", "united states"): (42.4912, -71.2762),
    ("thousand oaks", "united states"): (34.1706, -118.8376),
    ("west greenwich", "united states"): (41.6357, -71.6259),
    ("south san francisco", "united states"): (37.6547, -122.4077),
    ("andover", "united states"): (42.6584, -71.1370),
    ("north chicago", "united states"): (42.3253, -87.8412),
    ("devens", "united states"): (42.5426, -71.5948),
    ("gaithersburg", "united states"): (39.1434, -77.2014),
    ("west point", "united states"): (40.1515, -75.1785),
    ("rensselaer", "united states"): (42.6426, -73.7429),
    ("tarrytown", "united states"): (41.0759, -73.8590),
    ("clayton", "united states"): (35.6507, -78.4575),
    ("norwood", "united states"): (42.1945, -71.1995),
    ("kankakee", "united states"): (41.1200, -87.8612),
    ("indianapolis", "united states"): (39.7684, -86.1581),
    ("juncos", "united states"): (18.2274, -65.9208),
    ("barceloneta", "united states"): (18.4496, -66.5374),
    ("los angeles", "united states"): (34.0522, -118.2437),
    ("novato", "united states"): (38.1074, -122.5697),
    ("allston", "united states"): (42.3534, -71.1335),
    ("santa monica", "united states"): (34.0195, -118.4912),
    ("mcpherson", "united states"): (38.3706, -97.6642),
    ("cambridge", "united states"): (42.3736, -71.1097),
    ("raleigh", "united states"): (35.7796, -78.6382),
    ("newark", "united states"): (39.6837, -75.7497),   # DE (NIIMBL)
    ("king of prussia", "united states"): (40.0912, -75.3830),
    ("bethesda", "united states"): (38.9807, -77.1003),
    ("branchburg", "united states"): (40.5657, -74.7424),
    ("mountain view", "united states"): (37.3861, -122.0839),
    ("lebanon", "united states"): (43.6423, -72.2520),
    ("milwaukee", "united states"): (43.0389, -87.9065),
    ("horsham", "united states"): (40.1743, -75.1221),
    ("pearl river", "united states"): (41.0590, -74.0220),
    ("seattle", "united states"): (47.6062, -122.3321),
    ("morrisville", "united states"): (35.8229, -78.8242),
    ("albany", "united states"): (42.6526, -73.7562),
    ("swiftwater", "united states"): (41.0629, -75.3310),
    ("skokie", "united states"): (42.0334, -87.7334),
    ("boston", "united states"): (42.3601, -71.0589),
    ("golden", "united states"): (39.7555, -105.2211),
    ("emeryville", "united states"): (37.8309, -122.2850),
    ("ames", "united states"): (42.0347, -93.6200),
    ("decatur", "united states"): (39.8403, -88.9548),
    ("blair", "united states"): (41.5436, -96.1248),
    ("germantown", "united states"): (39.1735, -77.2716),
    ("frederick", "united states"): (39.4143, -77.4105),
    ("foster city", "united states"): (37.5585, -122.2711),
    ("san francisco", "united states"): (37.7749, -122.4194),
    ("mooresville", "united states"): (35.5846, -80.7998),
    ("philadelphia", "united states"): (39.9526, -75.1652),
    ("new brunswick", "united states"): (40.4862, -74.4518),
    ("hilliard", "united states"): (40.0334, -83.1581),
    ("bristol", "united states"): (40.0907, -74.8743),
    ("berkeley", "united states"): (37.8716, -122.2727),
    ("olean", "united states"): (42.0784, -78.4297),
    ("oceanside", "united states"): (33.1959, -117.3795),
    ("teaneck", "united states"): (40.8940, -74.0076),
    ("brisbane", "united states"): (37.6806, -122.3997),
    ("allendale", "united states"): (41.0198, -74.1360),
    ("lexington", "united states"): (42.4473, -71.2245),
    ("kalamazoo", "united states"): (42.2917, -85.5872),
    ("new haven", "united states"): (41.3082, -72.9279),
    ("framingham", "united states"): (42.2793, -71.4162),
    ("east hanover", "united states"): (40.8196, -74.3621),
    ("libertyville", "united states"): (42.2836, -87.9531),
    ("lawrenceville", "united states"): (40.2990, -74.7352),
    ("rahway", "united states"): (40.6076, -74.2774),
    ("new york", "united states"): (40.7128, -74.0060),
    ("chicago", "united states"): (41.8781, -87.6298),
    ("houston", "united states"): (29.7604, -95.3698),
    ("atlanta", "united states"): (33.7490, -84.3880),
    ("miami", "united states"): (25.7617, -80.1918),
    ("minneapolis", "united states"): (44.9778, -93.2650),
    ("new brighton", "united states"): (45.0649, -93.2024),
    ("spokane", "united states"): (47.6588, -117.4260),
    ("st. louis", "united states"): (38.6270, -90.1994),
    ("chesterfield", "united states"): (38.6631, -90.5771),
    ("mcpherson", "united states"): (38.3706, -97.6642),
    ("pearland", "united states"): (29.5635, -95.2860),
    ("belvidere", "united states"): (42.2634, -88.8443),
    # Canada
    ("mississauga", "canada"): (43.5890, -79.6441),
    ("charlottetown", "canada"): (46.2382, -63.1311),
    ("toronto", "canada"): (43.6532, -79.3832),
    ("laval", "canada"): (45.6066, -73.7124),
    ("saskatoon", "canada"): (52.1332, -106.6700),
    ("vancouver", "canada"): (49.2827, -123.1207),
    ("ottawa", "canada"): (45.4215, -75.6919),
    ("calgary", "canada"): (51.0447, -114.0719),
    # South Korea
    ("incheon", "south korea"): (37.4563, 126.7052),
    ("seoul", "south korea"): (37.5665, 126.9780),
    # China
    ("wuxi", "china"): (31.5700, 120.3000),
    ("shanghai", "china"): (31.2304, 121.4737),
    ("beijing", "china"): (39.9042, 116.4074),
    # European (global CDMOs, not in Pilots4U pilot facility network)
    ("visp", "switzerland"): (46.2940, 7.8810),
    ("barbengo", "switzerland"): (45.9871, 8.9449),
    ("sisseln", "switzerland"): (47.5580, 7.8878),
    ("berlin", "germany"): (52.5200, 13.4050),
    ("hanau", "germany"): (50.1282, 8.9169),
    ("laupheim", "germany"): (48.2284, 9.8783),
    ("biberach an der riß", "germany"): (48.0970, 9.7890),
    ("strängnäs", "sweden"): (59.3791, 17.0289),
    ("kalundborg", "denmark"): (55.6802, 11.0890),
    ("oulu", "finland"): (65.0121, 25.4651),
    ("delft", "netherlands"): (52.0116, 4.3571),
    ("pompey", "france"): (48.7712, 6.1278),
    ("billingham", "united kingdom"): (54.6023, -1.2801),
    ("london", "united kingdom"): (51.5074, -0.1278),
    ("cambridge", "united kingdom"): (52.2053, 0.1218),
}

# Facility name → (lat, lng) overrides for ambiguous cases
NAME_GEO: dict[str, tuple] = {
    "niimbl (national institute for innovation in manufacturing biopharmaceuticals)": (39.6837, -75.7497),
    "nc state btec": (35.7869, -78.6748),
    "mit koch institute (pilot scale biomanufacturing)": (42.3604, -71.0921),
    "waisman biomanufacturing": (43.0765, -89.4327),
    "center for breakthrough medicines (cbm)": (40.0912, -75.3830),
    "walter reed national military medical center bioproduction facility": (38.9807, -77.1003),
    "lonza biologics portsmouth": (43.0718, -70.7626),
    "lonza biologics vacaville": (38.3566, -121.9877),
    "genentech (south san francisco)": (37.6547, -122.4077),
    "genentech vacaville": (38.3566, -121.9877),
    "sanofi genzyme (framingham / allston)": (42.3534, -71.1335),
    "amgen puerto rico": (18.2274, -65.9208),
    "regeneron pharmaceuticals (rensselaer)": (42.6426, -73.7429),
}


def normalize(name: str) -> str:
    s = str(name).lower()
    for pat in [r"\s*[–—-]+\s*closed(/acquired)?", r"\s*\(closed(/acquired)?\)"]:
        s = re.sub(pat, "", s, flags=re.I)
    s = re.sub(r"[,./]+$", "", s).strip()
    return re.sub(r"\s+", " ", s)


def slugify(name: str) -> str:
    s = normalize(name)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


def geocode(facility_name: str, city: str, country: str):
    key = normalize(facility_name)
    if key in NAME_GEO:
        return NAME_GEO[key]
    c = city.strip().lower()
    co = country.strip().lower()
    if (c, co) in GEO:
        return GEO[(c, co)]
    # Try without "United States" for USA alias
    if co in ("usa", "us"):
        if (c, "united states") in GEO:
            return GEO[(c, "united states")]
    return None


def region_for(country: str) -> str:
    EUROPE = {
        "france", "germany", "netherlands", "finland", "spain", "sweden",
        "denmark", "belgium", "portugal", "united kingdom", "ireland",
        "italy", "poland", "czech republic", "austria", "norway",
        "switzerland", "hungary", "romania", "slovakia", "croatia",
        "greece", "bulgaria", "latvia", "lithuania", "estonia",
        "luxembourg", "slovenia",
    }
    NA = {"united states", "usa", "canada", "mexico"}
    ASIA = {"south korea", "china", "japan", "india", "singapore", "taiwan"}
    c = country.strip().lower()
    if c in NA:
        return "North America"
    if c in EUROPE:
        return "Europe"
    if c in ASIA:
        return "Asia"
    if c in ("brazil", "argentina", "chile", "colombia"):
        return "South America"
    if c in ("australia", "new zealand"):
        return "Oceania"
    return "Other"


TIER_TO_FACILITY_TYPE = {
    "basic member": "Pilot",
    "advanced member": "Pilot",
    "premium member": "Pilot",
    "open cmo": "CDMO",
    "captive": "Captive",
    "pilot facility": "Pilot",
    "closed": "Captive",
}

MODALITY_MAP = {
    "cell cultivation": "Mammalian cell culture",
    "microbial fermentation": "Microbial fermentation",
    "viral vector production": "Viral vector",
    "mrna/lnp manufacturing": "mRNA",
    "fill-finish": "Fill-Finish",
    "downstream processing": "Downstream processing",
    "plasma fractionation": "Plasma fractionation",
    "enzymatic catalysis": "Enzymatic catalysis",
    "fermentation and digestion": "Fermentation (industrial)",
    "separation technologies": "Separation",
    "cell therapy manufacturing": "Cell therapy",
    "vaccine production": "Vaccine production",
    "chemical conjugation": "ADC",
    "chemical synthesis": "Chemical synthesis",
    "oligonucleotide synthesis": "Oligonucleotide synthesis",
    "size reduction": "Size reduction",
    "sterilisation": "Sterilisation",
    "thermal processing": "Thermal processing",
    "thermochemical": "Thermochemical",
    "material technologies": "Material technologies",
    "pulping": "Pulping",
    "algae": "Algae",
}

OWNER_OVERRIDES = {
    "lonza biologics portsmouth": "Lonza Group AG",
    "lonza biologics hopkinton": "Lonza Group AG",
    "lonza biologics vacaville": "Lonza Group AG",
    "wuxi biologics (cranbury)": "WuXi Biologics",
    "wuxi biologics (worcester)": "WuXi Biologics",
    "catalent biologics bloomington": "Catalent (Novo Holdings)",
    "catalent biologics madison": "Catalent (Novo Holdings)",
    "fujifilm diosynth biotechnologies (rtp)": "Fujifilm Diosynth",
    "fujifilm diosynth biotechnologies (college station)": "Fujifilm Diosynth",
    "boehringer ingelheim bioxcellence (st. joseph)": "Boehringer Ingelheim",
    "boehringer ingelheim bioxcellence (fremont)": "Boehringer Ingelheim",
    "agc biologics (seattle)": "AGC Biologics",
    "agc biologics (boulder)": "AGC Biologics",
    "kbi biopharma (durham)": "KBI BioPharma / JSR Corp.",
    "kbi biopharma (rockville)": "KBI BioPharma / JSR Corp.",
    "emergent biosolutions (bayview)": "Emergent BioSolutions",
    "emergent biosolutions (lansing)": "Emergent BioSolutions",
    "national resilience (alachua)": "National Resilience",
    "national resilience (marlborough)": "National Resilience",
    "amgen thousand oaks": "Amgen Inc.",
    "amgen west greenwich": "Amgen Inc.",
    "amgen puerto rico": "Amgen Inc.",
    "genentech (south san francisco)": "Genentech / Roche",
    "genentech vacaville": "Genentech / Roche",
    "pfizer andover biologics": "Pfizer Inc.",
    "pfizer (mcpherson)": "Pfizer Inc.",
    "abbvie biologics (north chicago)": "AbbVie Inc.",
    "bristol-myers squibb devens": "Bristol-Myers Squibb",
    "astrazeneca / medimmune (gaithersburg)": "AstraZeneca / MedImmune",
    "merck & co. (west point)": "Merck & Co.",
    "biogen (research triangle park)": "Biogen Inc.",
    "regeneron pharmaceuticals (rensselaer)": "Regeneron Pharmaceuticals",
    "novo nordisk (clayton)": "Novo Nordisk",
    "moderna (norwood)": "Moderna Inc.",
    "csl behring (kankakee)": "CSL Behring",
    "eli lilly (indianapolis)": "Eli Lilly and Company",
    "sanofi genzyme (framingham / allston)": "Sanofi",
    "sanofi (swiftwater)": "Sanofi",
    "grifols (los angeles)": "Grifols S.A.",
    "takeda (cambridge/lexington)": "Takeda Pharmaceutical",
    "gilead sciences / kite pharma (santa monica)": "Gilead Sciences / Kite",
    "biomarin (novato)": "BioMarin Pharmaceutical",
    "therapure biopharma": "Therapure Biopharma",
    "biovectra": "BioVectra / Thermo Fisher",
    "andelyn biosciences": "Andelyn Biosciences",
    "forge biologics": "Forge Biologics",
    "elevatebio basecamp": "ElevateBio",
    "nc state btec": "North Carolina State University",
    "niimbl (national institute for innovation in manufacturing biopharmaceuticals)": "NIST / University of Delaware",
    "center for breakthrough medicines (cbm)": "Center for Breakthrough Medicines",
    "institut armand-frappier (iaf) – inrs": "INRS",
    "vaccine and infectious disease organization (vido)": "University of Saskatchewan",
}


def excel_to_json(row: dict, existing_id=None) -> dict:
    facility_name = str(row.get("Facility", "") or "").strip()
    city          = str(row.get("City", "") or "").strip()
    country       = str(row.get("Country", "") or "").strip()
    tier          = str(row.get("Membership tier", "") or "").strip()
    website       = str(row.get("Website", "") or "").strip()
    about         = str(row.get("About", "") or "").strip()
    tech_areas    = str(row.get("Technology areas", "") or "").strip()
    certs_raw     = str(row.get("Certifications", "") or "").strip()
    extra         = str(row.get("Extra information", "") or "").strip()
    logo          = str(row.get("Logo", "") or "").strip()
    p4u_page      = str(row.get("Pilots4U page", "") or "").strip()

    slug = existing_id if existing_id else slugify(facility_name)

    ft_key = tier.lower()
    facility_type = TIER_TO_FACILITY_TYPE.get(ft_key, "Pilot")
    if "closed" in facility_name.lower():
        facility_type = "Captive"  # use Captive type, notes will say closed

    mods_raw = [t.strip() for t in tech_areas.split("\n") if t.strip()]
    modalities = []
    for m in mods_raw:
        mapped = MODALITY_MAP.get(m.lower(), m)
        if mapped and mapped not in modalities:
            modalities.append(mapped)

    certs = [c.strip() for c in certs_raw.split("\n") if c.strip()
             and c.strip() not in ("N/A – research institute", "Research grade",
                                    "Research grade / academic GMP-like",
                                    "cGMP-like training environment",
                                    "FDA cGMP (historical)", "EMA GMP (historical)")]

    # Remove source ID tag that was added during merge
    legacy = re.sub(r"\s*\|\s*Source ID:\s*\S+", "", extra).strip()

    scale: list[str]
    if facility_type == "Pilot":
        scale = ["Pilot"]
    elif facility_type == "CDMO":
        scale = ["Development", "Clinical", "Commercial"]
    else:
        scale = ["Commercial"]

    # Owner
    owner_key = normalize(facility_name)
    owner = OWNER_OVERRIDES.get(owner_key, facility_name)

    # Geocode
    coords = geocode(facility_name, city, country)
    if coords is None:
        # fallback: try stripping "(closed)" variants from city
        coords = geocode(facility_name, city.split(",")[0].strip(), country)
    lat = coords[0] if coords else 0.0
    lng = coords[1] if coords else 0.0

    visible = True
    # Closed entries stay visible but are marked
    if ft_key == "closed" or "closed" in facility_name.lower():
        if legacy:
            legacy = legacy + " [CLOSED]"
        else:
            legacy = "[CLOSED]"

    return {
        "id": slug,
        "name": facility_name,
        "owner": owner,
        "location": {
            "city": city,
            "country": country,
            "lat": lat,
            "lng": lng,
            "region": region_for(country),
        },
        "facilityType": facility_type,
        "modalities": modalities,
        "scale": scale,
        "capacity": "",
        "clients": [],
        "products": [],
        "legacy": legacy,
        "certifications": certs,
        "website": website,
        "imageUrl": logo if logo.startswith("http") else "",
        "notes": about,
        "visible": visible,
        "source": "pilots4u" if tier.lower() in ("basic member", "advanced member", "premium member") else "manual",
        "pilots4uPage": p4u_page,
    }


# ── Load existing facilities.json ────────────────────────────────────────────
with open(DATA_DIR / "facilities.json") as f:
    existing: list[dict] = json.load(f)

existing_by_name: dict[str, dict] = {normalize(e["name"]): e for e in existing}
print(f"Existing facilities.json: {len(existing)} entries")

# ── Load merged Excel ─────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(DATA_DIR / "Global_biomanufacturing_database.xlsx", read_only=True)
ws = wb["All Facilities"]
header = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
excel_rows = []
for row in ws.iter_rows(min_row=2, values_only=True):
    excel_rows.append(dict(zip(header, row)))
print(f"Excel rows: {len(excel_rows)}")

# ── Merge: existing entries take priority; new entries are geocoded from Excel ─
output: list[dict] = []
seen_ids: set[str] = set()
geocode_failed: list[str] = []

for row in excel_rows:
    name = str(row.get("Facility", "") or "").strip()
    key  = normalize(name)

    if key in existing_by_name:
        # Use the existing high-quality entry
        entry = dict(existing_by_name[key])
        # Update with any richer Excel fields not already present
        if not entry.get("website") and row.get("Website"):
            entry["website"] = str(row["Website"])
        if not entry.get("notes") and row.get("About"):
            entry["notes"] = str(row["About"])
    else:
        # New entry: build from Excel row
        entry = excel_to_json(row)
        if entry["location"]["lat"] == 0.0:
            geocode_failed.append(f"{name} ({row.get('City')}, {row.get('Country')})")

    # Ensure unique IDs (slug collision fallback)
    eid = entry["id"]
    if eid in seen_ids:
        eid = eid + "-2"
        entry["id"] = eid
    seen_ids.add(eid)
    output.append(entry)

# ── Report ────────────────────────────────────────────────────────────────────
print(f"\nOutput: {len(output)} facilities")
print(f"  Kept from existing json: {sum(1 for e in output if e['id'] in {ex['id'] for ex in existing})}")
print(f"  New entries: {len(output) - sum(1 for e in output if e['id'] in {ex['id'] for ex in existing})}")
if geocode_failed:
    print(f"\nGeocoding FAILED for {len(geocode_failed)} entries (lat/lng = 0,0):")
    for g in geocode_failed:
        print(f"  {g}")
else:
    print("\nAll entries geocoded successfully.")

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = DATA_DIR / "facilities.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nSaved {len(output)} facilities → {out_path}")
