"""
Add BASF facilities (IDs 8001–8003) and update existing ID 20.
Run: python3 scripts/create_basf_facilities.py
"""
import openpyxl
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

COLUMNS = [
    "ID", "Facility", "Membership tier", "City", "Country", "Address",
    "Contact person", "Website", "Social links", "About",
    "Technology areas", "Technologies", "No. of technologies",
    "Certifications", "Non-technical services", "Open 24/7",
    "Extra information", "Downloads", "Videos", "Logo", "Pilots4U page",
    "Main products", "Annual capacity (est.)",
]

NEW_FACILITIES = [
    {
        "id": 8001,
        "facility": "BASF – Ludwigshafen Verbund (Vitamin E & A Production)",
        "tier": "Captive",
        "city": "Ludwigshafen am Rhein",
        "country": "Germany",
        "website": "https://www.basf.com/nutrition",
        "about": (
            "BASF's large-scale Vitamin E and Vitamin A chemical synthesis plant at the "
            "Ludwigshafen Verbund site, one of the world's largest integrated chemical "
            "production complexes (10 km², 220 production units). BASF is the world's "
            "largest producer of synthetic Vitamin E (all-rac-α-tocopheryl acetate) from "
            "petrochemical isophytol and trimethylhydroquinone, with estimated capacity of "
            "~50,000 MT/yr. Vitamin A (retinyl acetate/palmitate) is also synthesised here "
            "from petrochemical building blocks. Both vitamins are supplied as feed-grade, "
            "food-grade and pharmaceutical-grade ingredients globally under the Lutavit® and "
            "Basovit® brand portfolio."
        ),
        "tech_areas": "Downstream processing\nFermentation (industrial)",
        "technologies": (
            "Vitamin E (all-rac-α-tocopheryl acetate) chemical synthesis\n"
            "Vitamin A (retinyl acetate, retinyl palmitate) chemical synthesis\n"
            "Vitamin encapsulation and beadlet formulation\n"
            "Feed-grade and pharmaceutical-grade vitamin finishing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFSSC 22000\nFAMI-QS\nGMP (pharma grades)",
        "extra": (
            "World's largest single Vitamin E producer (~50,000 MT/yr). Vitamins sold under "
            "Lutavit® (feed) and Basovit® (human nutrition) brands. Integral part of BASF "
            "Nutrition & Health segment (~€2.6B revenue). Co-located with ID 20 (riboflavin) "
            "and 8002 (ecoflex) at Ludwigshafen."
        ),
        "main_products": (
            "Vitamin E (all-rac-α-tocopheryl acetate, Lutavit® E brand)\n"
            "Vitamin A (retinyl acetate, retinyl palmitate)\n"
            "Vitamin E oil solutions and emulsions\n"
            "Vitamin A oil solutions and beadlets\n"
            "Vitamin E / A premix preparations"
        ),
        "annual_capacity": (
            "Vitamin E: ~50,000 MT/yr (world's largest Vitamin E producer)\n"
            "Vitamin A: ~8,000–12,000 MT/yr"
        ),
    },
    {
        "id": 8002,
        "facility": "BASF – Ludwigshafen Biopolymers (ecoflex® / ecovio®)",
        "tier": "Captive",
        "city": "Ludwigshafen am Rhein",
        "country": "Germany",
        "website": "https://www.basf.com/biopolymers",
        "about": (
            "BASF's ecoflex® and ecovio® biopolymer production plant at Ludwigshafen, "
            "Germany. ecoflex® is a certified compostable, biodegradable polyester "
            "(polybutylene adipate-co-terephthalate, PBAT) used in agricultural mulch film, "
            "compostable bags, food packaging and coating applications. BASF expanded ecoflex® "
            "capacity to ~74,000 MT/yr in 2024, making it the world's largest PBAT plant. "
            "ecovio® is a compounded product combining ecoflex® with Ingeo™ PLA "
            "(from NatureWorks) for rigid compostable packaging and foam. Both products carry "
            "EN 13432 and OK Compost HOME certification."
        ),
        "tech_areas": "Downstream processing\nFermentation (industrial)",
        "technologies": (
            "ecoflex® PBAT (polybutylene adipate-co-terephthalate) polymerisation\n"
            "ecovio® biopolymer compounding (ecoflex® + Ingeo PLA blend)\n"
            "Compostable film and packaging material production"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001\nEN 13432\nOK Compost HOME\nDIN CERTCO",
        "extra": (
            "World's largest PBAT plant (74,000 MT/yr ecoflex®). "
            "ecovio® compounds ecoflex® with NatureWorks Ingeo PLA. "
            "Both certified fully compostable (EN 13432, OK Compost HOME). "
            "Key material for single-use plastics directive compliance in Europe."
        ),
        "main_products": (
            "ecoflex® PBAT (biodegradable polybutylene adipate-co-terephthalate)\n"
            "ecovio® biopolymer compound (ecoflex® + Ingeo™ PLA blend)\n"
            "Compostable film, bag and coating resin grades"
        ),
        "annual_capacity": (
            "ecoflex® PBAT: ~74,000 MT/yr (world's largest PBAT plant, expanded 2024)\n"
            "ecovio® compounds: several thousand MT/yr"
        ),
    },
    {
        "id": 8003,
        "facility": "BASF – Sandefjord Omega-3 Concentrate Plant (Pronova)",
        "tier": "Captive",
        "city": "Sandefjord",
        "country": "Norway",
        "website": "https://www.basf.com/omega3",
        "about": (
            "BASF's pharmaceutical and nutritional omega-3 fatty acid concentrate production "
            "plant in Sandefjord, Norway, formerly Pronova Biopharma (acquired by BASF in 2013 "
            "for ~NOK 5.1 billion). The world's leading manufacturer of pharmaceutical-grade "
            "omega-3 ethyl esters (EPA + DHA) under the OMACOR® brand, which is the only "
            "omega-3 drug approved for severe hypertriglyceridemia in both Europe and the US "
            "(sold as Lovaza® and Epanova® in North America). Also produces food- and "
            "supplement-grade omega-3 concentrates. Raw fish oil (anchovy, sardine, mackerel) "
            "is refined, concentrated and esterified to produce EPA:DHA concentrate. "
            "Pharmaceutical-grade product is GMP-certified and FDA-inspected."
        ),
        "tech_areas": "Downstream processing\nFermentation (industrial)",
        "technologies": (
            "Fish oil molecular distillation and fractionation\n"
            "Omega-3 ethyl ester concentration (EPA + DHA enrichment)\n"
            "Pharmaceutical-grade omega-3 finishing and encapsulation\n"
            "Omega-3 triglyceride re-esterification"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nGMP (EU and FDA)\nFDA-inspected\nKosher\nHalal",
        "extra": (
            "Acquired from Pronova Biopharma 2013 (~NOK 5.1B). "
            "OMACOR® is the world's leading pharmaceutical omega-3 product (EPA:DHA concentrate). "
            "Also serves supplement and food markets. "
            "Pronova heritage dates to 1838 whaling in Sandefjord. "
            "Also operates Ålesund crude fish oil refinery as upstream feedstock site."
        ),
        "main_products": (
            "OMACOR® omega-3 ethyl esters (pharmaceutical grade, EPA + DHA ~90%)\n"
            "Supplement-grade omega-3 concentrate (EPA + DHA ~65–85%)\n"
            "Food-grade omega-3 oil (EPA + DHA ~30–50%)\n"
            "Omega-3 triglyceride re-esterified (rTG) concentrate"
        ),
        "annual_capacity": (
            "Omega-3 pharmaceutical concentrate: ~10,000–15,000 MT/yr\n"
            "Total omega-3 concentrates (all grades): ~20,000–25,000 MT/yr"
        ),
    },
    {
        "id": 8004,
        "facility": "BASF – Ålesund Omega-3 Refinery (Pronova)",
        "tier": "Captive",
        "city": "Ålesund",
        "country": "Norway",
        "website": "https://www.basf.com/omega3",
        "about": (
            "BASF's crude fish oil receiving, degumming, deacidification and refining facility "
            "in Ålesund (Ellingsøy), Norway, part of the Pronova supply chain (acquired 2013). "
            "Ålesund is one of Europe's largest fish-landing ports. The site processes raw "
            "pelagic fish oil (anchovy, mackerel, herring) into refined fish oil that is then "
            "shipped to the Sandefjord concentrate plant for further EPA/DHA enrichment. "
            "Handles ~50,000–80,000 MT/yr of crude fish oil input."
        ),
        "tech_areas": "Downstream processing",
        "technologies": (
            "Crude fish oil degumming, neutralisation and bleaching\n"
            "Fish oil deodorisation and refining\n"
            "Winterisation and fractionation of fish oil"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000\nMSC Chain of Custody\nIFOS 5-star",
        "extra": (
            "Pronova heritage (acquired 2013). Upstream refinery supplying Sandefjord plant "
            "(ID 8003). Ålesund is Norway's largest fish-landing port. "
            "IFOS 5-star certified crude fish oil processing."
        ),
        "main_products": (
            "Refined fish oil (EPA + DHA ~30%)\n"
            "Winterised and fractionated fish oil fractions\n"
            "Crude fish oil processing intermediates for omega-3 concentration"
        ),
        "annual_capacity": (
            "Crude fish oil input: ~50,000–80,000 MT/yr\n"
            "Refined fish oil output: ~30,000–50,000 MT/yr"
        ),
    },
    {
        "id": 8005,
        "facility": "BASF – Minden Choline Chloride Plant",
        "tier": "Captive",
        "city": "Minden",
        "country": "Germany",
        "website": "https://www.basf.com/nutrition",
        "about": (
            "BASF's choline chloride production plant in Minden, North Rhine-Westphalia, "
            "Germany. Choline chloride (Vitamin B4) is an essential feed additive for poultry "
            "and swine, preventing fatty liver syndrome and supporting methionine metabolism. "
            "BASF is one of the world's major choline chloride producers, supplying "
            "feed-grade (50% and 75% solutions, 60% dry) and pharmaceutical-grade products "
            "globally under the Lutavit® Choline brand."
        ),
        "tech_areas": "Downstream processing\nFermentation (industrial)",
        "technologies": (
            "Choline chloride synthesis (trimethylamine + ethylene oxide route)\n"
            "Feed-grade choline chloride solution and dry corn-cob carrier production\n"
            "Pharmaceutical-grade choline chloride purification"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000\nFAMI-QS",
        "extra": (
            "Lutavit® Choline brand. Feed additive essential for poultry, swine and aquaculture. "
            "50% and 75% liquid solutions plus 60% dry-on-carrier. "
            "One of BASF's key specialty animal nutrition ingredient sites in Europe."
        ),
        "main_products": (
            "Choline chloride 75% aqueous solution (feed grade)\n"
            "Choline chloride 60% dry (on corn-cob carrier)\n"
            "Pharmaceutical-grade choline chloride"
        ),
        "annual_capacity": (
            "Choline chloride: ~30,000–50,000 MT/yr (all grades combined)"
        ),
    },
    {
        "id": 8006,
        "facility": "BASF – Geismar Butanediol Complex (BDO/THF/GBL)",
        "tier": "Captive",
        "city": "Geismar",
        "country": "United States",
        "website": "https://www.basf.com/bdo",
        "about": (
            "BASF's Geismar, Louisiana production complex for 1,4-butanediol (BDO) and "
            "downstream derivatives: tetrahydrofuran (THF), gamma-butyrolactone (GBL) and "
            "polytetrahydrofuran (polyTHF / PTMEG). BDO is the key monomer for biodegradable "
            "PBAT (ecoflex®) and PBT engineering plastics. The Geismar site is one of the "
            "world's largest BDO complexes, producing from petrochemical feedstocks. "
            "Bio-based BDO (from fermentation) is under evaluation as a future feedstock "
            "transition aligned with Mater-Biotech's Genomatica-technology bio-BDO (see ID 7060). "
            "Geismar is a major component of BASF's global biopolymer supply chain."
        ),
        "tech_areas": "Downstream processing\nFermentation (industrial)",
        "technologies": (
            "1,4-Butanediol (BDO) production (Reppe acetylene-formaldehyde route)\n"
            "Tetrahydrofuran (THF) production from BDO\n"
            "Gamma-butyrolactone (GBL) production\n"
            "PolyTHF (PTMEG) polymerisation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nREACH",
        "extra": (
            "One of world's largest BDO/THF complexes. BDO is feedstock for ecoflex® PBAT "
            "(biopolymers), PBT engineering plastics and spandex (PTMEG). "
            "Bio-based BDO transition pathway under evaluation (Genomatica process). "
            "Geismar is BASF's largest US site."
        ),
        "main_products": (
            "1,4-Butanediol (BDO) — monomer for biodegradable PBAT and PBT plastics\n"
            "Tetrahydrofuran (THF) — solvent and PTMEG monomer\n"
            "Gamma-butyrolactone (GBL) — solvent and NMP alternative\n"
            "PolyTHF / PTMEG — monomer for spandex and polyurethanes"
        ),
        "annual_capacity": (
            "BDO: ~250,000–300,000 MT/yr\n"
            "THF: ~100,000–150,000 MT/yr\n"
            "PolyTHF/PTMEG: ~50,000–80,000 MT/yr"
        ),
    },
]

# Update data for existing ID 20
ID20_UPDATES = {
    "Main products": (
        "Vitamin B2 (riboflavin) — Ashbya gossypii submerged fermentation\n"
        "Natuphos® E phytase (Aspergillus niger fermentation, market-leading feed phytase)\n"
        "Beta-carotene (Lucaropen®, natural — Blakeslea trispora fermentation)\n"
        "Lycopene (LycoVit®, natural — Blakeslea trispora fermentation)\n"
        "Astaxanthin (AstaSana® — Haematococcus pluvialis microalgae)\n"
        "Specialty biotransformation and bioconversion products"
    ),
    "Annual capacity (est.)": (
        "Riboflavin: ~3,000–5,000 MT/yr (world top-2; reduced share due to Chinese competition)\n"
        "Natuphos® E phytase: hundreds of MT/yr (world's first commercial phytase, launched 1991)\n"
        "Beta-carotene: ~500–1,000 MT/yr (natural-grade)\n"
        "Lycopene: ~200–500 MT/yr\n"
        "Astaxanthin: ~50–150 MT/yr"
    ),
    "About": (
        "BASF's fermentation and biotech production plant at Ludwigshafen, Germany, birthplace "
        "of industrial riboflavin fermentation. BASF was the first company to produce riboflavin "
        "(Vitamin B2) at industrial scale by fermentation of Ashbya gossypii, a filamentous "
        "fungus that overproduces riboflavin naturally. Also manufactures Natuphos® E, the "
        "world's first commercially launched phytase (1991), by Aspergillus niger fermentation; "
        "and natural carotenoids (beta-carotene, lycopene) by Blakeslea trispora fermentation, "
        "as well as astaxanthin from Haematococcus microalgae. Part of BASF's Nutrition & Health "
        "segment. Co-located at the 10 km² Ludwigshafen Verbund site with ID 8001 (Vitamin E/A "
        "synthesis) and ID 8002 (ecoflex® biopolymers)."
    ),
    "Technology areas": "Microbial fermentation\nFermentation (industrial)\nEnzymatic catalysis",
    "Technologies": (
        "Ashbya gossypii submerged fermentation for riboflavin (Vitamin B2)\n"
        "Aspergillus niger fermentation for Natuphos® E phytase\n"
        "Blakeslea trispora fermentation for beta-carotene and lycopene\n"
        "Haematococcus pluvialis microalgae cultivation for astaxanthin\n"
        "Bioconversion and biotransformation processes"
    ),
    "No. of technologies": 5,
    "Certifications": "ISO 9001\nISO 14001\nFSSC 22000\nFAMI-QS",
    "Extra information": (
        "World's first commercial phytase (Natuphos® E, launched 1991). "
        "Birthplace of industrial Ashbya gossypii riboflavin fermentation. "
        "Natural carotenoids by Blakeslea trispora fermentation (Lucaropen® beta-carotene, LycoVit® lycopene). "
        "Astaxanthin (AstaSana®) by microalgae cultivation."
    ),
}


def row_from_entry(e: dict) -> list:
    d = {
        "ID": e["id"], "Facility": e["facility"], "Membership tier": e["tier"],
        "City": e["city"], "Country": e["country"], "Address": "",
        "Contact person": "", "Website": e.get("website", ""), "Social links": "",
        "About": e.get("about", ""), "Technology areas": e.get("tech_areas", ""),
        "Technologies": e.get("technologies", ""),
        "No. of technologies": e.get("n_tech", ""),
        "Certifications": e.get("certs", ""), "Non-technical services": "",
        "Open 24/7": "", "Extra information": e.get("extra", ""),
        "Downloads": "", "Videos": "", "Logo": "", "Pilots4U page": "",
        "Main products": e.get("main_products", ""),
        "Annual capacity (est.)": e.get("annual_capacity", ""),
    }
    return [d.get(col, "") for col in COLUMNS]


if __name__ == "__main__":
    path = DATA_DIR / "Global_biomanufacturing_database.xlsx"
    wb = openpyxl.load_workbook(path)
    ws = wb["All Facilities"]
    header = [c.value for c in ws[1]]

    existing_ids = {row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0]}

    # ── 1. Append new facilities ──────────────────────────────────────────────
    appended = 0
    for entry in NEW_FACILITIES:
        if entry["id"] in existing_ids:
            print(f"  Skip {entry['id']} – already in DB")
            continue
        ws.append(row_from_entry(entry))
        appended += 1
    print(f"Appended {appended} new BASF facilities")

    # ── 2. Update existing ID 20 ──────────────────────────────────────────────
    col_idx = {v: i + 1 for i, v in enumerate(header) if v}
    updated_fields = 0
    for row_num, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[col_idx["ID"] - 1].value == 20:
            for field, value in ID20_UPDATES.items():
                if field in col_idx:
                    ws.cell(row=row_num, column=col_idx[field], value=value)
                    updated_fields += 1
                else:
                    print(f"  Warning: column '{field}' not found – skipping")
            print(f"Updated {updated_fields} fields for ID 20")
            break

    wb.save(path)
    print(f"Saved → {ws.max_row - 1} total facilities")
