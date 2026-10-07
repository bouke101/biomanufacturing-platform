"""
Batch 1: IFF N&B, Evonik Nutrition, Kerry Group, Cargill, ADM fermentation sites.
IDs 6001–6035. Excludes entries already in database:
  - IFF Shanghai (already in DB)
  - ADM Decatur (already in DB)
  - Cargill Blair general fermentation (already in DB)
  - Evonik Hanau (already in DB; discontinued end-2025)
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
]

FACILITIES = [
    # ══════════════════════════════════════════════════════════════════════════
    # IFF — Nutrition & Biosciences
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 6001,
        "facility": "IFF – Grindsted Production",
        "tier": "Captive",
        "city": "Grindsted",
        "country": "Denmark",
        "website": "https://www.iff.com",
        "about": (
            "World's largest carbon-neutral food emulsifier manufacturing plant, celebrating "
            "its 100th anniversary in August 2024 and currently undergoing capacity expansion. "
            "Produces GRINDSTED® brand emulsifiers (mono- and diglycerides, lecithins, DATEM, "
            "SSL), hydrocolloids (pectin, carrageenan, locust bean gum), specialty lipids and "
            "texture systems for global food and beverage manufacturers. IFF employs 1,000+ "
            "staff across its four Danish sites."
        ),
        "tech_areas": "Enzymatic catalysis\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Enzymatic interesterification for emulsifier production\n"
            "Pectin extraction and purification\n"
            "Hydrocolloid processing and blending\n"
            "Lipid modification and encapsulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
        "extra": "100-year anniversary 2024. Carbon-neutral manufacturing. Currently expanding capacity. World's largest emulsifier site.",
    },
    {
        "id": 6002,
        "facility": "IFF – Haderslev Production",
        "tier": "Captive",
        "city": "Haderslev",
        "country": "Denmark",
        "website": "https://www.iff.com",
        "about": (
            "IFF food ingredient manufacturing site in southern Jutland, Denmark, producing "
            "hydrocolloids, texture systems and specialty food ingredients. Part of IFF's "
            "Danish manufacturing network (alongside Grindsted, Brabrand) serving the "
            "global food and beverage industry. The site specialises in carrageenan and "
            "pectin-based texturisers for dairy, confectionery and processed food applications."
        ),
        "tech_areas": "Enzymatic catalysis\nDownstream processing",
        "technologies": (
            "Hydrocolloid extraction and purification\n"
            "Carrageenan and pectin processing\n"
            "Texture system blending and standardisation"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "Part of IFF's 4-site Danish manufacturing network. Supplies hydrocolloids to global food industry.",
    },
    {
        "id": 6003,
        "facility": "IFF – Brabrand Innovation & Pilot Campus",
        "tier": "Pilot facility",
        "city": "Brabrand",
        "country": "Denmark",
        "website": "https://www.iff.com",
        "about": (
            "IFF's largest European R&D and innovation centre near Aarhus, Denmark, with "
            "400+ staff including food scientists, fermentation specialists and application "
            "engineers. Houses pilot-scale fermentation and bioprocessing facilities for "
            "dairy, bakery, culinary and plant-based food applications. Co-creation hub "
            "for customers developing next-generation fermented food ingredients, cultures "
            "and enzyme applications at pilot scale before commercial transfer."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nProbiotics & cultures",
        "technologies": (
            "Pilot fermentation for food cultures and enzymes (1–500 L)\n"
            "Dairy and plant-based application testing\n"
            "Sensory evaluation and consumer research labs\n"
            "Bakery and culinary fermentation pilots"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000",
        "extra": "400+ R&D staff. IFF's largest European innovation centre. Customer co-creation for fermented food ingredients.",
    },
    {
        "id": 6004,
        "facility": "IFF – Kantvik Enzyme Production",
        "tier": "Captive",
        "city": "Kantvik",
        "country": "Finland",
        "website": "https://www.iff.com",
        "about": (
            "Industrial enzyme manufacturing facility in Kantvik (Kirkkonummi), Finland, "
            "operating since 1974 with roots in Finn Sugar / Cultor / Genencor heritage. "
            "Produces enzymes for animal nutrition (ruminant, monogastric), food processing "
            "and specialty applications by submerged microbial fermentation. Part of IFF's "
            "global enzyme production network under the Nutrition & Biosciences division."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Submerged microbial fermentation for enzyme production\n"
            "Enzyme concentration and formulation\n"
            "Animal nutrition enzyme blending"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "Operating since 1974 (Finn Sugar → Cultor → Genencor → DuPont → IFF heritage). Key enzyme site for IFF N&B animal nutrition.",
    },
    {
        "id": 6005,
        "facility": "IFF – Cedar Rapids Enzyme Production",
        "tier": "Captive",
        "city": "Cedar Rapids",
        "country": "United States",
        "website": "https://www.iff.com",
        "about": (
            "IFF's primary North American enzyme manufacturing facility in Cedar Rapids, "
            "Iowa, with 200+ employees. Produces industrial enzymes for food & beverage, "
            "household care, animal nutrition and biofuel applications. A $70 million, "
            "47,000 sq ft expansion is underway, expected operational in late 2026, "
            "significantly increasing capacity for the North American enzyme market. "
            "Genencor heritage site (acquired by DuPont 2011, then IFF 2021)."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Submerged enzyme fermentation\n"
            "Enzyme downstream processing and formulation\n"
            "Liquid and granular enzyme products for food, biofuel, household"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001\nFSSC 22000",
        "extra": "$70M / 47,000 sq ft expansion underway, operational late 2026. 200+ employees. Genencor → DuPont → IFF heritage.",
    },
    {
        "id": 6006,
        "facility": "IFF – Dangé-Saint-Romain Probiotic & Culture Production",
        "tier": "Captive",
        "city": "Dangé-Saint-Romain",
        "country": "France",
        "website": "https://www.iff.com",
        "about": (
            "IFF's probiotic and starter culture production facility in the Vienne "
            "department of France. Achieved the world's first industrial-scale anaerobic "
            "fermentation of next-generation probiotic Akkermansia muciniphila in 2023. "
            "Also produces plant-based fermentation starter cultures for cheese, yogurt "
            "and plant-based dairy analogues. Expanding plant-based starter culture capacity "
            "to meet growing demand."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures",
        "technologies": (
            "Anaerobic probiotic fermentation (Akkermansia muciniphila — world first at industrial scale)\n"
            "Lactic acid bacteria starter culture fermentation\n"
            "Plant-based fermentation culture production\n"
            "Freeze-drying and spray-drying of cultures"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "World's first industrial-scale Akkermansia probiotic fermentation (2023). Expanding plant-based culture capacity.",
    },
    {
        "id": 6007,
        "facility": "IFF – Rochester Enzyme R&D & Pilot (Genencor Heritage)",
        "tier": "Pilot facility",
        "city": "Rochester",
        "country": "United States",
        "website": "https://www.iff.com",
        "about": (
            "IFF enzyme R&D and pilot fermentation facility in Rochester, New York, built "
            "on the Genencor International legacy (founded 1982 as Genentech/Corning JV). "
            "Houses protein engineering, directed evolution, enzyme screening and pilot-scale "
            "fermentation. Some cGMP-like pilot production of specialty enzymes. A historic "
            "hub for industrial enzyme innovation that has produced landmark technologies "
            "including cellulases, lipases and proteases used across dozens of industries."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Directed evolution and protein engineering for enzymes\n"
            "High-throughput enzyme screening\n"
            "Pilot fermentation 1–200 L\n"
            "Specialty enzyme pilot production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001",
        "extra": "Genencor heritage (1982). Historic centre of industrial enzyme innovation. Founded as Genentech/Corning JV, then Genencor → DuPont → IFF.",
    },
    {
        "id": 6008,
        "facility": "IFF – Arroyito Enzyme Production (Latin America Hub)",
        "tier": "Captive",
        "city": "Arroyito",
        "country": "Argentina",
        "website": "https://www.iff.com",
        "about": (
            "IFF's emerging Latin American enzyme production hub in Córdoba Province, "
            "Argentina. An announced March 2026 upgrade is converting the Arroyito facility "
            "from a packaging and finishing operation to a full-cycle fermentation-based "
            "enzyme production site — the first complete enzyme production capability "
            "in Latin America for IFF. Will serve food, feed and industrial enzyme "
            "customers across South America, reducing import dependency."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Submerged enzyme fermentation (new full-cycle capability from 2026)\n"
            "Enzyme formulation and packaging\n"
            "Application labs for food and feed enzymes"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000",
        "extra": "Upgrade to full fermentation announced March 2026. First full-cycle enzyme production in Latin America for IFF.",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Evonik — Nutrition & Care
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 6009,
        "facility": "Evonik Mobile – MetAMINO® Plant",
        "tier": "Captive",
        "city": "Mobile",
        "country": "United States",
        "website": "https://www.evonik.com",
        "about": (
            "Evonik's world-scale DL-methionine (MetAMINO®) manufacturing complex in "
            "Theodore, Alabama (Mobile area). Produces methionine for poultry, swine and "
            "aquaculture feed globally. A $176.5 million expansion completed in 2022 "
            "increased capacity, and backward integration (methyl mercaptan plant) was "
            "completed in July 2026. Also produces Mepron® (rumen-protected methionine "
            "for dairy cattle). One of three global Evonik methionine production sites."
        ),
        "tech_areas": "Fermentation (industrial)\nDownstream processing",
        "technologies": (
            "Strecker synthesis for DL-methionine\n"
            "Methyl mercaptan production (backward integration, 2026)\n"
            "Mepron® rumen-protected methionine coating\n"
            "Feed-grade amino acid granulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "$176.5M expansion 2022. Methyl mercaptan backward integration completed July 2026. Produces MetAMINO® and Mepron®. One of 3 global Evonik methionine sites.",
    },
    {
        "id": 6010,
        "facility": "Evonik Antwerp – Methionine Verbund",
        "tier": "Captive",
        "city": "Antwerp",
        "country": "Belgium",
        "website": "https://www.evonik.com",
        "about": (
            "Evonik's European DL-methionine production site in Antwerp, part of the "
            "integrated Antwerp-Wesseling methionine Verbund operating since 1974 (50 years "
            "in 2024). Produces MetAMINO® for European and global animal feed markets. "
            "The Antwerp/Wesseling Verbund underwent technical upgrades in 2025 "
            "(partial planned shutdown May–July 2025 for modernisation). "
            "One of Evonik's three global methionine hubs alongside Mobile (USA) and "
            "Singapore."
        ),
        "tech_areas": "Fermentation (industrial)\nDownstream processing",
        "technologies": (
            "Strecker synthesis for DL-methionine\n"
            "Integrated Verbund process with Wesseling\n"
            "Feed-grade amino acid granulation and packaging"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "50-year history (1974–2024). Part of Antwerp-Wesseling methionine Verbund. Modernisation upgrade 2025.",
    },
    {
        "id": 6011,
        "facility": "Evonik Wesseling – Methionine Verbund",
        "tier": "Captive",
        "city": "Wesseling",
        "country": "Germany",
        "website": "https://www.evonik.com",
        "about": (
            "Evonik's German methionine intermediate and precursor production site near "
            "Cologne, integrated with the Antwerp facility in the Antwerp-Wesseling "
            "methionine Verbund. Produces key methionine chemical intermediates and "
            "supports the overall European MetAMINO® supply chain. Part of the 2025 "
            "technical upgrade programme for the European Verbund."
        ),
        "tech_areas": "Fermentation (industrial)\nDownstream processing",
        "technologies": (
            "Methionine precursor and intermediate chemistry\n"
            "Integrated Verbund process with Antwerp\n"
            "Industrial chemical synthesis for amino acid production"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001",
        "extra": "Part of the Antwerp-Wesseling methionine Verbund. Produces intermediates for MetAMINO® supply chain.",
    },
    {
        "id": 6012,
        "facility": "Evonik Singapore – MetAMINO® Campus (Jurong Island)",
        "tier": "Captive",
        "city": "Singapore",
        "country": "Singapore",
        "website": "https://www.evonik.com",
        "about": (
            "Evonik's largest and most modern methionine complex on Jurong Island, "
            "Singapore, and the world's largest single methionine site. Two plants opened "
            "in 2014 and 2019 were expanded in 2024, bringing total MetAMINO® capacity "
            "to approximately 340,000 tonnes per year — over 40% of global methionine "
            "supply. Strategic Asian location serves rapidly growing aquaculture and "
            "poultry feed markets across Asia-Pacific. ~1,000 employees at the campus."
        ),
        "tech_areas": "Fermentation (industrial)\nDownstream processing",
        "technologies": (
            "World-scale Strecker synthesis for DL-methionine\n"
            "Two-plant campus (2014 + 2019) with 2024 expansion\n"
            "Feed-grade granulation and liquid methionine formulation\n"
            "MHA (methionine hydroxy analogue) production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nISO 45001\nFAMI-QS",
        "extra": "~340,000 t/yr capacity post-2024 expansion. >40% global methionine market share. World's largest single methionine complex. Located on Jurong Island.",
    },
    {
        "id": 6013,
        "facility": "Evonik Fermas – Slovenská Ľupča",
        "tier": "Captive",
        "city": "Slovenská Ľupča",
        "country": "Slovakia",
        "website": "https://www.evonik.com",
        "about": (
            "Evonik Fermas s.r.o. in Slovenská Ľupča, Slovakia — Evonik's dedicated "
            "fermentation amino acid production facility, founded 1992. Produces specialty "
            "fermentation-derived amino acids for animal nutrition and industrial applications. "
            "A €80 million expansion (groundbreaking September 2026, completion 2028) will "
            "add significant new downstream fermentation capacity, creating ~50 new jobs. "
            "One of Central Europe's key industrial fermentation sites."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Submerged amino acid fermentation\n"
            "Fed-batch microbial fermentation processes\n"
            "Downstream amino acid purification and drying\n"
            "Animal nutrition amino acid formulation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nFAMI-QS",
        "extra": "Founded 1992. €80M expansion 2026–2028 adding downstream fermentation capacity. ~50 new jobs. Key Central European fermentation site.",
    },
    {
        "id": 6014,
        "facility": "Evonik REXIM – Ham",
        "tier": "Captive",
        "city": "Ham",
        "country": "France",
        "website": "https://www.evonik.com",
        "about": (
            "Evonik REXIM's specialty fermentation amino acid and keto acid production "
            "facility in Ham, Somme, France. Produces pharmaceutical and nutraceutical-grade "
            "amino acids (including L-amino acids), keto acids and specialty fermentation "
            "products by microbial fermentation. One of two remaining REXIM keto acid "
            "production sites after the 2025 closure of the Hanau (Germany) plant, with "
            "production consolidated between Ham and Wuming (China)."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Fermentation-derived L-amino acid production\n"
            "Keto acid synthesis and purification\n"
            "High-purity amino acid crystallisation\n"
            "Pharmaceutical and nutraceutical grade processing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nGMP (nutraceutical grade)",
        "extra": "One of two REXIM keto/pharma amino acid sites post-Hanau closure (2025). Produces specialty fermentation amino acids for nutraceutical and pharmaceutical markets.",
    },
    {
        "id": 6015,
        "facility": "Evonik REXIM – Wuming",
        "tier": "Captive",
        "city": "Wuming",
        "country": "China",
        "website": "https://www.evonik.com",
        "about": (
            "Evonik REXIM's Chinese fermentation amino acid production facility in Wuming "
            "District, Nanning, Guangxi. Produces pharmaceutical and nutraceutical-grade "
            "amino acids and keto acids by microbial fermentation, serving Asian markets. "
            "Together with Ham (France), constitutes the two-site REXIM network following "
            "consolidation from Hanau (Germany). Key production hub for Evonik's "
            "specialty amino acid business in Asia."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Fermentation-derived L-amino acid and keto acid production\n"
            "High-purity amino acid purification\n"
            "Nutraceutical and pharma-grade fermentation"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000\nGMP (nutraceutical grade)",
        "extra": "Part of Evonik REXIM two-site network (Ham FR + Wuming CN) post-Hanau closure. Wuming District, Nanning, Guangxi Province.",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Kerry Group
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 6016,
        "facility": "Kerry – Carrigaline Enzyme Production",
        "tier": "Captive",
        "city": "Carrigaline",
        "country": "Ireland",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's industrial lactase enzyme production facility in Carrigaline, County "
            "Cork, Ireland. The world's largest lactase producer for lactose-free dairy, "
            "processing over 2 million tonnes of milk annually for 200+ customers in "
            "80+ countries. A significant capacity expansion completed April 2026. "
            "Kerry's Carrigaline site is the cornerstone of the global lactose-free dairy "
            "ingredient supply chain."
        ),
        "tech_areas": "Enzymatic catalysis\nMicrobial fermentation",
        "technologies": (
            "Industrial lactase fermentation and production\n"
            "Lactase enzyme concentration and formulation\n"
            "Continuous and batch milk hydrolysis systems\n"
            "Lactose-free dairy processing solutions"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "World's largest lactase producer. >2 million tonnes milk processed/yr. 200+ customers, 80+ countries. Capacity expansion April 2026.",
    },
    {
        "id": 6017,
        "facility": "Kerry Biotechnology Centre – Leipzig (C-LEcta)",
        "tier": "Pilot facility",
        "city": "Leipzig",
        "country": "Germany",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's biotechnology centre in Leipzig, Germany, built on the 2022 acquisition "
            "of C-LEcta (a University of Leipzig spin-out acquired for €137 million). Houses "
            "100+ scientists including 34 PhDs, specialising in enzyme engineering, "
            "fermentation development and bioprocess scale-up. Officially opened September 2025. "
            "Products include ACRYLERASE® (enzymatic acrylamide reduction in coffee and baked "
            "goods) and BIOBAKE® enzymes (bakery shelf-life extension). Acts as Kerry's "
            "global enzyme innovation hub with pilot production capability."
        ),
        "tech_areas": "Enzymatic catalysis\nMicrobial fermentation",
        "technologies": (
            "Enzyme engineering and directed evolution\n"
            "Fermentation process development and scale-up (pilot 1–500 L)\n"
            "ACRYLERASE® (acrylamide reduction enzyme) production\n"
            "BIOBAKE® bakery enzyme development\n"
            "Biocatalysis for food and beverage applications"
        ),
        "n_tech": 5,
        "certs": "ISO 9001",
        "extra": "C-LEcta acquisition 2022 (€137M). Opened September 2025. 100+ scientists, 34 PhDs. ACRYLERASE® and BIOBAKE® product lines. Kerry's global enzyme innovation hub.",
    },
    {
        "id": 6018,
        "facility": "Kerry – Beloit Yeast Extract & Fermentation",
        "tier": "Captive",
        "city": "Beloit",
        "country": "United States",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's US fermentation hub in Beloit, Wisconsin, producing Yeastex® yeast "
            "extracts, fermentation-derived savoury taste and preservation ingredients, "
            "and natural fermented flavours. The site applies yeast fermentation, autolysis "
            "and enzymatic hydrolysis to produce clean-label taste ingredients, umami "
            "enhancers, and natural antimicrobial solutions for food manufacturers. "
            "Key production site for Kerry's Taste & Nutrition Americas business."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Yeast submerged fermentation and autolysis\n"
            "Enzymatic protein hydrolysis for savoury extracts\n"
            "Yeastex® yeast extract production\n"
            "Natural fermented flavour development"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHACCP",
        "extra": "Produces Yeastex® yeast extracts and fermentation-derived savoury ingredients. Kerry Taste & Nutrition Americas hub.",
    },
    {
        "id": 6019,
        "facility": "Kerry – Jackson Dairy Cultures",
        "tier": "Captive",
        "city": "Jackson",
        "country": "United States",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's dairy ingredient and fermented dairy culture manufacturing facility "
            "in Jackson, Wisconsin. Produces dairy cultures, fermented dairy ingredients "
            "and specialty cheese/yogurt components for North American food manufacturers. "
            "Serves the US cheese, yogurt and fermented dairy sectors with starter cultures "
            "and processing aids."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures",
        "technologies": (
            "Dairy starter culture fermentation\n"
            "Fermented dairy ingredient production\n"
            "Culture standardisation and concentration\n"
            "Freeze-dried culture manufacturing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHACCP",
        "extra": "Dairy cultures and fermented dairy ingredients for North American food manufacturers.",
    },
    {
        "id": 6020,
        "facility": "Biosearch Life (Kerry) – Granada Probiotic Campus",
        "tier": "Captive",
        "city": "Granada",
        "country": "Spain",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's probiotic research and production campus in Granada, Spain, operated "
            "under the Biosearch Life brand (acquired by Kerry in 2021 for €127 million). "
            "Produces proprietary probiotic strains including Hereditum® range, breast "
            "milk-derived Lactobacillus strains, and specialty probiotics for women's health, "
            "infant nutrition and immunity. ~150 employees. Houses probiotic strain library, "
            "clinical research and industrial-scale fermentation and lyophilisation."
        ),
        "tech_areas": "Microbial fermentation\nProbiotics & cultures",
        "technologies": (
            "Lactic acid bacteria probiotic fermentation\n"
            "Breast milk-derived strain fermentation (Hereditum® range)\n"
            "Industrial-scale lyophilisation\n"
            "Clinical probiotic research and validation"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nGMP (dietary supplement)",
        "extra": "Acquired by Kerry 2021 (€127M). ~150 employees. Hereditum® proprietary probiotic strains. Specialty in women's health and infant nutrition probiotics.",
    },
    {
        "id": 6021,
        "facility": "Kerry – Tumkur Taste Manufacturing",
        "tier": "Captive",
        "city": "Tumkur",
        "country": "India",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's taste and fermented flavour systems manufacturing facility in Tumkur, "
            "Karnataka (~120 km from Bangalore), serving South and West Asia. A €20 million "
            "facility producing fermentation-derived savoury flavours, spice blends and "
            "food ingredient systems for Indian and Asian food manufacturers. Supports Kerry's "
            "growing presence in the Asia-Pacific taste and nutrition market."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Fermentation-derived savoury flavour production\n"
            "Enzymatic hydrolysis for taste ingredients\n"
            "Spice extract and flavour blending\n"
            "Yeast extract production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal",
        "extra": "€20M facility. ~120 km from Bangalore. Serves South and West Asia taste and nutrition market.",
    },
    {
        "id": 6022,
        "facility": "Kerry – Karawang Taste & Fermentation",
        "tier": "Captive",
        "city": "Karawang",
        "country": "Indonesia",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's Indonesian taste manufacturing and fermentation facility in Karawang, "
            "West Java. A 50,000 m² facility housing fermented flavour production, R&D "
            "pilot plant and application laboratories serving Southeast Asian food and "
            "beverage manufacturers. Produces fermentation-derived savoury ingredients, "
            "taste systems and functional food components for the ASEAN market."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Fermentation-derived flavour production\n"
            "Savoury taste ingredient manufacturing\n"
            "Pilot fermentation for ASEAN market development\n"
            "Application and sensory evaluation labs"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nHalal",
        "extra": "50,000 m² facility. R&D pilot plant on-site. ASEAN market hub for Kerry taste and nutrition.",
    },
    {
        "id": 6023,
        "facility": "Kerry – Jining Savoury Flavours (Jining Nature Group)",
        "tier": "Captive",
        "city": "Jining",
        "country": "China",
        "website": "https://www.kerry.com",
        "about": (
            "Kerry's Chinese savoury flavour production facility in Jining, Shandong, "
            "acquired through the Jining Nature Group acquisition. Produces fermentation-derived "
            "savoury flavours, seasonings, yeast extracts and umami ingredients for Chinese "
            "and Asian food manufacturers. Part of Kerry's expanding taste manufacturing "
            "presence in China."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Fermentation-derived savoury flavour and seasoning production\n"
            "Yeast extract and umami ingredient manufacturing\n"
            "Enzymatic hydrolysis for savoury taste"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 22000\nHACCP",
        "extra": "Jining Nature Group acquisition. Produces fermentation-derived savoury flavours for Chinese food industry.",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Cargill
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 6024,
        "facility": "Qore – Bio-based BDO Plant (Cargill / HELM JV)",
        "tier": "Captive",
        "city": "Eddyville",
        "country": "United States",
        "website": "https://www.qore.com",
        "about": (
            "World's largest bio-based 1,4-butanediol (BDO) production facility, opened "
            "July 2025 in Eddyville, Iowa. Qore is a 50/50 joint venture between Cargill "
            "and HELM AG using Genomatica's fermentation technology to convert corn sugars "
            "into QIRA™ bio-based BDO. Capacity 66,000 MT/yr. $300 million investment. "
            "QIRA™ bio-BDO is used in bioplastics (PBT, PBS), spandex fibres, engineering "
            "plastics and solvents, displacing petroleum-derived BDO."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Genomatica fermentation technology for bio-based 1,4-BDO from corn sugars\n"
            "Anaerobic fermentation in large-scale bioreactors\n"
            "BDO downstream purification and distillation\n"
            "Integration with Cargill corn wet milling for feedstock"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "50/50 JV Cargill + HELM AG. Opened July 2025. $300M investment. 66,000 MT/yr QIRA™ bio-BDO. Uses Genomatica technology. World's largest bio-BDO plant.",
    },
    {
        "id": 6025,
        "facility": "NatureWorks – Ingeo PLA Plant (Cargill / PTT GC JV)",
        "tier": "Captive",
        "city": "Blair",
        "country": "United States",
        "website": "https://www.natureworksllc.com",
        "about": (
            "World's largest polylactic acid (PLA) biopolymer production facility in Blair, "
            "Nebraska, operated by NatureWorks LLC — a 50/50 joint venture between Cargill "
            "and PTT Global Chemical (Thailand). Produces Ingeo™ PLA biopolymer from corn "
            "dextrose via lactic acid fermentation → lactide → polymerisation. Capacity "
            "~150,000 MT/yr. Operational since 2001 with multiple expansions. "
            "Ingeo™ is used in packaging, fibres, apparel, electronics and serviceware. "
            "Co-located with the Novonesis (Novozymes) Blair campus."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Lactic acid fermentation from corn dextrose\n"
            "Lactide synthesis and purification\n"
            "Ring-opening polymerisation to PLA (Ingeo™)\n"
            "Biopolymer pelletising and packaging"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001\nOK Compost\nDIN CERTCO",
        "extra": "50/50 JV: Cargill + PTT Global Chemical. ~150,000 MT/yr Ingeo™ PLA. Operational since 2001. Co-located with Novonesis Blair and Veramaris Blair.",
    },
    {
        "id": 6026,
        "facility": "Cargill – Fort Dodge Bioethanol",
        "tier": "Captive",
        "city": "Fort Dodge",
        "country": "United States",
        "website": "https://www.cargill.com",
        "about": (
            "Cargill's corn wet mill and bioethanol fermentation complex in Fort Dodge, "
            "Iowa, acquired from Tate & Lyle in 2011. Produces fuel ethanol (115 million "
            "gallons/year) alongside corn dextrose, starch and animal feed co-products. "
            "Part of Cargill's integrated North American corn processing and bioenergy network."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Corn wet milling and glucose production\n"
            "Continuous bioethanol fermentation\n"
            "Distillation and molecular sieve dehydration\n"
            "DDGS and gluten feed co-product processing"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "115 million gal/yr fuel ethanol. Acquired from Tate & Lyle 2011. Integrated corn wet mill.",
    },
    {
        "id": 6027,
        "facility": "ENOUGH – Mycoprotein Plant, Sas van Gent (Cargill partnership)",
        "tier": "Captive",
        "city": "Sas van Gent",
        "country": "Netherlands",
        "website": "https://www.enough-food.com",
        "about": (
            "ENOUGH's 15,000 m² commercial mycoprotein fermentation plant in Sas van Gent, "
            "Netherlands, co-located with Cargill's starch facility which supplies the "
            "fermentable sugar feedstock. Produces ABUNDA™ mycoprotein (Fusarium venenatum "
            "fungal biomass) for alternative protein food applications. Cargill is a Series C "
            "investor and holds a commercial offtake agreement (expanded 2024). The Cargill "
            "starch plant adjacent also operates bioethanol fermentation from the processing "
            "wastewater streams."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Continuous submerged fungal fermentation (Fusarium venenatum)\n"
            "ABUNDA™ mycoprotein biomass harvesting\n"
            "Mycoprotein texturisation and processing\n"
            "Integration with adjacent Cargill starch facility for glucose supply"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000",
        "extra": "ENOUGH-owned, Cargill Series C investor + offtake partner (expanded 2024). 15,000 m² facility. ABUNDA™ mycoprotein. Fungal fermentation for alternative protein.",
    },
    {
        "id": 6028,
        "facility": "Cargill – Barby Wheat Biorefinery",
        "tier": "Captive",
        "city": "Barby",
        "country": "Germany",
        "website": "https://www.cargill.com",
        "about": (
            "One of Europe's largest wheat starch processing and biorefinery facilities "
            "in Barby, Saxony-Anhalt, Germany. Produces wheat starch, vital wheat gluten, "
            "glucose syrups, wheat proteins and bioethanol from wheat. A ~€60 million "
            "dedicated ethanol fermentation plant was added around 2013. "
            "Supplies food, feed and bioenergy markets across Central Europe."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Wheat wet milling and starch separation\n"
            "Enzymatic saccharification to glucose\n"
            "Bioethanol fermentation from wheat starch\n"
            "Gluten washing and drying"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nISO 14001",
        "extra": "One of Europe's largest wheat starch facilities. €60M ethanol plant added ~2013. Supplies Central European food and bioenergy markets.",
    },
    {
        "id": 6029,
        "facility": "Cargill – Krefeld Wheat Biorefinery",
        "tier": "Captive",
        "city": "Krefeld",
        "country": "Germany",
        "website": "https://www.cargill.com",
        "about": (
            "Cargill's Krefeld facility in North Rhine-Westphalia processes wheat into "
            "specialty industrial wheat starches, vegetable wheat proteins, advanced biofuels "
            "and bioethanol following a major transformation (~$200 million investment) from "
            "corn to wheat processing. Supplies specialty starch and bioethanol to food, "
            "paper and bioenergy industries in Western Europe."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Wheat wet milling and specialty starch production\n"
            "Bioethanol fermentation from wheat\n"
            "Vegetable wheat protein processing\n"
            "Advanced biofuel (ethanol) production"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nISO 14001",
        "extra": "~$200M investment converting from corn to wheat processing. Advanced biofuel and specialty starch production.",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ADM — Fermentation & Industrial Biotech
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 6030,
        "facility": "ADM Clinton – Precision Fermentation Hub",
        "tier": "Open CMO",
        "city": "Clinton",
        "country": "United States",
        "website": "https://www.adm.com",
        "about": (
            "ADM's commercial-scale precision fermentation facility in Clinton, Iowa, "
            "converted from idle conventional fermentation space ($55.5 million investment, "
            "463,503 sq ft). Awarded $2.23 million Iowa tax credit; creates 53 new jobs. "
            "ADM's first offering of precision fermentation as a commercial manufacturing "
            "service: first product is EVERY Company's OvoPro™ egg white protein produced "
            "by yeast fermentation. Open to other precision fermentation customers for "
            "alternative proteins, enzymes and specialty food ingredients."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing",
        "technologies": (
            "Commercial-scale precision fermentation (yeast expression systems)\n"
            "Alternative protein production (OvoPro™ egg white protein)\n"
            "Downstream protein concentration and purification\n"
            "Open CMO precision fermentation services"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000",
        "extra": "$55.5M conversion of 463,503 sq ft idle fermentation space. First product: EVERY Company OvoPro™ egg white protein. ADM's commercial precision fermentation CMO platform.",
    },
    {
        "id": 6031,
        "facility": "ADM Cedar Rapids – Corn Wet Mill & Ethanol",
        "tier": "Captive",
        "city": "Cedar Rapids",
        "country": "United States",
        "website": "https://www.adm.com",
        "about": (
            "ADM's large corn wet mill and bioethanol complex in Cedar Rapids, Iowa, one "
            "of ADM's largest corn processing sites. Operates a 240 million gal/yr wet "
            "mill ethanol plant alongside a 300 million gal/yr dry mill, producing sweeteners "
            "(HFCS, dextrose), corn starches, animal feeds and fuel ethanol. An important "
            "Midwest bioenergy and sweetener production hub serving food, feed and "
            "industrial markets."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)\nEnzymatic catalysis",
        "technologies": (
            "Corn wet milling and starch hydrolysis\n"
            "Bioethanol fermentation (wet and dry mill)\n"
            "HFCS and dextrose enzymatic production\n"
            "Distillation and dehydration"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "240M gal/yr wet mill + 300M gal/yr dry mill ethanol. One of ADM's largest corn processing complexes.",
    },
    {
        "id": 6032,
        "facility": "ADM Columbus – Bioethanol & Carbon Capture",
        "tier": "Captive",
        "city": "Columbus",
        "country": "United States",
        "website": "https://www.adm.com",
        "about": (
            "ADM's Columbus, Nebraska bioethanol fermentation complex, producing "
            "420 million gallons per year of fuel ethanol from corn. Home to the world's "
            "largest bioethanol carbon capture facility (Tallgrass CCS), opened November 2025, "
            "capturing 800,000+ tonnes of CO₂ per year from fermentation off-gas for "
            "permanent geological storage. Landmark demonstration of carbon-negative "
            "bioethanol production."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Large-scale corn bioethanol fermentation (420M gal/yr)\n"
            "CO₂ capture from fermentation off-gas\n"
            "Carbon geological storage (CCS, Tallgrass partnership)\n"
            "Molecular sieve dehydration"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 14001",
        "extra": "420M gal/yr bioethanol. World's largest bioethanol CCS (Tallgrass, opened Nov 2025): 800,000+ t CO₂/yr captured. Carbon-negative fermentation landmark.",
    },
    {
        "id": 6033,
        "facility": "ADM Marshall – Bioethanol",
        "tier": "Captive",
        "city": "Marshall",
        "country": "United States",
        "website": "https://www.adm.com",
        "about": (
            "ADM's corn dry mill bioethanol fermentation facility in Marshall, Minnesota, "
            "producing approximately 52.7 million gallons per year of fuel ethanol. "
            "Part of ADM's extensive Midwest bioethanol network, contributing to the "
            "US corn ethanol industry and animal feed (DDGS) supply chain."
        ),
        "tech_areas": "Microbial fermentation\nFermentation (industrial)",
        "technologies": (
            "Corn dry mill bioethanol fermentation\n"
            "Distillation and molecular sieve dehydration\n"
            "DDGS production"
        ),
        "n_tech": 3,
        "certs": "ISO 9001\nISO 14001",
        "extra": "~52.7M gal/yr fuel ethanol. Part of ADM Midwest bioethanol network.",
    },
    {
        "id": 6034,
        "facility": "ADM WILD – Eppelheim (European Flavour Hub)",
        "tier": "Captive",
        "city": "Eppelheim",
        "country": "Germany",
        "website": "https://www.adm.com",
        "about": (
            "ADM WILD Europe's headquarters and main production plant in Eppelheim near "
            "Heidelberg, Germany, employing ~1,400 staff. WILD Flavors was acquired by "
            "ADM in 2014. Produces natural flavour systems, fermentation-derived taste "
            "ingredients, fruit concentrates, natural colours, sweetening systems and "
            "functional food ingredients for global food and beverage manufacturers. "
            "ADM's largest single flavour production site globally."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)",
        "technologies": (
            "Fermentation-derived natural flavour production\n"
            "Enzymatic flavour development\n"
            "Fruit concentrate processing\n"
            "Natural colour extraction and fermentation\n"
            "Spray encapsulation of flavour ingredients"
        ),
        "n_tech": 5,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
        "extra": "~1,400 employees. WILD Flavors acquired by ADM 2014. ADM's largest flavour production site globally. Near Heidelberg, Baden-Württemberg.",
    },
    {
        "id": 6035,
        "facility": "ADM WILD – Erlanger Flavour Production",
        "tier": "Captive",
        "city": "Erlanger",
        "country": "United States",
        "website": "https://www.adm.com",
        "about": (
            "ADM's WILD Flavors US flagship production facility in Erlanger, Kentucky, "
            "producing naturally derived colours, flavours, encapsulated ingredients and "
            "food reformulation solutions. A $15 million investment in 2025 followed by a "
            "$26 million expansion announced in 2026 reflects strong growth in natural "
            "food ingredient demand. Serves as ADM's North American flavour and colour "
            "innovation and co-creation hub for food and beverage customers."
        ),
        "tech_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Natural colour fermentation and extraction\n"
            "Fermentation-derived flavour production\n"
            "Encapsulated ingredient manufacturing\n"
            "Food reformulation co-creation services"
        ),
        "n_tech": 4,
        "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
        "extra": "$15M investment 2025 + $26M expansion announced 2026. ADM North America flavour and colour innovation hub. WILD Flavors heritage.",
    },
]


def row_from_entry(e: dict) -> dict:
    return {
        "ID": e["id"], "Facility": e["facility"], "Membership tier": e["tier"],
        "City": e["city"], "Country": e["country"], "Address": "",
        "Contact person": "", "Website": e.get("website", ""), "Social links": "",
        "About": e.get("about", ""), "Technology areas": e.get("tech_areas", ""),
        "Technologies": e.get("technologies", ""),
        "No. of technologies": e.get("n_tech", ""),
        "Certifications": e.get("certs", ""), "Non-technical services": "",
        "Open 24/7": "", "Extra information": e.get("extra", ""),
        "Downloads": "", "Videos": "", "Logo": "", "Pilots4U page": "",
    }


if __name__ == "__main__":
    global_path = DATA_DIR / "Global_biomanufacturing_database.xlsx"
    wb = openpyxl.load_workbook(global_path)
    ws = wb["All Facilities"]

    existing_ids = {row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0]}

    appended = 0
    for entry in FACILITIES:
        if entry["id"] in existing_ids:
            print(f"  Skip {entry['id']} – already in DB")
            continue
        ws.append([row_from_entry(entry).get(col, "") for col in COLUMNS])
        appended += 1

    wb.save(global_path)
    print(f"Appended {appended} rows → Global now {ws.max_row - 1} facilities")
