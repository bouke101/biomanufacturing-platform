"""
Create Asia (non-China) and China industrial biotech / food facility databases.
NO PHARMA — only: industrial fermentation, food biotech, industrial enzymes,
biofuels/biochemicals, bioplastics, algae, probiotics (food-grade).
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

COLUMNS = [
    "ID", "Facility", "Membership tier", "City", "Country", "Address",
    "Contact person", "Website", "Social links", "About",
    "Technology areas", "Technologies", "No. of technologies",
    "Certifications", "Non-technical services", "Open 24/7",
    "Extra information", "Downloads", "Videos", "Logo", "Pilots4U page",
]

# ── China facilities ──────────────────────────────────────────────────────────

CHINA_FACILITIES = [
    # ── Amino acids ──────────────────────────────────────────────────────────
    {
        "id": 3001,
        "facility": "Meihua Holdings Group Co. Ltd",
        "tier": "Captive",
        "city": "Langfang",
        "country": "China",
        "website": "https://www.meihua.info",
        "about": (
            "World's largest amino acid producer, specialising in glutamic acid, lysine, "
            "threonine, valine and other feed and food amino acids via large-scale microbial "
            "fermentation from corn feedstocks. Annual capacity exceeds 1.5 million tonnes "
            "of amino acid products across 6 production bases in China."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Large-scale submerged fermentation (up to 500 m³ fermenters)\n"
            "Continuous glucose supply from corn wet-milling\n"
            "Crystallisation and spray-drying downstream\n"
            "Wastewater biogas recovery"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFSSC 22000\nHACCP",
        "extra": "Listed on Shenzhen Stock Exchange. Largest single-site amino acid fermentation complex in the world.",
    },
    {
        "id": 3002,
        "facility": "Fufeng Group Co. Ltd",
        "tier": "Captive",
        "city": "Hulunbuir",
        "country": "China",
        "website": "https://www.fufeng.com",
        "about": (
            "Major producer of monosodium glutamate (MSG), xanthan gum, corn-based starch "
            "sugars and polyglutamic acid by large-scale fermentation. Operates multiple plants "
            "in Inner Mongolia and Shandong Province using corn as primary feedstock. "
            "Annual MSG capacity exceeds 300,000 tonnes."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Fed-batch and continuous fermentation for glutamic acid\n"
            "Xanthan gum bioreactors\n"
            "Corn wet-milling integration\n"
            "Evaporation and crystallisation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "Listed on Hong Kong Stock Exchange. Also produces functional starch products and animal nutrition ingredients.",
    },
    {
        "id": 3003,
        "facility": "Shandong Shouguang Meihua Amino Acid Co. Ltd",
        "tier": "Captive",
        "city": "Shouguang",
        "country": "China",
        "website": "https://www.meihua.info",
        "about": (
            "Large-scale glutamic acid and MSG producer in Shandong Province, part of the "
            "Meihua Group ecosystem. Produces monosodium glutamate and crystalline glutamic "
            "acid from corn fermentation for China's food seasoning industry. "
            "Capacity ~150,000 tonnes MSG per year."
        ),
        "tech_areas": "Microbial fermentation\nDownstream processing",
        "technologies": (
            "Glutamic acid fed-batch fermentation (Corynebacterium glutamicum)\n"
            "Isoelectric crystallisation\n"
            "MSG neutralisation and drying"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "Exports MSG and glutamic acid to SE Asia, Africa and Middle East.",
    },
    {
        "id": 3004,
        "facility": "Qujing Shengkai Innovations Ltd",
        "tier": "Captive",
        "city": "Qujing",
        "country": "China",
        "website": "",
        "about": (
            "Amino acid producer in Yunnan Province leveraging local corn and sugar resources. "
            "Specialises in threonine, tryptophan and branched-chain amino acids (BCAA) for "
            "feed and food applications. Growing export presence in Southeast Asian markets."
        ),
        "tech_areas": "Microbial fermentation\nDownstream processing",
        "technologies": (
            "Microbial amino acid fermentation\n"
            "Ion exchange purification\n"
            "Spray drying and packaging"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000",
        "extra": "Located in Yunnan Province; key supplier to SE Asian feed manufacturers.",
    },
    # ── Yeast ─────────────────────────────────────────────────────────────────
    {
        "id": 3005,
        "facility": "Angel Yeast Co. Ltd",
        "tier": "Captive",
        "city": "Yichang",
        "country": "China",
        "website": "https://www.angelyeast.com",
        "about": (
            "China's largest yeast manufacturer and one of the global top five. Produces "
            "baker's yeast, nutritional yeast, yeast extracts, selenium-enriched yeast, "
            "fermentation nutrients and yeast-derived food flavourings. Serves food, animal "
            "nutrition and industrial biotechnology sectors. Annual yeast capacity exceeds "
            "200,000 tonnes across 14 global production bases."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Aerobic fed-batch yeast cultivation (up to 300 m³)\n"
            "Yeast extract autolysis and hydrolysis\n"
            "Spray drying and drum drying\n"
            "Selenium biofortification\n"
            "Continuous yeast culture systems"
        ),
        "n_tech": 5,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
        "extra": "Listed on Shenzhen Stock Exchange. Founded 1986. Production bases in Egypt, Russia, Chile and Indonesia.",
    },
    {
        "id": 3006,
        "facility": "Lesaffre – Tianjin Lesaffre Yeast Co. Ltd",
        "tier": "Captive",
        "city": "Tianjin",
        "country": "China",
        "website": "https://www.lesaffre.com",
        "about": (
            "Chinese manufacturing subsidiary of Lesaffre, the world's leading yeast and "
            "fermentation specialist. Produces baker's yeast, instant dry yeast and sourdough "
            "cultures for the Chinese food industry and Asia-Pacific market. Also manufactures "
            "yeast extracts and fermentation media for industrial clients."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nProbiotics & cultures",
        "technologies": (
            "Fed-batch yeast propagation\n"
            "Yeast cream separation\n"
            "Instant dry yeast production\n"
            "Spray drying of yeast extracts"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHalal\nKosher",
        "extra": "Part of Lesaffre Group global production network. Serves bakeries and food manufacturers across China and SE Asia.",
    },
    # ── Organic acids ─────────────────────────────────────────────────────────
    {
        "id": 3007,
        "facility": "BBCA Group – Anhui BBCA Biochemical Co. Ltd",
        "tier": "Captive",
        "city": "Bengbu",
        "country": "China",
        "website": "https://www.bbca.com.cn",
        "about": (
            "Leading producer of citric acid, lactic acid and gluconic acid in China, "
            "based in Bengbu, Anhui Province. Uses corn starch as feedstock for large-scale "
            "fermentation. Vertically integrated from corn processing to food-grade and "
            "industrial-grade organic acids. One of China's top 5 citric acid producers."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Submerged Aspergillus niger fermentation for citric acid\n"
            "Lactic acid bacterial fermentation\n"
            "Calcium salt precipitation and acidification\n"
            "Ion exchange and membrane filtration purification"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "Annual citric acid capacity ~200,000 tonnes. Associated with COFCO Group ecosystem.",
    },
    {
        "id": 3008,
        "facility": "Weifang Ensign Industry Co. Ltd",
        "tier": "Captive",
        "city": "Weifang",
        "country": "China",
        "website": "https://www.ensignind.com",
        "about": (
            "One of China's largest citric acid manufacturers, based in Shandong Province. "
            "Produces citric acid and sodium citrate via Aspergillus niger submerged "
            "fermentation on corn-based substrates. Exports to over 50 countries and is "
            "among the world's top three citric acid producers by volume."
        ),
        "tech_areas": "Microbial fermentation\nDownstream processing",
        "technologies": (
            "Submerged Aspergillus fermentation\n"
            "Calcium salt precipitation\n"
            "Crystallisation and granulation\n"
            "Sodium citrate production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
        "extra": "Annual citric acid capacity ~300,000 tonnes. Top 3 global citric acid producer.",
    },
    {
        "id": 3009,
        "facility": "Henan Jindan Lactic Acid Technology Co. Ltd",
        "tier": "Captive",
        "city": "Zhumadian",
        "country": "China",
        "website": "https://www.jindan.com.cn",
        "about": (
            "Specialist L-lactic acid and D-lactic acid producer via microbial fermentation "
            "in Henan Province. Supplies food-grade, industrial-grade and high-purity lactic "
            "acid to food, cosmetics, bioplastic and chemical markets globally. Key supplier "
            "for PLA (polylactic acid) biopolymer production chains."
        ),
        "tech_areas": "Microbial fermentation\nDownstream processing",
        "technologies": (
            "Batch and fed-batch lactic acid fermentation\n"
            "Membrane filtration and electrodialysis purification\n"
            "High-purity L- and D-lactic acid crystallisation\n"
            "Lactide synthesis pilot line"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP\nFDA registration",
        "extra": "Annual lactic acid capacity ~100,000 tonnes. Key supplier to NatureWorks and Total Corbion PLA chains. Exports to Europe, North America, Japan.",
    },
    # ── Industrial enzymes ────────────────────────────────────────────────────
    {
        "id": 3010,
        "facility": "Novozymes (China) Investment Co. Ltd – Tianjin Plant",
        "tier": "Captive",
        "city": "Tianjin",
        "country": "China",
        "website": "https://www.novozymes.com",
        "about": (
            "Tianjin manufacturing facility of Novozymes A/S (now dsm-firmenich), the world's "
            "largest industrial enzyme company. Produces fermentation-derived enzymes for food "
            "processing, textiles, biofuel, detergent and agriculture markets across Asia-Pacific. "
            "One of the largest enzyme production sites in Asia."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nDownstream processing",
        "technologies": (
            "Fed-batch submerged fermentation (up to 100 m³)\n"
            "Enzyme recovery by ultrafiltration\n"
            "Granulation and liquid enzyme formulation\n"
            "Spray drying"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nISO 45001",
        "extra": "Part of dsm-firmenich following 2023 merger. Serves China and Asia-Pacific markets.",
    },
    {
        "id": 3011,
        "facility": "Vland Biotech Group Co. Ltd",
        "tier": "Open CMO",
        "city": "Qingdao",
        "country": "China",
        "website": "https://www.vlandbio.com",
        "about": (
            "Industrial enzyme and animal nutrition biotechnology company in Qingdao. "
            "Develops and manufactures phytases, proteases, xylanases, amylases and probiotics "
            "for animal feed and food applications. Operates as an open CMO offering contract "
            "enzyme fermentation and custom biotech production to international clients."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Submerged and solid-state fermentation\n"
            "Enzyme concentration and coating technology\n"
            "Probiotic culture production and drying\n"
            "Custom strain development"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFAMI-QS\nGMP (feed grade)",
        "extra": "Listed on Shenzhen Stock Exchange. Exports to 60+ countries. 200+ patents in enzyme engineering.",
    },
    {
        "id": 3012,
        "facility": "Habio Bioengineering Co. Ltd",
        "tier": "Open CMO",
        "city": "Chengdu",
        "country": "China",
        "website": "https://www.habio.cn",
        "about": (
            "Enzyme manufacturer and industrial biotech company in Sichuan Province. "
            "Specialises in phytases, NSP enzymes, cellulases and composite enzyme products "
            "for feed and food applications. Provides contract fermentation services for "
            "custom enzyme production. Annual capacity ~20,000 tonnes of enzyme products."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Submerged and solid-state fermentation\n"
            "Enzyme spray drying\n"
            "Probiotic culture and lyophilisation"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000\nFAMI-QS",
        "extra": "Founded 2000. Serves feed mills and food manufacturers across Asia.",
    },
    {
        "id": 3013,
        "facility": "Sunson Industry Group Co. Ltd",
        "tier": "Open CMO",
        "city": "Wuxi",
        "country": "China",
        "website": "https://www.sunsonbio.com",
        "about": (
            "Major industrial enzyme manufacturer in Jiangsu Province. Produces textile, "
            "paper, food and biofuel enzymes including cellulases, amylases, proteases and "
            "lipases by submerged fermentation. Offers contract enzyme production services "
            "to international clients. One of China's top 5 enzyme manufacturers by volume."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Submerged fermentation up to 100 m³\n"
            "Fed-batch fungal and bacterial culture\n"
            "Ultrafiltration concentration\n"
            "Liquid and granular enzyme formulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "Exports to 70+ countries. Strong position in textile and pulp & paper enzyme markets.",
    },
    {
        "id": 3014,
        "facility": "Wuhan Sunhy Biology Co. Ltd",
        "tier": "Open CMO",
        "city": "Wuhan",
        "country": "China",
        "website": "https://www.sunhybio.com",
        "about": (
            "Industrial biotechnology company in Wuhan providing fermentation and enzyme "
            "solutions for food, beverage and feed industries. Offers contract fermentation, "
            "baking enzyme development and microbial culture services. Located in Wuhan "
            "Biolake high-tech zone."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Submerged fungal and bacterial fermentation\n"
            "Baking enzyme blending and standardisation\n"
            "Probiotic culture production"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000",
        "extra": "Located in Wuhan Biolake biotech park. CMO services for food ingredient companies.",
    },
    # ── Biofuels / biochemicals ───────────────────────────────────────────────
    {
        "id": 3015,
        "facility": "COFCO Biochemical (Anhui) Co. Ltd",
        "tier": "Captive",
        "city": "Bengbu",
        "country": "China",
        "website": "https://www.cofco.com",
        "about": (
            "State-owned biorefinery under COFCO Group producing fuel ethanol, lactic acid "
            "and starch-based biochemicals from corn in Anhui Province. One of China's largest "
            "integrated fermentation biorefineries, with annual fuel ethanol capacity "
            "~500,000 tonnes."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Continuous and batch ethanol fermentation\n"
            "Molecular sieve ethanol dehydration\n"
            "Lactic acid fermentation\n"
            "Corn starch wet milling"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "Part of COFCO Group, China's largest food processing enterprise. Annual capacity ~500,000 tonnes fuel ethanol.",
    },
    {
        "id": 3016,
        "facility": "Tianguan Group Co. Ltd",
        "tier": "Captive",
        "city": "Nanyang",
        "country": "China",
        "website": "https://www.tianguan.com.cn",
        "about": (
            "One of China's original four designated fuel ethanol producers, based in Henan "
            "Province. Utilises wheat and corn feedstocks for large-scale fermentative ethanol "
            "production. Also produces DDGS animal feed as co-product. Annual capacity "
            "~600,000 tonnes bioethanol."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Continuous fermentation for fuel ethanol\n"
            "Batch distillation and rectification\n"
            "Molecular sieve dehydration\n"
            "DDGS drying and pelletisation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "One of the original four state-designated fuel ethanol producers in China.",
    },
    {
        "id": 3017,
        "facility": "Guangxi Guitang (Group) Co. Ltd",
        "tier": "Captive",
        "city": "Guigang",
        "country": "China",
        "website": "https://www.guitang.com",
        "about": (
            "Integrated sugarcane biorefinery in Guangxi Province producing sugar, fuel "
            "ethanol, pulp and animal feed. One of China's largest sugarcane processors, "
            "with a substantial bioethanol plant co-located at the sugar refinery using "
            "molasses and sugarcane juice. Annual ethanol production ~100,000 tonnes."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Sugarcane juice and molasses ethanol fermentation\n"
            "Continuous distillation\n"
            "Bagasse co-generation\n"
            "Vinasse biogas recovery"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "Located in Guangxi, China's largest sugarcane-growing region. Vertically integrated cane-to-ethanol model.",
    },
    # ── Specialty carbohydrates / starch ──────────────────────────────────────
    {
        "id": 3018,
        "facility": "Shandong Longlive Bio-Technology Co. Ltd",
        "tier": "Captive",
        "city": "Dezhou",
        "country": "China",
        "website": "https://www.longlive.cn",
        "about": (
            "Specialty carbohydrate biotechnology company producing xylose, xylitol, "
            "fructooligosaccharides (FOS) and arabinoxylan from corn cob lignocellulose. "
            "Pioneered industrial-scale xylose fermentation in China. Annual xylose capacity "
            "~100,000 tonnes, making it one of the world's largest xylose producers."
        ),
        "tech_areas": "Enzymatic catalysis\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "Acid and enzymatic hydrolysis of corn cob\n"
            "Xylose hydrogenation to xylitol\n"
            "Enzymatic FOS synthesis\n"
            "Membrane filtration and chromatographic purification"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "One of the world's largest xylitol and xylose producers. Key supplier to food and pharma excipient markets.",
    },
    {
        "id": 3019,
        "facility": "Jilin Roquette Starch Co. Ltd",
        "tier": "Captive",
        "city": "Jilin",
        "country": "China",
        "website": "https://www.roquette.com",
        "about": (
            "Chinese joint venture of Roquette Frères (France), one of the world's largest "
            "starch and derivatives companies. Produces corn starch, glucose syrup, sorbitol, "
            "maltodextrin and fermentation feedstocks from corn. Key supplier of glucose and "
            "fermentation substrates to the Chinese biotech industry. Capacity ~400,000 tonnes "
            "corn processed per year."
        ),
        "tech_areas": "Fermentation (industrial)\nEnzymatic catalysis\nDownstream processing",
        "technologies": (
            "Corn wet milling\n"
            "Enzymatic starch hydrolysis and saccharification\n"
            "Glucose isomerisation (HFCS)\n"
            "Sorbitol hydrogenation\n"
            "Spray drying and crystallisation"
        ),
        "n_tech": 5,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "Key supplier of fermentation substrates to Chinese industrial biotech. Part of Roquette Group.",
    },
    # ── Vitamins ──────────────────────────────────────────────────────────────
    {
        "id": 3020,
        "facility": "DSM Nutritional Products (China) Ltd – Tianjin",
        "tier": "Captive",
        "city": "Tianjin",
        "country": "China",
        "website": "https://www.dsm.com",
        "about": (
            "Tianjin manufacturing facility of dsm-firmenich producing fermentation-derived "
            "vitamins including riboflavin (vitamin B2) and vitamin C for food fortification, "
            "feed nutrition and industrial markets. One of the world's largest riboflavin "
            "production sites."
        ),
        "tech_areas": "Microbial fermentation\nDownstream processing",
        "technologies": (
            "Bacillus subtilis riboflavin fermentation\n"
            "Two-step vitamin C fermentation (Gluconobacter / Ketogulonigenium)\n"
            "Crystallisation and spray drying\n"
            "Vitamin formulation and blending"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "Part of dsm-firmenich (2023 merger of DSM and Firmenich). Global leader in fermentative vitamins.",
    },
    # ── Food cultures / probiotics ────────────────────────────────────────────
    {
        "id": 3021,
        "facility": "IFF Nutrition & Biosciences China (Shanghai)",
        "tier": "Open CMO",
        "city": "Shanghai",
        "country": "China",
        "website": "https://www.iff.com",
        "about": (
            "IFF's Nutrition & Biosciences division (formerly DuPont Danisco) operates "
            "fermentation production in China for food and beverage cultures, probiotics, "
            "enzymes and specialty ingredients. Serves dairy, bakery and food manufacturing "
            "sectors across Asia. Holds an extensive strain library with 30,000+ cultures."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nProbiotics & cultures",
        "technologies": (
            "Lactic acid bacteria starter culture fermentation\n"
            "Probiotic lyophilisation (freeze drying)\n"
            "Industrial enzyme production by submerged fermentation\n"
            "Culture standardisation and blending"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "Global leader in food cultures and probiotics. Part of IFF group (merged with DuPont N&B 2021).",
    },
    {
        "id": 3022,
        "facility": "Chr. Hansen (Shanghai) Co. Ltd",
        "tier": "Open CMO",
        "city": "Shanghai",
        "country": "China",
        "website": "https://www.chr-hansen.com",
        "about": (
            "China subsidiary of Chr. Hansen A/S (now dsm-firmenich) producing microbial "
            "cultures, probiotics and natural colorants for the food and nutrition industry. "
            "Supplies dairy, plant-based and dietary supplement manufacturers across Asia. "
            "Holds the world's largest collection of lactic acid bacteria cultures."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures",
        "technologies": (
            "Lactic acid bacteria fermentation\n"
            "Freeze-drying and spray-drying culture technology\n"
            "Natural fermentation-derived colorants\n"
            "Probiotic viability and enumeration testing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal",
        "extra": "Part of dsm-firmenich following 2023 merger. Supplies ~40% of the world's dairy cultures.",
    },
    # ── Food fermentation (large scale) ──────────────────────────────────────
    {
        "id": 3023,
        "facility": "Kweichow Moutai Co. Ltd",
        "tier": "Captive",
        "city": "Renhuai",
        "country": "China",
        "website": "https://www.moutaichina.com",
        "about": (
            "World's most valuable spirits brand and one of the largest traditional solid-state "
            "fermentation operations globally. Produces Moutai baijiu in Guizhou Province using "
            "multi-round sorghum and wheat qu (brick koji) fermentation. The 33,000-tonne annual "
            "production represents an unmatched scale in solid-state bioprocessing."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Solid-state sorghum fermentation (sand-tank process, 9 rounds)\n"
            "Brick koji (Daqu) microbial ecosystem management\n"
            "Pit mud microbial community cultivation\n"
            "Traditional batch distillation (pot still)"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nHACCP\nGB/T national standard certification",
        "extra": "Market cap ~$250B. Annual baijiu production ~75,000 tonnes. World's largest solid-state fermentation complex.",
    },
    {
        "id": 3024,
        "facility": "Tsingtao Brewery Co. Ltd – Qingdao Main Plant",
        "tier": "Captive",
        "city": "Qingdao",
        "country": "China",
        "website": "https://www.tsingtaobeer.com",
        "about": (
            "China's largest international beer brand, operating industrial-scale lager "
            "fermentation at the flagship Qingdao plant. Notable for fermentation scale, "
            "process consistency and a biotechnology R&D centre focused on yeast strain "
            "development and fermentation process innovation. Annual brewing capacity "
            "~8 million kilolitres."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Large cylindroconical lager fermenters (up to 4,000 hL)\n"
            "Yeast propagation and management\n"
            "Continuous filtration and pasteurisation\n"
            "CIP and SIP systems"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "Founded 1903. Exports to 100+ countries. Listed on Hong Kong and Shanghai stock exchanges.",
    },
    {
        "id": 3025,
        "facility": "Inner Mongolia Yili Industrial Group Co. Ltd",
        "tier": "Captive",
        "city": "Hohhot",
        "country": "China",
        "website": "https://www.yili.com",
        "about": (
            "China's largest dairy company and Asia's top food & beverage enterprise. "
            "Operates large-scale dairy fermentation manufacturing for yogurt, kefir and "
            "probiotic dairy products across 50+ plants. Runs a proprietary microbiology "
            "research institute for strain development and fermentation optimisation. "
            "Revenue ~RMB 120 billion."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures\nDownstream processing",
        "technologies": (
            "Industrial dairy fermentation (LAB cultures)\n"
            "Aseptic filling technology\n"
            "UHT processing\n"
            "Probiotic lyophilisation and spray drying"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHACCP",
        "extra": "R&D centres in Netherlands (WUR partnership) and New Zealand. 900+ patents in dairy biotech.",
    },
    # ── Algae / marine biotech ────────────────────────────────────────────────
    {
        "id": 3026,
        "facility": "Qingdao Seawin Biotech Group Co. Ltd",
        "tier": "Captive",
        "city": "Qingdao",
        "country": "China",
        "website": "https://www.seawin.com.cn",
        "about": (
            "Marine biotech company specialising in seaweed-derived products including "
            "alginate, agar, carrageenan, fucoidan and seaweed-based biostimulants. "
            "Located in Qingdao, China's largest seaweed processing hub. Serves food, "
            "agriculture and cosmetics industries globally."
        ),
        "tech_areas": "Algae\nEnzymatic catalysis\nDownstream processing",
        "technologies": (
            "Seaweed biomass extraction and processing\n"
            "Enzymatic depolymerisation of polysaccharides\n"
            "Alginate and carrageenan purification\n"
            "Spray drying and granulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "Key supplier to food ingredient and agricultural biostimulant markets globally.",
    },
    # ── Bioplastics ───────────────────────────────────────────────────────────
    {
        "id": 3027,
        "facility": "Bluepha Co. Ltd",
        "tier": "Pilot facility",
        "city": "Shanghai",
        "country": "China",
        "website": "https://www.bluepha.com",
        "about": (
            "Biotechnology startup pioneering continuous non-sterile PHA (polyhydroxyalkanoate) "
            "bioplastic production. Operates a pilot and small-scale commercial facility in "
            "Shanghai using a proprietary open continuous culture (OCC) platform, achieving "
            "significantly lower production costs than conventional batch PHA fermentation."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Open continuous fermentation (OCC process)\n"
            "Mixed microbial culture PHA accumulation\n"
            "PHA solvent extraction and purification\n"
            "Biopolymer compounding pilot line"
        ),
        "n_tech": 4,
        "certs": "",
        "extra": "Venture-backed by CITIC Capital and IDG. Targeting 10,000-tonne commercial scale. Pioneering non-sterile PHA fermentation.",
    },
    {
        "id": 3028,
        "facility": "Shenzhen Ecomann Biotechnology Co. Ltd",
        "tier": "Captive",
        "city": "Shenzhen",
        "country": "China",
        "website": "https://www.ecomann.com",
        "about": (
            "Pioneer in PHA bioplastic production in China, producing P(3HB-co-4HB) and "
            "P(3HB-co-3HHx) copolymers via Cupriavidus necator and Aeromonas hydrophila "
            "industrial fermentation. Supplies biodegradable packaging, agricultural film "
            "and specialty film markets. Annual capacity ~5,000 tonnes PHA."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Fed-batch PHA fermentation (Cupriavidus necator)\n"
            "PHA extraction by solvent and non-solvent methods\n"
            "Biopolymer compounding and film blowing\n"
            "Composting certification testing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nOK Compost certification",
        "extra": "Annual PHA capacity ~5,000 tonnes. Supplies global brands with certified compostable packaging.",
    },
    # ── Contract / specialty fermentation ────────────────────────────────────
    {
        "id": 3029,
        "facility": "Guangdong VTR Bio-Tech Co. Ltd",
        "tier": "Open CMO",
        "city": "Zhuhai",
        "country": "China",
        "website": "https://www.vtrbiotech.com",
        "about": (
            "Industrial microbiology contract manufacturer in Guangdong Province. Provides "
            "custom fermentation development and production for food ingredients, bio-pesticides, "
            "microbial fertilisers and specialty fermentation products. Works with international "
            "agrochemical and food ingredient companies on scale-up projects."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Submerged fermentation 1–200 m³\n"
            "Solid-state fermentation\n"
            "Downstream extraction and concentration\n"
            "Custom strain improvement services"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nGMP (agricultural biologicals)",
        "extra": "CMO services for industrial biotech, food and agrochemical sectors.",
    },
    # ── Research / pilot ──────────────────────────────────────────────────────
    {
        "id": 3030,
        "facility": "Tianjin Institute of Industrial Biotechnology (TIB), CAS",
        "tier": "Pilot facility",
        "city": "Tianjin",
        "country": "China",
        "website": "https://www.tib.cas.cn",
        "about": (
            "National research and pilot manufacturing institute under the Chinese Academy "
            "of Sciences (CAS). Focuses on metabolic engineering, synthetic biology and "
            "process scale-up of industrial biotechnology. Operates pilot fermentation suites "
            "for bio-based chemicals, food ingredients and specialty molecules. "
            "Key partner to industry for bench-to-pilot translation."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Pilot fermenters 1–1000 L\n"
            "Metabolic flux analysis and synthetic biology platform\n"
            "Downstream bioprocess piloting\n"
            "Strain engineering and directed evolution"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Part of CAS. Located in Tianjin Binhai Industrial Zone biotech cluster. Key institute for Chinese industrial biotech scale-up.",
    },
    {
        "id": 3031,
        "facility": "Jiangnan University – Nat. Engineering Research Center for Cereal Fermentation",
        "tier": "Pilot facility",
        "city": "Wuxi",
        "country": "China",
        "website": "https://www.jiangnan.edu.cn",
        "about": (
            "University-affiliated national research and pilot centre in Jiangsu Province "
            "dedicated to cereal fermentation and food ingredient biotechnology. Offers "
            "fermentation scale-up services, process development and microbial strain "
            "optimisation. China's leading academic fermentation science institution with "
            "strong industry partnerships (Angel Yeast, Meihua, etc.)."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nEnzymatic catalysis",
        "technologies": (
            "Pilot fermentation 1–500 L\n"
            "Fed-batch and continuous fermentation\n"
            "Cereal starch hydrolysis pilot\n"
            "Analytical metabolomics platform"
        ),
        "n_tech": 4,
        "certs": "",
        "extra": "Top-ranked Chinese university for fermentation science. National engineering research centre designation.",
    },
    {
        "id": 3032,
        "facility": "Shanghai Institute of Plant Physiology & Ecology (SIPPE), CAS",
        "tier": "Pilot facility",
        "city": "Shanghai",
        "country": "China",
        "website": "https://www.sippe.ac.cn",
        "about": (
            "Chinese Academy of Sciences institute with active industrial biotechnology "
            "programs. Conducts pilot-scale development of bio-based chemicals including "
            "itaconic acid, succinate and bio-based aromatics via metabolic engineering. "
            "Partner to industrial companies for process development and scale-up. "
            "Key expertise in lignocellulose bioconversion and synthetic biology."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Pilot fermentation suite 1–100 L\n"
            "Metabolic engineering and synthetic biology\n"
            "Fed-batch bioprocess development\n"
            "Lignocellulose pretreatment pilot"
        ),
        "n_tech": 4,
        "certs": "",
        "extra": "Part of Chinese Academy of Sciences. Strong collaborative network with industrial biotech companies.",
    },
    {
        "id": 3033,
        "facility": "Tereos Starch & Sweeteners China",
        "tier": "Captive",
        "city": "Nantong",
        "country": "China",
        "website": "https://www.tereos.com",
        "about": (
            "Chinese manufacturing operations of Tereos Group (France) producing corn starch, "
            "glucose, fructose and bioethanol in Jiangsu Province. Supplies food, fermentation "
            "and industrial markets in Eastern China. Part of Tereos Group, a global leader "
            "in sugar, starch and bioethanol."
        ),
        "tech_areas": "Fermentation (industrial)\nEnzymatic catalysis\nDownstream processing",
        "technologies": (
            "Corn wet milling\n"
            "Enzymatic saccharification\n"
            "HFCS (high-fructose corn syrup) production\n"
            "Bioethanol fermentation and distillation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000",
        "extra": "Part of Tereos Group. Nantong plant serves the Yangtze River Delta industrial cluster.",
    },
]

# ── Asia (non-China) facilities ───────────────────────────────────────────────

ASIA_FACILITIES = [
    # ── JAPAN ─────────────────────────────────────────────────────────────────
    {
        "id": 4001,
        "facility": "Ajinomoto Co. Inc. – Tokai Plant",
        "tier": "Captive",
        "city": "Tokai",
        "country": "Japan",
        "website": "https://www.ajinomoto.com",
        "about": (
            "Major production facility of Ajinomoto Co., the pioneer of amino acid "
            "fermentation, producing MSG, glutamic acid, nucleotides (IMP, GMP), lysine and "
            "threonine by microbial fermentation. The Tokai plant is one of Ajinomoto's core "
            "domestic amino acid manufacturing sites using sugarcane molasses and starch feedstocks."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Large-scale submerged amino acid fermentation\n"
            "Nucleotide production by microbial synthesis\n"
            "Ion exchange purification\n"
            "Crystallisation and spray drying"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nISO 22000\nFSSC 22000",
        "extra": "Ajinomoto operates 30+ production sites globally. Pioneer of industrial amino acid fermentation since 1956.",
    },
    {
        "id": 4002,
        "facility": "Kikkoman Corporation – Noda Brewery",
        "tier": "Captive",
        "city": "Noda",
        "country": "Japan",
        "website": "https://www.kikkoman.com",
        "about": (
            "World's largest soy sauce producer, operating the historic Noda brewery with "
            "continuous industrial-scale koji and moromi (soy sauce mash) fermentation. "
            "Also produces and markets industrial enzymes (amylases, proteases, cellulases) "
            "derived from fermentation as a commercial product line. Annual soy sauce "
            "production exceeds 300 million litres globally."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nEnzymatic catalysis",
        "technologies": (
            "Koji solid-state fermentation (Aspergillus oryzae)\n"
            "Moromi liquid fermentation in large tanks\n"
            "Industrial enzyme extraction and formulation\n"
            "Soy sauce pressing and pasteurisation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP\nFSSC 22000",
        "extra": "Founded 1917. Industrial enzymes division supplies food and biotech industries globally.",
    },
    {
        "id": 4003,
        "facility": "Amano Enzyme Inc.",
        "tier": "Open CMO",
        "city": "Nagoya",
        "country": "Japan",
        "website": "https://www.amano-enzyme.co.jp",
        "about": (
            "Leading Japanese industrial enzyme manufacturer producing over 100 enzyme "
            "products including lipases, proteases, amylases and cellulases from microbial "
            "fermentation. Supplies food processing, pharmaceutical excipient and industrial "
            "biotechnology markets globally. Offers custom enzyme development and contract "
            "manufacturing services."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Submerged and solid-state fungal fermentation\n"
            "Enzyme extraction, ultrafiltration and concentration\n"
            "Lyophilisation and spray drying\n"
            "Custom enzyme engineering services"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFDA GRAS",
        "extra": "Founded 1947. Exports to 50+ countries. One of Japan's largest enzyme CMOs. 100+ commercial enzyme products.",
    },
    {
        "id": 4004,
        "facility": "Kaneka Corporation – Takasago Plant",
        "tier": "Captive",
        "city": "Takasago",
        "country": "Japan",
        "website": "https://www.kaneka.co.jp",
        "about": (
            "Kaneka's Takasago facility produces Coenzyme Q10 (CoQ10) by microbial "
            "fermentation and manufactures PHBH (poly-3-hydroxybutyrate-co-3-hydroxyhexanoate) "
            "bioplastics under the Kaneka PHBH™ brand using Cupriavidus necator fermentation. "
            "Also produces astaxanthin and other fermentation-derived nutritional ingredients."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Aerobic submerged fermentation for CoQ10 (Rhizobium radiobacter)\n"
            "PHA bioplastic fermentation (C. necator / engineered strains)\n"
            "PHBH extraction and compounding\n"
            "Astaxanthin microalgae cultivation pilot"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFSSC 22000",
        "extra": "World's largest PHBH bioplastic producer. CoQ10 capacity among global top producers. Marine-biodegradable bioplastics for packaging.",
    },
    {
        "id": 4005,
        "facility": "Hayashibara Co. Ltd (Nagase Group)",
        "tier": "Captive",
        "city": "Okayama",
        "country": "Japan",
        "website": "https://www.hayashibara.co.jp",
        "about": (
            "Japanese biotechnology company and a global leader in trehalose production "
            "via enzymatic conversion of starch using a proprietary two-enzyme system. "
            "Also produces isomaltulose, branching enzyme products, and specialty "
            "oligosaccharides for food, cosmetics and industrial applications. "
            "Part of Nagase Group."
        ),
        "tech_areas": "Enzymatic catalysis\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "Two-enzyme trehalose synthesis (trehalose synthase pathway)\n"
            "Isomaltulose enzymatic conversion\n"
            "Starch branching enzyme application\n"
            "Chromatographic purification of specialty sugars"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "Holds key patents on enzymatic trehalose production. World's largest trehalose producer.",
    },
    {
        "id": 4006,
        "facility": "Shin Nihon Chemical Co. Ltd",
        "tier": "Open CMO",
        "city": "Anjo",
        "country": "Japan",
        "website": "https://www.snc.co.jp",
        "about": (
            "Established Japanese enzyme and biochemical manufacturer offering contract "
            "fermentation and enzyme production services. Produces proteases, lipases, "
            "amylases and specialty enzymes for food, pharmaceutical excipient and fine "
            "chemical applications. Provides custom enzyme development for global clients."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Submerged microbial fermentation\n"
            "Enzyme purification and concentration\n"
            "Lyophilisation and powder formulation\n"
            "Custom enzyme scale-up services"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Specialist contract enzyme manufacturer. Serves food, biotech and fine chemical sectors.",
    },
    {
        "id": 4007,
        "facility": "Mitsubishi Chemical Corporation – Bio-based Chemicals (Yokkaichi)",
        "tier": "Captive",
        "city": "Yokkaichi",
        "country": "Japan",
        "website": "https://www.m-chemical.co.jp",
        "about": (
            "Mitsubishi Chemical operates industrial fermentation for bio-based 1,4-butanediol "
            "(BDO) production using Genomatica's BioNylon technology. The Yokkaichi complex "
            "integrates fermentation with downstream chemical processing to produce bio-based "
            "BDO for bioplastics and polymer applications."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Anaerobic fermentation for bio-based 1,4-BDO (Genomatica platform)\n"
            "Downstream chemical purification and distillation\n"
            "Integration with polymer production"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001",
        "extra": "One of the first commercial-scale bio-based BDO producers. Partnership with Genomatica (USA).",
    },
    {
        "id": 4008,
        "facility": "National Agriculture and Food Research Org. (NARO) – Food Research Institute",
        "tier": "Pilot facility",
        "city": "Tsukuba",
        "country": "Japan",
        "website": "https://www.naro.go.jp",
        "about": (
            "Government food research institute providing pilot-scale biotechnology and "
            "fermentation services for food ingredient development, food safety and "
            "traditional fermented food modernisation. Supports Japanese food companies "
            "with scale-up from lab to pilot for fermented and enzyme-processed foods."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Food fermentation pilot 1–200 L\n"
            "Enzyme screening and development\n"
            "Traditional fermented food process analysis\n"
            "Koji fermentation characterisation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Government-funded national research institute. Publishes open-access fermentation research.",
    },
    # ── SOUTH KOREA ───────────────────────────────────────────────────────────
    {
        "id": 4009,
        "facility": "CJ CheilJedang Corporation – Bio Division (Incheon)",
        "tier": "Captive",
        "city": "Incheon",
        "country": "South Korea",
        "website": "https://www.cj.co.kr",
        "about": (
            "South Korea's largest industrial biotech company and a global top-3 amino acid "
            "producer. CJ's Bio Division manufactures lysine, tryptophan, threonine and "
            "methionine by microbial fermentation for animal feed globally. Also produces "
            "probiotics and fermentation-derived food ingredients. "
            "Annual amino acid capacity exceeds 1 million tonnes globally."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Large-scale lysine fermentation (Corynebacterium glutamicum)\n"
            "Fed-batch and continuous amino acid fermentation\n"
            "Ion exchange and membrane purification\n"
            "Spray drying and granulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nFAMI-QS\nHACCP",
        "extra": "World's largest lysine exporter. Bio Division production sites in Korea, USA, Brazil, Indonesia and China.",
    },
    {
        "id": 4010,
        "facility": "Daesang Corporation – Bio & Fermentation Division",
        "tier": "Captive",
        "city": "Gunsan",
        "country": "South Korea",
        "website": "https://www.daesang.com",
        "about": (
            "Major South Korean food and biotechnology group producing MSG, citric acid, "
            "amino acids, starch sweeteners and nucleotides by fermentation. The Gunsan "
            "plant is the main fermentation site, processing corn starch into a range of "
            "food-grade organic acids, amino acids and specialty ingredients."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Submerged fermentation for glutamic acid and citric acid\n"
            "Nucleotide production by microbial synthesis\n"
            "Ion exchange purification and crystallisation\n"
            "Corn wet milling and glucose production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "Revenue ~KRW 3 trillion. Also a major Korean traditional food manufacturer (kimchi, sauces).",
    },
    {
        "id": 4011,
        "facility": "Amicogen Inc.",
        "tier": "Open CMO",
        "city": "Jinju",
        "country": "South Korea",
        "website": "https://www.amicogen.com",
        "about": (
            "South Korean industrial enzyme and bioconversion specialist offering contract "
            "manufacturing of industrial enzymes, specialty biochemicals and fermentation "
            "products. Focuses on lipases, proteases and custom enzyme development for food, "
            "feed and industrial applications. Also produces hyaluronic acid by microbial "
            "fermentation for the cosmetics and food industries."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Submerged enzyme fermentation\n"
            "Hyaluronic acid fermentation (Streptococcus equi)\n"
            "Enzyme purification and liquid/powder formulation\n"
            "Custom bioconversion process development"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000",
        "extra": "Listed on KOSDAQ. Key supplier of HA to cosmetics sector. Strong enzyme IP portfolio.",
    },
    {
        "id": 4012,
        "facility": "Korea Research Institute of Bioscience & Biotechnology (KRIBB)",
        "tier": "Pilot facility",
        "city": "Daejeon",
        "country": "South Korea",
        "website": "https://www.kribb.re.kr",
        "about": (
            "Government-funded research institute providing pilot-scale fermentation and "
            "bioprocess development for industrial biotechnology. Operates pilot suites for "
            "bio-based chemicals, food ingredients, industrial enzymes and microbial platform "
            "chemicals. Key partner for Korean biotech companies seeking scale-up support."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Pilot fermentation 1–500 L\n"
            "Metabolic engineering platform\n"
            "Enzyme discovery and engineering\n"
            "Downstream process development"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Government research institute under Ministry of Science. Key industrial biotech scale-up partner in Korea.",
    },
    {
        "id": 4013,
        "facility": "Samyang Holdings – Bio & Chemical Division",
        "tier": "Captive",
        "city": "Seoul",
        "country": "South Korea",
        "website": "https://www.samyang.com",
        "about": (
            "South Korean industrial group with a significant fermentation and bio-based "
            "chemicals division. Produces bioplastics (PBS, PBSA), specialty sugars, "
            "food ingredients and bio-based monomers. Also manufactures isomalt and "
            "isomaltulose for the food sector. One of Korea's pioneers in bio-based "
            "chemical production."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Enzymatic isomaltulose and isomalt production\n"
            "Bio-based succinate fermentation pilot\n"
            "PBS/PBSA bioplastic production\n"
            "Specialty sugar purification"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000",
        "extra": "Revenue ~KRW 2 trillion. Pioneer in bio-based PBS bioplastics in Korea.",
    },
    # ── INDIA ─────────────────────────────────────────────────────────────────
    {
        "id": 4014,
        "facility": "Advanced Enzymes Technologies Ltd",
        "tier": "Open CMO",
        "city": "Thane",
        "country": "India",
        "website": "https://www.advancedenzymes.com",
        "about": (
            "India's largest industrial enzyme manufacturer and a global top-10 enzyme "
            "company. Produces 400+ enzyme products for human nutrition, food processing, "
            "animal feed and industrial applications from 8 manufacturing facilities. "
            "Offers custom enzyme development and contract fermentation. "
            "Serves 700+ clients in 50+ countries."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Submerged and solid-state microbial fermentation\n"
            "Enzyme concentration, ultrafiltration and formulation\n"
            "Custom strain development and scale-up\n"
            "Lyophilisation and granular enzyme production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nFDA registration\nHalal\nKosher",
        "extra": "Listed on BSE and NSE. Revenue ~INR 5 billion. India's leading enzyme exporter.",
    },
    {
        "id": 4015,
        "facility": "Praj Industries Ltd – BioEnergy Division",
        "tier": "Open CMO",
        "city": "Pune",
        "country": "India",
        "website": "https://www.praj.net",
        "about": (
            "Leading Indian bioprocess engineering company and industrial biotech technology "
            "provider. Operates a pilot plant (Praj Matrix R&D centre) in Pune for process "
            "development of bioethanol (1G and 2G), biochemicals and bio-based materials. "
            "Provides engineering, procurement and construction (EPC) for biorefineries "
            "worldwide. Also offers pilot fermentation services for novel bio-products."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "1G and 2G lignocellulosic bioethanol pilot\n"
            "Molecular sieve ethanol dehydration\n"
            "Biogas upgrading (biomethane)\n"
            "Lactic acid and succinic acid fermentation pilot"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "700+ biorefinery installations worldwide. Praj Matrix R&D centre: India's most advanced industrial biotech pilot facility.",
    },
    {
        "id": 4016,
        "facility": "Godavari Biorefineries Ltd",
        "tier": "Captive",
        "city": "Solapur",
        "country": "India",
        "website": "https://www.godavaribiorefineries.com",
        "about": (
            "India's largest integrated sugarcane biorefinery, producing fuel ethanol, "
            "industrial ethanol, bio-based ethyl acetate and nutraceuticals from sugarcane "
            "in Maharashtra. Operates multiple plants with a combined capacity of "
            "~400 million litres of ethanol per year. Pioneer in bio-based solvent production."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Continuous molasses and juice ethanol fermentation\n"
            "Molecular sieve dehydration\n"
            "Ethyl acetate production from bio-ethanol\n"
            "Vinasse biogas and biofertiliser recovery"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nISO 22000",
        "extra": "Annual ethanol capacity ~400 million litres. India's largest bio-based solvent producer.",
    },
    {
        "id": 4017,
        "facility": "CSIR – National Chemical Laboratory (NCL), Industrial Biotech Division",
        "tier": "Pilot facility",
        "city": "Pune",
        "country": "India",
        "website": "https://www.ncl.res.in",
        "about": (
            "Government research laboratory under CSIR with significant industrial biotech "
            "programs. Conducts pilot-scale process development for bio-based chemicals, "
            "enzymatic processes and fermentation products. Key expertise in biocatalysis, "
            "metabolic engineering and bioprocess scale-up. Provides technology transfer "
            "to Indian industry."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Pilot fermentation 1–200 L\n"
            "Biocatalysis and enzyme process development\n"
            "Metabolic engineering tools\n"
            "Bioprocess scale-up consultancy"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Part of CSIR network. Strong industry-linkage programmes. Hosts the CSIR800 technology transfer initiative.",
    },
    {
        "id": 4018,
        "facility": "ICAR – Central Food Technological Research Institute (CFTRI)",
        "tier": "Pilot facility",
        "city": "Mysuru",
        "country": "India",
        "website": "https://www.cftri.res.in",
        "about": (
            "India's premier food science research institute under ICAR. Operates "
            "pilot-scale facilities for fermented food technology, food enzymes, single-cell "
            "protein, probiotic cultures and traditional fermented food modernisation. "
            "Provides technology transfer and scale-up support to food and fermentation "
            "companies across India."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nProbiotics & cultures",
        "technologies": (
            "Food fermentation pilot (idli, dosa, yogurt, fermented beverages)\n"
            "Food enzyme screening and production pilot\n"
            "Single-cell protein fermentation\n"
            "Probiotic culture development"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Government institute under ICAR/DARES. Key partner for Indian food industry scale-up and technology transfer.",
    },
    # ── SINGAPORE ─────────────────────────────────────────────────────────────
    {
        "id": 4019,
        "facility": "A*STAR – Singapore Institute of Food and Biotechnology Innovation (SIFBI)",
        "tier": "Pilot facility",
        "city": "Singapore",
        "country": "Singapore",
        "website": "https://www.a-star.edu.sg",
        "about": (
            "Singapore government research institute under A*STAR focusing on food "
            "biotechnology and industrial bioprocessing. Operates pilot fermentation "
            "and bioprocess facilities for food ingredient development, precision "
            "fermentation and alternative protein scale-up. Key hub for Singapore's "
            "food manufacturing innovation ecosystem."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Pilot fermentation 1–100 L\n"
            "Precision fermentation for food proteins\n"
            "Enzyme discovery and food bioprocessing\n"
            "Downstream processing pilot"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Government-funded. Collaborates with global food companies on Singapore Food Story initiatives.",
    },
    {
        "id": 4020,
        "facility": "TurtleTree Ltd",
        "tier": "Pilot facility",
        "city": "Singapore",
        "country": "Singapore",
        "website": "https://www.turtletree.com",
        "about": (
            "Singapore-based food biotech startup pioneering precision fermentation for "
            "dairy proteins, specifically lactoferrin, produced without animals. Operates "
            "a pilot production facility in Singapore and is scaling towards commercial "
            "production for functional food and infant formula markets."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Precision fermentation for lactoferrin (yeast expression system)\n"
            "Protein purification and concentration\n"
            "Food-grade formulation development"
        ),
        "n_tech": 3,
        "certs": "",
        "extra": "Venture-backed startup. Singapore Food Agency regulatory engagement. Targets infant formula and sports nutrition markets.",
    },
    # ── THAILAND ──────────────────────────────────────────────────────────────
    {
        "id": 4021,
        "facility": "PTT Global Chemical (PTTGC) – BioPBS Plant",
        "tier": "Captive",
        "city": "Rayong",
        "country": "Thailand",
        "website": "https://www.pttgc.com",
        "about": (
            "PTTGC's Map Ta Phut complex in Rayong houses Thailand's first commercial "
            "bioplastic plant, producing BioPBS (polybutylene succinate) and bio-based "
            "chemicals including bio-succinic acid. Also develops bio-based monomers and "
            "specialty biochemicals. Part of Thailand's national bioeconomy strategy."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Bio-succinic acid fermentation pilot\n"
            "PBS bioplastic polymerisation\n"
            "Bio-based monomer production\n"
            "Downstream chemical purification"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nOK Compost",
        "extra": "Part of PTT Group (Thailand's national oil company). Key player in Thailand's S-Curve bioeconomy policy.",
    },
    {
        "id": 4022,
        "facility": "KTIS Group – Kaset Thai International Sugar Corp.",
        "tier": "Captive",
        "city": "Nakhon Sawan",
        "country": "Thailand",
        "website": "https://www.ktisgroup.com",
        "about": (
            "Thailand's largest integrated sugarcane processing group producing sugar, "
            "bioethanol, electricity and biofertiliser. The biorefinery complex in Nakhon "
            "Sawan operates large-scale molasses and juice ethanol fermentation alongside "
            "the sugar factory. One of Southeast Asia's largest agri-biorefinery complexes."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Continuous sugarcane ethanol fermentation\n"
            "Molecular sieve dehydration\n"
            "Vinasse biogas recovery\n"
            "Biofertiliser production from stillage"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nRSPO",
        "extra": "Annual ethanol capacity ~500,000 kL. Integrated sugarcane-to-ethanol-to-electricity biorefinery model.",
    },
    {
        "id": 4023,
        "facility": "National Science and Technology Development Agency (NSTDA) – IVL",
        "tier": "Pilot facility",
        "city": "Pathum Thani",
        "country": "Thailand",
        "website": "https://www.nstda.or.th",
        "about": (
            "Thailand's main government science and technology research agency, operating "
            "pilot bioprocess facilities for food and industrial biotechnology. The Industrial "
            "Biotechnology Pilot Plant (IBP) at the Thailand Science Park supports fermentation "
            "scale-up for food ingredients, enzymes, biopolymers and bio-based chemicals for "
            "Thai industry."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Pilot fermentation 1–500 L\n"
            "Industrial enzyme development\n"
            "Biopolymer fermentation pilot\n"
            "Downstream process development"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Government agency. Thailand Science Park biotech cluster. Key industrial biotech pilot facility in SE Asia.",
    },
    # ── INDONESIA ─────────────────────────────────────────────────────────────
    {
        "id": 4024,
        "facility": "PT Indo Acidatama Tbk",
        "tier": "Captive",
        "city": "Karanganyar",
        "country": "Indonesia",
        "website": "https://www.indoacidatama.co.id",
        "about": (
            "Indonesia's largest bioethanol and acetic acid producer, operating a molasses "
            "fermentation complex in Central Java. Produces fuel ethanol, industrial ethanol "
            "and acetic acid from sugarcane molasses feedstock. Listed on the Indonesian "
            "Stock Exchange. One of Southeast Asia's largest standalone fermentation facilities."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Molasses ethanol fermentation (continuous)\n"
            "Acetic acid oxidative fermentation (Acetobacter)\n"
            "Distillation and rectification\n"
            "Acetic acid concentration and purification"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "Listed on IDX. Annual ethanol capacity ~100,000 kL. Key Indonesian bioethanol supplier.",
    },
    # ── TAIWAN ────────────────────────────────────────────────────────────────
    {
        "id": 4025,
        "facility": "Industrial Technology Research Institute (ITRI) – Biomedical & Food Division",
        "tier": "Pilot facility",
        "city": "Hsinchu",
        "country": "Taiwan",
        "website": "https://www.itri.org.tw",
        "about": (
            "Taiwan's leading applied research institute operating pilot bioprocess facilities "
            "for industrial biotechnology, food ingredients and bio-based materials. ITRI's "
            "biotechnology and pharmaceutical division runs fermentation scale-up services "
            "for Taiwanese industry, including enzyme production, food protein fermentation "
            "and specialty ingredient development."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Pilot fermentation 1–300 L\n"
            "Food enzyme and probiotic development\n"
            "Bio-based material fermentation\n"
            "Downstream process pilot"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Government-backed applied research. Key scale-up partner for Taiwanese food and industrial biotech companies.",
    },
    {
        "id": 4026,
        "facility": "Taiwan Sugar Corporation (Taishin) – Bioethanol Division",
        "tier": "Captive",
        "city": "Tainan",
        "country": "Taiwan",
        "website": "https://www.taisugar.com.tw",
        "about": (
            "State-owned corporation operating large-scale food fermentation and bioethanol "
            "production from sugarcane in southern Taiwan. Produces bioethanol for blended "
            "fuel and industrial use, as well as traditional fermented foods including "
            "vinegar and soy sauce. Also operates mushroom and yeast fermentation operations."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Sugarcane juice and molasses ethanol fermentation\n"
            "Continuous distillation\n"
            "Traditional food fermentation (vinegar, soy sauce)\n"
            "Edible mushroom cultivation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "State-owned enterprise. Annual bioethanol capacity ~50 million litres. Also operates premium fermented food brands.",
    },
    # ── MALAYSIA ──────────────────────────────────────────────────────────────
    {
        "id": 4027,
        "facility": "Malaysian Biotechnology Corporation (BiotechCorp) – Pilot Plant",
        "tier": "Pilot facility",
        "city": "Kuala Lumpur",
        "country": "Malaysia",
        "website": "https://www.biotechcorp.com.my",
        "about": (
            "Malaysia's national biotech development agency operating a shared pilot "
            "bioprocessing facility for industrial and food biotechnology companies. "
            "The pilot plant supports Malaysian biotech SMEs with scale-up of fermentation "
            "processes for food ingredients, enzymes, biopolymers and nutraceuticals. "
            "Part of the BioNexus partner ecosystem."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Shared pilot fermentation 1–200 L\n"
            "Downstream processing pilot (filtration, chromatography)\n"
            "Food bioprocess scale-up services"
        ),
        "n_tech": 3,
        "certs": "ISO 9001",
        "extra": "Government agency. BioNexus partner programme. Key support for Malaysian biotech SMEs.",
    },
]

# ── Excel writer ──────────────────────────────────────────────────────────────

def row_from_entry(entry: dict) -> dict:
    certs = entry.get("certs", "")
    return {
        "ID": entry["id"],
        "Facility": entry["facility"],
        "Membership tier": entry["tier"],
        "City": entry["city"],
        "Country": entry["country"],
        "Address": entry.get("address", ""),
        "Contact person": "",
        "Website": entry.get("website", ""),
        "Social links": "",
        "About": entry.get("about", ""),
        "Technology areas": entry.get("tech_areas", ""),
        "Technologies": entry.get("technologies", ""),
        "No. of technologies": entry.get("n_tech", ""),
        "Certifications": certs,
        "Non-technical services": entry.get("non_tech", ""),
        "Open 24/7": "",
        "Extra information": entry.get("extra", ""),
        "Downloads": "",
        "Videos": "",
        "Logo": "",
        "Pilots4U page": "",
    }


TIER_FILLS = {
    "Open CMO":       PatternFill(start_color="E3F2FD", end_color="E3F2FD", fill_type="solid"),
    "Captive":        PatternFill(start_color="FFF8E1", end_color="FFF8E1", fill_type="solid"),
    "Pilot facility": PatternFill(start_color="F3E5F5", end_color="F3E5F5", fill_type="solid"),
}
ALT_FILL    = PatternFill(start_color="F0FAF5", end_color="F0FAF5", fill_type="solid")
HEADER_FILL = PatternFill(start_color="1B4332", end_color="1B4332", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)
COL_WIDTHS = {
    "ID": 6, "Facility": 45, "Membership tier": 16,
    "City": 20, "Country": 14, "Address": 28,
    "Contact person": 20, "Website": 36, "Social links": 18,
    "About": 60, "Technology areas": 30, "Technologies": 45,
    "No. of technologies": 9, "Certifications": 26,
    "Non-technical services": 28, "Open 24/7": 9,
    "Extra information": 50, "Downloads": 10, "Videos": 10,
    "Logo": 28, "Pilots4U page": 18,
}


def make_workbook(facilities: list, label: str) -> openpyxl.Workbook:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facilities"

    # Header
    for ci, col in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=ci, value=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[1].height = 30

    # Rows
    for ri, entry in enumerate(facilities, 2):
        row_data = row_from_entry(entry)
        tier = row_data["Membership tier"]
        fill = TIER_FILLS.get(tier, ALT_FILL if ri % 2 == 0 else PatternFill())
        for ci, col in enumerate(COLUMNS, 1):
            cell = ws.cell(row=ri, column=ci, value=row_data.get(col, ""))
            cell.fill = fill
            cell.border = THIN_BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True, horizontal="left")

    # Column widths
    from openpyxl.utils import get_column_letter
    for ci, col in enumerate(COLUMNS, 1):
        ws.column_dimensions[get_column_letter(ci)].width = COL_WIDTHS.get(col, 18)

    ws.freeze_panes = "A2"

    # Notes sheet
    ws2 = wb.create_sheet("Notes")
    ws2["A1"] = f"{label} Industrial Biotech & Food Biomanufacturing Database"
    ws2["A1"].font = Font(bold=True, size=14)
    ws2["A3"] = f"Total facilities: {len(facilities)}"
    ws2["A4"] = "Scope: Industrial fermentation, food biotechnology, industrial enzymes, biofuels, biopolymers, algae — NO PHARMA"

    from collections import Counter
    tier_counts = Counter(e["tier"] for e in facilities)
    ws2["A6"] = "By type:"
    ws2["A6"].font = Font(bold=True)
    for i, (tier, count) in enumerate(sorted(tier_counts.items()), 7):
        ws2.cell(i, 1, f"  {tier}: {count}")

    country_counts = Counter(e["country"] for e in facilities)
    row_n = 7 + len(tier_counts) + 1
    ws2.cell(row_n, 1, "By country:").font = Font(bold=True)
    for country, count in country_counts.most_common():
        row_n += 1
        ws2.cell(row_n, 1, f"  {country}: {count}")

    ws2.column_dimensions["A"].width = 80
    return wb


if __name__ == "__main__":
    china_wb = make_workbook(CHINA_FACILITIES, "China")
    china_path = DATA_DIR / "China_biomanufacturing_database.xlsx"
    china_wb.save(china_path)
    print(f"Saved China database → {china_path}  ({len(CHINA_FACILITIES)} facilities)")

    asia_wb = make_workbook(ASIA_FACILITIES, "Asia")
    asia_path = DATA_DIR / "Asia_biomanufacturing_database.xlsx"
    asia_wb.save(asia_path)
    print(f"Saved Asia database  → {asia_path}  ({len(ASIA_FACILITIES)} facilities)")
