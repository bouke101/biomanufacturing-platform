"""
Additional dsm-firmenich US manufacturing sites.
Also patches the Belvidere entry (was geocoded as Belvidere IL — should be Belvidere NJ).
IDs 5013–5017.
"""
import json
import openpyxl
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

COLUMNS = [
    "ID", "Facility", "Membership tier", "City", "Country", "Address",
    "Contact person", "Website", "Social links", "About",
    "Technology areas", "Technologies", "No. of technologies",
    "Certifications", "Non-technical services", "Open 24/7",
    "Extra information", "Downloads", "Videos", "Logo", "Pilots4U page",
]

NEW_FACILITIES = [
    {
        "id": 5013,
        "facility": "dsm-firmenich Kingstree",
        "tier": "Captive",
        "city": "Kingstree",
        "country": "United States",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "DSM Nutritional Products site in Kingstree, South Carolina, producing "
            "carotenoids including canthaxanthin and beta-carotene through fermentation-derived "
            "and synthetic-route processes for the animal nutrition, aquaculture and food "
            "colouring markets. Canthaxanthin is used as a pigmenting agent in salmon, trout "
            "and poultry feed. Part of dsm-firmenich's Animal Nutrition & Health division."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Carotenoid synthesis and fermentation-derived routes\n"
            "Canthaxanthin and beta-carotene production\n"
            "Encapsulation for feed applications\n"
            "Nutritional ingredient formulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "Produces canthaxanthin for salmon/trout aquaculture pigmentation and poultry skin colour. Part of dsm-firmenich Animal Nutrition & Health.",
    },
    {
        "id": 5014,
        "facility": "dsm-firmenich Newark",
        "tier": "Captive",
        "city": "Newark",
        "country": "United States",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Flavour and fragrance manufacturing facility of dsm-firmenich (Firmenich "
            "heritage) at 150 Firmenich Way, Newark, New Jersey. Produces encapsulated "
            "flavours for food and beverage applications, fragrance ingredients for personal "
            "care, and taste molecules for consumer products. Serves as a key North American "
            "production hub for the Perfumery, Beauty & Care and Taste, Texture & Health "
            "divisions. ~100 employees on site."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Encapsulated flavour manufacturing\n"
            "Fermentation-derived taste molecules\n"
            "Fragrance ingredient production\n"
            "Spray-dried flavour encapsulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "Firmenich heritage site at 150 Firmenich Way, Newark NJ. ~100 employees. North American production hub for dsm-firmenich flavour and fragrance divisions.",
    },
    {
        "id": 5015,
        "facility": "dsm-firmenich Plainsboro – Food & Beverage Pilot",
        "tier": "Pilot facility",
        "city": "Plainsboro",
        "country": "United States",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Food & Beverage co-creation and scale-up pilot facility opened March 2024 "
            "at the dsm-firmenich North America innovation campus in Plainsboro, New Jersey. "
            "Enables customers to develop and scale fermentation-derived flavours, functional "
            "food ingredients, texture systems and health ingredients in collaboration with "
            "dsm-firmenich application scientists. Houses pilot fermentation, formulation "
            "labs and sensory evaluation suites."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Pilot fermentation for taste and flavour molecules\n"
            "Functional ingredient formulation and texturisation\n"
            "Sensory evaluation and application testing\n"
            "Scale-up from bench to pilot for food & beverage customers"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000",
        "extra": "Opened March 2024. Co-creation model: customers develop and scale innovations with dsm-firmenich scientists on-site. Part of Plainsboro North America innovation campus.",
    },
    {
        "id": 5016,
        "facility": "dsm-firmenich Schenectady",
        "tier": "Captive",
        "city": "Schenectady",
        "country": "United States",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Nutritional premix and ingredient blending facility in Schenectady, New York, "
            "established 1995. Produces vitamin and mineral premixes, nutritional blends and "
            "customised ingredient solutions for food fortification, dietary supplements and "
            "animal nutrition customers. Underwent a $10 million production modernisation and "
            "audit-readiness upgrade completed in 2024–2025, adding automation and traceability "
            "systems."
        ),
        "tech_areas": "Fermentation (industrial)\nDownstream processing",
        "technologies": (
            "Vitamin and mineral premix blending\n"
            "Custom nutritional blend formulation\n"
            "Micronutrient encapsulation and coating\n"
            "Automated batch assembly and traceability"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nNSF\nHACCP",
        "extra": "Established 1995. $10M modernisation upgrade 2024–2025. Nutritional premix hub for dsm-firmenich North America Health, Nutrition & Care division.",
    },
    {
        "id": 5017,
        "facility": "dsm-firmenich Tonganoxie – NextGen Pet Nutrition",
        "tier": "Captive",
        "city": "Tonganoxie",
        "country": "United States",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Fully automated pet nutrition premix manufacturing facility ('NextGen Tonganoxie') "
            "opened October 2025 in Kansas. Dedicated exclusively to pet food nutrition, "
            "featuring 100% automated micro-ingredient addition systems, fully traceable batch "
            "assembly and advanced quality control. Produces highly customised vitamin, mineral "
            "and amino acid premixes for pet food manufacturers. Part of dsm-firmenich's "
            "Animal Nutrition & Health pet segment."
        ),
        "tech_areas": "Fermentation (industrial)\nDownstream processing",
        "technologies": (
            "Automated micro-ingredient dosing and blending\n"
            "Fermentation-derived amino acid premix incorporation\n"
            "100% traceable batch assembly system\n"
            "Custom pet nutrition premix manufacturing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nFAMI-QS",
        "extra": "Opened October 2025. 100% automated micro-ingredient addition. Fully traceable. dsm-firmenich's dedicated NextGen pet nutrition manufacturing facility.",
    },
]


def row_from_entry(entry: dict) -> dict:
    return {
        "ID": entry["id"],
        "Facility": entry["facility"],
        "Membership tier": entry["tier"],
        "City": entry["city"],
        "Country": entry["country"],
        "Address": "",
        "Contact person": "",
        "Website": entry.get("website", ""),
        "Social links": "",
        "About": entry.get("about", ""),
        "Technology areas": entry.get("tech_areas", ""),
        "Technologies": entry.get("technologies", ""),
        "No. of technologies": entry.get("n_tech", ""),
        "Certifications": entry.get("certs", ""),
        "Non-technical services": "",
        "Open 24/7": "",
        "Extra information": entry.get("extra", ""),
        "Downloads": "",
        "Videos": "",
        "Logo": "",
        "Pilots4U page": "",
    }


if __name__ == "__main__":
    # ── 1. Append to Global Excel ─────────────────────────────────────────────
    global_path = DATA_DIR / "Global_biomanufacturing_database.xlsx"
    wb = openpyxl.load_workbook(global_path)
    ws = wb["All Facilities"]

    existing_ids = {row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0]}

    appended = 0
    for entry in NEW_FACILITIES:
        if entry["id"] in existing_ids:
            print(f"  Skip duplicate {entry['id']}")
            continue
        ws.append([row_from_entry(entry).get(col, "") for col in COLUMNS])
        appended += 1

    wb.save(global_path)
    print(f"Appended {appended} rows → Global now {ws.max_row - 1} facilities")

    # ── 2. Patch Belvidere NJ coordinates directly in facilities.json ─────────
    json_path = DATA_DIR / "facilities.json"
    with open(json_path) as f:
        facs = json.load(f)

    patched = 0
    for fac in facs:
        if fac["id"] == "dsm-firmenich-belvidere":
            fac["location"]["lat"] = 40.8260
            fac["location"]["lng"] = -75.0774
            patched += 1

    with open(json_path, "w") as f:
        json.dump(facs, f, indent=2, ensure_ascii=False)
    print(f"Patched {patched} Belvidere NJ coordinate(s) in facilities.json")
