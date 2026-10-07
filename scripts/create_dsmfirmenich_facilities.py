"""
dsm-firmenich group + Novonesis production sites missing from the database.
No pharma — industrial fermentation, vitamins, enzymes, food cultures only.
IDs 5001–5012.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

COLUMNS = [
    "ID", "Facility", "Membership tier", "City", "Country", "Address",
    "Contact person", "Website", "Social links", "About",
    "Technology areas", "Technologies", "No. of technologies",
    "Certifications", "Non-technical services", "Open 24/7",
    "Extra information", "Downloads", "Videos", "Logo", "Pilots4U page",
]

FACILITIES = [
    # ── dsm-firmenich ─────────────────────────────────────────────────────────
    {
        "id": 5001,
        "facility": "dsm-firmenich Grenzach",
        "tier": "Captive",
        "city": "Grenzach-Wyhlen",
        "country": "Germany",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "One of dsm-firmenich's largest European manufacturing sites, producing "
            "riboflavin (vitamin B2) by Bacillus subtilis fermentation, vitamin B1 (thiamine), "
            "vitamin B6, and vitamin D3 as well as intermediates for vitamin C synthesis. "
            "The site employs ~1,500 people and is among the highest-volume fermentative "
            "vitamin production complexes in the world, operating since the 1940s under "
            "successive ownership (Hoffmann-La Roche → DSM → dsm-firmenich)."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Large-scale Bacillus subtilis riboflavin fermentation\n"
            "Vitamin B1 and B6 fermentation and chemical synthesis\n"
            "Vitamin D3 bioconversion\n"
            "Crystallisation, spray drying and encapsulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "~1,500 employees. Fermentative riboflavin (B2) capacity among top 3 globally. Operates since 1940s under Roche then DSM then dsm-firmenich.",
    },
    {
        "id": 5002,
        "facility": "dsm-firmenich Dalry",
        "tier": "Captive",
        "city": "Dalry",
        "country": "United Kingdom",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Scottish manufacturing site of dsm-firmenich producing pantothenic acid "
            "(vitamin B5) and vitamin C intermediates by fermentation, and manufacturing "
            "Bovaer® (3-NOP), the methane-reducing feed additive for dairy and beef cattle. "
            "A dedicated Bovaer® production plant opened on the Dalry campus in 2025, "
            "significantly scaling supply of the climate-impact animal nutrition ingredient. "
            "Long-standing fermentation expertise at this site predates the DSM era."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Fermentative pantothenic acid (B5) production\n"
            "Bovaer® (3-NOP) synthesis and formulation\n"
            "Vitamin C intermediate processing\n"
            "Granulation and feed premix manufacturing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "New Bovaer® (3-NOP) dedicated plant opened 2025. Key site for animal nutrition and climate solutions portfolio.",
    },
    {
        "id": 5003,
        "facility": "dsm-firmenich Leeuwarden",
        "tier": "Captive",
        "city": "Leeuwarden",
        "country": "Netherlands",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Dairy fermentation culture manufacturing site in Friesland, Netherlands, "
            "producing the Delvo® range of cheese and yogurt starter cultures and "
            "anti-microbial nisin (a natural food preservative produced by Lactococcus "
            "lactis fermentation). The site has historical roots in Dutch dairy science "
            "and serves cheese and fermented dairy manufacturers globally with "
            "concentrated direct-vat-set (DVS) and bulk culture products."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures",
        "technologies": (
            "Lactic acid bacteria starter culture fermentation\n"
            "Nisin fermentation (Lactococcus lactis)\n"
            "Freeze-drying and spray-drying of concentrated cultures\n"
            "Direct-vat-set (DVS) culture standardisation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "Produces Delvo® dairy cultures and nisin preservative. Part of dsm-firmenich Food & Beverage division.",
    },
    {
        "id": 5004,
        "facility": "dsm-firmenich – Firmenich Geneva Campus (La Plaine)",
        "tier": "Captive",
        "city": "La Plaine",
        "country": "Switzerland",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Main production campus of the former Firmenich business (now dsm-firmenich "
            "Perfumery, Beauty & Care and Taste, Texture & Health divisions), located near "
            "Geneva. Hosts three production plants and a biotechnology pilot facility. "
            "Produces fermentation-derived taste molecules, enzymatically produced flavour "
            "compounds, aroma chemicals, and fragrance ingredients. ~1,450 employees on site. "
            "Centre of excellence for biotransformation and fermentation-derived "
            "flavour/fragrance molecules within the dsm-firmenich group."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Fermentation-derived flavour molecules (yeast and bacterial platforms)\n"
            "Enzymatic bioconversion of terpenoids\n"
            "Flavour fermentation pilot (1–500 L)\n"
            "Synthetic biology platform for aroma chemicals"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "~1,450 employees. 3 production plants. Biotechnology pilot centre for Taste & Flavour fermentation innovation. Centre of former Firmenich group.",
    },
    {
        "id": 5005,
        "facility": "dsm-firmenich Lalden",
        "tier": "Captive",
        "city": "Lalden",
        "country": "Switzerland",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "Valais site within the dsm-firmenich Sisseln vitamin complex network, "
            "producing carotenoid and vitamin intermediates. Lalden handles first-stage "
            "processing and chemical transformation steps upstream of the final vitamin "
            "formulation carried out at Sisseln. The site specialises in carotenoid "
            "chemistry including beta-carotene and lycopene precursor processing."
        ),
        "tech_areas": "Fermentation (industrial)\nDownstream processing",
        "technologies": (
            "Carotenoid intermediate synthesis\n"
            "Vitamin precursor processing\n"
            "Crystallisation and purification"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001",
        "extra": "Part of the dsm-firmenich Swiss vitamin manufacturing network together with Sisseln.",
    },
    {
        "id": 5006,
        "facility": "dsm-firmenich Sete Lagoas – Tortuga Animal Nutrition",
        "tier": "Captive",
        "city": "Sete Lagoas",
        "country": "Brazil",
        "website": "https://www.dsm-firmenich.com",
        "about": (
            "State-of-the-art animal nutrition manufacturing complex opened October 2024 "
            "in Minas Gerais, Brazil, under the Tortuga® brand. Produces mineral and vitamin "
            "premixes, probiotic supplements and fermentation-derived feed additives for "
            "beef and dairy cattle, predominantly for Brazilian and Latin American "
            "agribusiness. Capacity ~100,000 tonnes per year of blended nutrition products. "
            "One of the largest animal nutrition manufacturing investments in Latin America."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures\nFermentation (industrial)",
        "technologies": (
            "Probiotic fermentation and drying for feed applications\n"
            "Vitamin and mineral premix blending\n"
            "Encapsulated nutrient production\n"
            "Fermentation-derived amino acid supplement formulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFAMI-QS",
        "extra": "Opened October 2024. Capacity ~100,000 t/yr. Tortuga® brand (Brazilian market leader in cattle nutrition, owned by DSM/dsm-firmenich since 2004).",
    },
    # ── Novonesis ─────────────────────────────────────────────────────────────
    {
        "id": 5007,
        "facility": "Novonesis Kalundborg Production Campus",
        "tier": "Captive",
        "city": "Kalundborg",
        "country": "Denmark",
        "website": "https://www.novonesis.com",
        "about": (
            "World's largest industrial enzyme production facility, operated by Novonesis "
            "(formed 2023 from merger of Novozymes and Chr. Hansen). The Kalundborg campus "
            "is the global centre of gravity for industrial enzyme manufacturing, producing "
            "enzymes for detergents, food processing, biofuel, textiles, pulp & paper and "
            "animal nutrition. Legendary for symbiotic industrial ecology: waste streams "
            "from adjacent factories (Novo Nordisk, Equinor refinery, Kalundborg utility) "
            "are exchanged on-site in Denmark's first industrial symbiosis network. "
            "~750 employees on campus."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nEnzymatic catalysis\nDownstream processing",
        "technologies": (
            "Large-scale submerged enzyme fermentation (industrial scale; 100,000+ m³ annual throughput)\n"
            "Fed-batch fungal and bacterial fermentation platforms\n"
            "Enzyme recovery by ultrafiltration and centrifugation\n"
            "Granulation (T-granulate), liquid and powder enzyme formulation\n"
            "Industrial symbiosis (waste heat, biogas, gypsum exchange with neighbours)"
        ),
        "n_tech": 5,
        "certs": "ISO 9001\nISO 14001\nISO 45001\nFSSC 22000",
        "extra": "World's largest enzyme production site. Part of Kalundborg Symbiosis (world's first industrial symbiosis network, 1972). ~750 employees. Owned by Novonesis (Novozymes + Chr. Hansen merger 2023).",
    },
    {
        "id": 5008,
        "facility": "Novonesis Hørsholm – Food Cultures & Probiotics Campus",
        "tier": "Captive",
        "city": "Hørsholm",
        "country": "Denmark",
        "website": "https://www.novonesis.com",
        "about": (
            "Novonesis group headquarters and primary food culture & probiotic production "
            "facility in Hørsholm, Denmark. Inherits Chr. Hansen's 150-year history of "
            "microbial culture science. Produces direct-vat-set (DVS) dairy cultures, "
            "probiotic strains (incl. BB-12® Bifidobacterium and LGG®-equivalent strains), "
            "plant-based fermentation cultures and bioprotective cultures for food safety. "
            "Houses the world's largest collection of lactic acid bacteria (~50,000 strains) "
            "and the global Novonesis R&D and innovation centre."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures\nDownstream processing",
        "technologies": (
            "Lactic acid bacteria (LAB) fermentation at scale\n"
            "Bifidobacterium and Lactobacillus probiotic production\n"
            "Freeze-drying (lyophilisation) of concentrated cultures\n"
            "Spray-drying and protective coating of probiotics\n"
            "Bioprotective culture development and standardisation"
        ),
        "n_tech": 5,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
        "extra": "Novonesis group HQ. World's largest LAB strain collection (~50,000 strains). BB-12® is world's most documented probiotic. Chr. Hansen heritage since 1874.",
    },
    {
        "id": 5009,
        "facility": "Novonesis Franklinton",
        "tier": "Captive",
        "city": "Franklinton",
        "country": "United States",
        "website": "https://www.novonesis.com",
        "about": (
            "North American enzyme manufacturing facility of Novonesis (formerly Novozymes "
            "North America headquarters). Produces industrial enzymes for food & beverage, "
            "household care, bioenergy and textile applications, serving over 30 industries. "
            "The Franklinton site is the main US production and operations hub, with "
            "~700 employees in North Carolina. Supports the US biofuel and starch "
            "processing industries as a key customer base."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Submerged enzyme fermentation\n"
            "Enzyme downstream processing and formulation\n"
            "Liquid and granular enzyme products\n"
            "Application labs for food, biofuel and textile enzymes"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFSSC 22000",
        "extra": "Novonesis North America HQ and main US production site. ~700 NC employees. Key supplier to US corn ethanol and food processing industries.",
    },
    {
        "id": 5010,
        "facility": "Novonesis Salem",
        "tier": "Captive",
        "city": "Salem",
        "country": "United States",
        "website": "https://www.novonesis.com",
        "about": (
            "Virginia manufacturing facility of Novonesis (formerly Novozymes) producing "
            "spore-based biosolutions: microbial inoculants and biocontrol products for "
            "agriculture, aquaculture and water treatment. The Salem site has over 75 years "
            "of history in microbial production and received a $5 million expansion in 2025 "
            "to scale production of spore-forming Bacillus-based biostimulants and "
            "probiotics for sustainable agriculture."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Bacillus spore fermentation and sporulation\n"
            "Microbial inoculant drying and formulation\n"
            "Biocontrol agent production (liquid and wettable powder)\n"
            "Aquaculture and water treatment microbial products"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "75+ year history in spore-based microbial products. $5M expansion 2025. Key site for Novonesis BioAg and biosolutions portfolio.",
    },
    {
        "id": 5011,
        "facility": "Novonesis West Allis – Food Cultures & Probiotics",
        "tier": "Captive",
        "city": "West Allis",
        "country": "United States",
        "website": "https://www.novonesis.com",
        "about": (
            "Wisconsin manufacturing site of Novonesis (Chr. Hansen legacy, established "
            "1929) producing food cultures, cheese starters and probiotic ingredients for "
            "the North American dairy, plant-based and dietary supplement markets. "
            "Produces direct-vat-set (DVS) cultures and concentrated freeze-dried "
            "probiotics including HN019 (Bifidobacterium lactis) and Lactobacillus "
            "rhamnosus strains. A $75 million facility expansion was announced to "
            "meet growing demand for probiotic ingredients in the Americas."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures",
        "technologies": (
            "Dairy starter culture fermentation\n"
            "Probiotic LAB fermentation and concentration\n"
            "Freeze-drying of cultures\n"
            "DVS and spray-dried culture production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
        "extra": "Founded 1929 (Chr. Hansen North America legacy). 280 employees. $75M expansion planned. Key probiotics supplier for North American dietary supplements.",
    },
    # ── dsm-firmenich JV ──────────────────────────────────────────────────────
    {
        "id": 5012,
        "facility": "Veramaris – Algal Omega-3 Plant (BASF / DSM JV)",
        "tier": "Captive",
        "city": "Blair",
        "country": "United States",
        "website": "https://www.veramaris.com",
        "about": (
            "Commercial-scale algal omega-3 (EPA + DHA) production facility co-located "
            "with the Novonesis (Novozymes) Blair campus in Nebraska. Veramaris is a "
            "50/50 joint venture between BASF and DSM (now dsm-firmenich) producing "
            "Schizochytrium sp. microalgae at commercial scale to supply EPA+DHA for "
            "aquaculture feed as a sustainable alternative to fish oil. "
            "Annual capacity ~1,200 tonnes EPA+DHA. One of the world's first commercial-scale "
            "microalgal omega-3 plants, opened 2019."
        ),
        "tech_areas": "Algae\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Heterotrophic microalgae fermentation (Schizochytrium sp.)\n"
            "Large-scale fed-batch algal cultivation on glucose\n"
            "Lipid extraction and omega-3 concentration\n"
            "Microalgal biomass drying and oil refining"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFSSC 22000\nFriend of the Sea",
        "extra": "50/50 JV between BASF and DSM (dsm-firmenich). Opened 2019. ~1,200 t/yr EPA+DHA capacity. Co-located with Novonesis Blair campus. Supplies salmon and trout aquaculture globally.",
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


HEADER_FILL = PatternFill(start_color="1B4332", end_color="1B4332", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
ROW_FILL_A  = PatternFill(start_color="E3F2FD", end_color="E3F2FD", fill_type="solid")
ROW_FILL_B  = PatternFill(start_color="FFF8E1", end_color="FFF8E1", fill_type="solid")
THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"), right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"), bottom=Side(style="thin", color="CCCCCC"),
)
COL_WIDTHS = {
    "ID": 6, "Facility": 50, "Membership tier": 16,
    "City": 22, "Country": 16, "Address": 28,
    "Contact person": 20, "Website": 38, "Social links": 18,
    "About": 65, "Technology areas": 32, "Technologies": 48,
    "No. of technologies": 9, "Certifications": 28,
    "Non-technical services": 28, "Open 24/7": 9,
    "Extra information": 55, "Downloads": 10, "Videos": 10,
    "Logo": 28, "Pilots4U page": 18,
}


def make_workbook(facilities: list) -> openpyxl.Workbook:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facilities"
    for ci, col in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=ci, value=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[1].height = 30
    for ri, entry in enumerate(facilities, 2):
        row_data = row_from_entry(entry)
        fill = ROW_FILL_A if ri % 2 == 0 else ROW_FILL_B
        for ci, col in enumerate(COLUMNS, 1):
            cell = ws.cell(row=ri, column=ci, value=row_data.get(col, ""))
            cell.fill = fill
            cell.border = THIN_BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True, horizontal="left")
    from openpyxl.utils import get_column_letter
    for ci, col in enumerate(COLUMNS, 1):
        ws.column_dimensions[get_column_letter(ci)].width = COL_WIDTHS.get(col, 18)
    ws.freeze_panes = "A2"
    return wb


if __name__ == "__main__":
    # ── 1. Write standalone Excel ─────────────────────────────────────────────
    out_path = DATA_DIR / "DSMFirmenich_Novonesis_database.xlsx"
    wb = make_workbook(FACILITIES)
    wb.save(out_path)
    print(f"Saved {len(FACILITIES)} facilities → {out_path}")

    # ── 2. Append to Global Excel ─────────────────────────────────────────────
    global_path = DATA_DIR / "Global_biomanufacturing_database.xlsx"
    wb_global = openpyxl.load_workbook(global_path)
    ws_global = wb_global["All Facilities"]

    existing_ids = set()
    for row in ws_global.iter_rows(min_row=2, values_only=True):
        if row[0] is not None:
            existing_ids.add(row[0])

    appended = 0
    for entry in FACILITIES:
        if entry["id"] in existing_ids:
            print(f"  Skip duplicate ID {entry['id']}")
            continue
        ws_global.append([row_from_entry(entry).get(col, "") for col in COLUMNS])
        appended += 1

    wb_global.save(global_path)
    print(f"Appended {appended} rows to Global database → total {ws_global.max_row - 1} facilities")
