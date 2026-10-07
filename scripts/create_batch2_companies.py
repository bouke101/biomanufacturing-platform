"""
Batch 2: Lallemand, AB Mauri, Ohly, Lesaffre (new), AB Enzymes, Sensient,
Kyowa Hakko Bio, Global Bio-Chem, Vedan, Zhejiang NHU, NEPG, Anhui Tiger Biotech,
Xinfa Pharmaceutical, Kemin Industries, Corbion, Jungbunzlauer, TotalEnergies Corbion,
Novamont, Braskem, Danimer/Teknor Apex, Amyris, POET, Green Plains,
Raízen, Verbio, Quorn Foods, Perfect Day, Solar Foods, Calysta.
IDs 7001–7090.
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
    # ── LALLEMAND ─────────────────────────────────────────────────────────────
    {"id": 7001, "facility": "Lallemand – Montréal Yeast Plant", "tier": "Captive",
     "city": "Montréal", "country": "Canada", "website": "https://www.lallemand.com",
     "about": "Lallemand's flagship North American baker's yeast and specialty yeast production plant in Montréal, QC, celebrating its 100-year anniversary in 2023. Produces baker's yeast (fresh, active dry, instant), wine/oenology yeast, distilling yeast and selenium-enriched yeast by aerobic submerged fermentation. Also houses Lallemand's global R&D and commercial headquarters.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Aerobic submerged yeast fermentation\nSpecialty and selenium-enriched yeast production\nYeast drying (active dry, instant)",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nKosher\nHalal",
     "extra": "100-year anniversary 2023. Global HQ. Baker's yeast, wine yeast, distilling yeast, selenium yeast."},

    {"id": 7002, "facility": "Lallemand – Baltimore Yeast Plant", "tier": "Captive",
     "city": "Baltimore", "country": "United States", "website": "https://www.lallemand.com",
     "about": "Lallemand's major North American baker's yeast production facility in Baltimore, Maryland. Produces fresh and dry baker's yeast by aerobic submerged fermentation, supplying US food manufacturers and artisan bakeries.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nFresh and dry yeast production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000", "extra": "Major North American baker's yeast hub."},

    {"id": 7003, "facility": "Lallemand – Memphis Yeast Plant", "tier": "Captive",
     "city": "Memphis", "country": "United States", "website": "https://www.lallemand.com",
     "about": "Lallemand baker's yeast production facility in Memphis, Tennessee, built in 2003. Serves the US South food and bakery market with fresh and dry baker's yeast.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nFresh baker's yeast production",
     "certs": "ISO 9001\nISO 22000", "extra": "Built 2003. US South baker's yeast production."},

    {"id": 7004, "facility": "Lallemand – Hattiesburg Yeast Plant", "tier": "Captive",
     "city": "Hattiesburg", "country": "United States", "website": "https://www.lallemand.com",
     "about": "Lallemand baker's yeast manufacturing facility in Hattiesburg, Mississippi, serving the US South market.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nFresh baker's yeast production",
     "certs": "ISO 9001\nISO 22000", "extra": "US South baker's yeast production."},

    {"id": 7005, "facility": "Lallemand – Milwaukee Bacteria Plant", "tier": "Captive",
     "city": "Milwaukee", "country": "United States", "website": "https://www.lallemand.com",
     "about": "Lallemand's North American bacteria and probiotic fermentation facility in Milwaukee, Wisconsin. Produces lactic acid bacteria (LAB) starter cultures for wine, dairy and feed, plus probiotic and specialty bacteria by fermentation with downstream freeze-drying.",
     "tech_areas": "Microbial fermentation\nProbiotics & cultures", "n_tech": 3,
     "technologies": "LAB and probiotic fermentation\nFreeze-drying of bacterial cultures\nWine, dairy and feed bacteria production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000", "extra": "Key North American bacteria/probiotic fermentation site. Freeze-dried cultures."},

    {"id": 7006, "facility": "Lallemand – Saint-Simon Bacteria Plant", "tier": "Captive",
     "city": "Saint-Simon", "country": "France", "website": "https://www.lallemand.com",
     "about": "Lallemand's European bacteria fermentation plant in Saint-Simon, Cantal, France. Specialises in bacteria cultures for oenology (wine), dairy and feed applications, featuring large fermentation tanks and industrial freeze-drying.",
     "tech_areas": "Microbial fermentation\nProbiotics & cultures", "n_tech": 3,
     "technologies": "LAB fermentation for wine and dairy cultures\nIndustrial freeze-drying\nEnology bacteria production",
     "certs": "ISO 9001\nISO 22000", "extra": "Key European bacteria/oenology culture production site in Cantal, Auvergne."},

    {"id": 7007, "facility": "Lallemand – Vienna Yeast Plant", "tier": "Captive",
     "city": "Vienna", "country": "Austria", "website": "https://www.lallemand.com",
     "about": "Lallemand's Austrian baker's yeast and specialty yeast manufacturing facility in Vienna. Specialises in organic-certified cream yeast and specialty yeast for food and beverage applications.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Organic-certified cream yeast fermentation\nSpecialty yeast production",
     "certs": "ISO 9001\nISO 22000\nOrganic certification", "extra": "Organic cream yeast specialist. Vienna production hub."},

    {"id": 7008, "facility": "Lallemand – Schwarzenbach Yeast Plant", "tier": "Captive",
     "city": "Schwarzenbach an der Saale", "country": "Germany", "website": "https://www.lallemand.com",
     "about": "One of Europe's oldest yeast factories, founded in 1862 in Schwarzenbach an der Saale, Bavaria. Produces baker's yeast by aerobic submerged fermentation. Part of Lallemand's European yeast network.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nBaker's yeast production",
     "certs": "ISO 9001\nISO 22000", "extra": "Founded 1862. Oldest Bavarian yeast factory. Part of Lallemand European network."},

    {"id": 7009, "facility": "Lallemand – Salutaguse Bacteria Plant", "tier": "Captive",
     "city": "Salutaguse", "country": "Estonia", "website": "https://www.lallemand.com",
     "about": "Lallemand's key European bacteria fermentation facility in Salutaguse, Estonia. Produces lactic acid bacteria cultures and probiotics for food, feed and agricultural applications. Serves as a major Eastern European hub for bacteria fermentation and freeze-drying.",
     "tech_areas": "Microbial fermentation\nProbiotics & cultures", "n_tech": 3,
     "technologies": "LAB and probiotic fermentation\nFreeze-drying of bacterial cultures\nFood and feed culture production",
     "certs": "ISO 9001\nISO 22000", "extra": "Key Eastern European bacteria culture hub."},

    # ── AB MAURI ──────────────────────────────────────────────────────────────
    {"id": 7010, "facility": "AB Mauri – Casteggio Yeast Plant", "tier": "Captive",
     "city": "Casteggio", "country": "Italy", "website": "https://www.abmauri.com",
     "about": "AB Mauri's Casteggio facility in Lombardy, Italy, is the largest baker's yeast plant in Europe. Produces commercial baker's yeast in all formats (cream, compressed, active dry, instant dry) by aerobic submerged fermentation. Major energy efficiency upgrade completed 2022.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Aerobic submerged baker's yeast fermentation\nMulti-format yeast drying (compressed, ADY, IDY)\nCream yeast production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
     "extra": "Largest baker's yeast plant in Europe. Major energy efficiency upgrade 2022."},

    {"id": 7011, "facility": "AB Mauri – Cedar Rapids Yeast Plant", "tier": "Captive",
     "city": "Cedar Rapids", "country": "United States", "website": "https://www.abmauri.com",
     "about": "AB Mauri's flagship US baker's yeast production and specialty blending facility in Cedar Rapids, Iowa (44,000 sq ft). Produces baker's yeast in multiple formats and custom yeast blends for US food manufacturers.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nSpecialty yeast blending",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000", "extra": "44,000 sq ft. Flagship US baker's yeast and specialty blending site."},

    {"id": 7012, "facility": "AB Mauri – Wilsonville Yeast Plant", "tier": "Captive",
     "city": "Wilsonville", "country": "United States", "website": "https://www.abmauri.com",
     "about": "AB Mauri's West Coast baker's yeast production facility in Wilsonville, Oregon, supplying fresh and dry baker's yeast to Pacific Northwest and West Coast food manufacturers.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nFresh and dry baker's yeast",
     "certs": "ISO 9001\nISO 22000", "extra": "US West Coast baker's yeast hub."},

    {"id": 7013, "facility": "AB Mauri – Memphis Yeast Plant", "tier": "Captive",
     "city": "Memphis", "country": "United States", "website": "https://www.abmauri.com",
     "about": "AB Mauri's US South baker's yeast production facility in Memphis, Tennessee. Produces fresh baker's yeast for regional food manufacturers.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nFresh baker's yeast production",
     "certs": "ISO 9001\nISO 22000", "extra": "US South baker's yeast production hub."},

    {"id": 7014, "facility": "AB Mauri – LaSalle Yeast Plant", "tier": "Captive",
     "city": "LaSalle", "country": "Canada", "website": "https://www.abmauri.com",
     "about": "AB Mauri's Canadian baker's yeast production facility in LaSalle, Quebec, supplying Canadian food manufacturers with baker's yeast in multiple formats.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nBaker's yeast production",
     "certs": "ISO 9001\nISO 22000\nKosher", "extra": "Canadian production hub."},

    {"id": 7015, "facility": "AB Mauri – Veracruz Yeast Plant", "tier": "Captive",
     "city": "Veracruz", "country": "Mexico", "website": "https://www.abmauri.com",
     "about": "AB Mauri's Latin American baker's yeast production facility in Veracruz, Mexico. Serves Mexican and Latin American food manufacturers with baker's yeast in fresh and dry formats.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nFresh and dry baker's yeast",
     "certs": "ISO 9001\nISO 22000\nHalal\nKosher", "extra": "Latin American production hub."},

    # ── OHLY ──────────────────────────────────────────────────────────────────
    {"id": 7016, "facility": "Ohly – Hamburg Yeast Extract Plant", "tier": "Captive",
     "city": "Hamburg", "country": "Germany", "website": "https://www.ohly.com",
     "about": "Ohly's flagship yeast extract production facility in Hamburg, Germany, operating since 1836. Produces a full range of yeast extracts, yeast cell walls, beta-glucans and high-nucleotide extracts by fermentation, autolysis and spray-drying. New fermentation plant and spray-drying tower added +50% capacity. Part of ABF Ingredients group.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Yeast fermentation and autolysis\nYeast extract spray-drying and concentration\nHigh-nucleotide yeast extract production\nBeta-glucan and yeast cell wall extraction",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
     "extra": "Founded 1836. ABF Ingredients group. +50% capacity expansion (new fermentation plant + spray drying tower)."},

    {"id": 7017, "facility": "Ohly – Hutchinson Torula Extract Plant", "tier": "Captive",
     "city": "Hutchinson", "country": "United States", "website": "https://www.ohly.com",
     "about": "Ohly's US specialty yeast extract facility in Hutchinson, Minnesota, producing torula yeast (Cyberlindnera jadinii) extracts. Torula yeast extracts offer distinctive flavour profiles for food and fermentation media applications.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Torula yeast (Cyberlindnera jadinii) fermentation\nYeast extract autolysis and processing",
     "certs": "ISO 9001\nISO 22000", "extra": "Specialty torula yeast extracts. Distinctive flavour profiles for food and fermentation media."},

    {"id": 7018, "facility": "Ohly – Boyceville Yeast Extract Plant", "tier": "Captive",
     "city": "Boyceville", "country": "United States", "website": "https://www.ohly.com",
     "about": "Ohly's yeast extract and natural flavour production facility in Boyceville, Wisconsin. Produces multiple types of spray-dried yeast extracts and natural flavours for food applications.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Yeast fermentation and autolysis\nSpray-dried yeast extract production\nNatural flavour development",
     "certs": "ISO 9001\nISO 22000", "extra": "Spray-dried yeast extracts and natural flavours."},

    # ── LESAFFRE (new additions — Tianjin + Ennolys already in DB) ─────────────
    {"id": 7019, "facility": "Lesaffre – Marcq-en-Baroeul (Flagship)", "tier": "Captive",
     "city": "Marcq-en-Baroeul", "country": "France", "website": "https://www.lesaffre.com",
     "about": "Lesaffre's flagship production site and group headquarters in Marcq-en-Baroeul near Lille, France, housing the world's largest single baker's yeast plant. Founded 1853. Produces baker's yeast, specialty yeast, bread improvement systems and fermentation research. Lesaffre operates 80 production sites globally in 55 countries.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Aerobic submerged baker's yeast fermentation\nSpecialty yeast (wine, distilling, food)\nBread improvement ingredient production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
     "extra": "World's largest single baker's yeast plant. Lesaffre group HQ. Founded 1853. Global network of 80 production sites in 55 countries."},

    {"id": 7020, "facility": "Lesaffre – Ghent (Algist Bruggeman)", "tier": "Captive",
     "city": "Ghent", "country": "Belgium", "website": "https://www.lesaffre.com",
     "about": "Lesaffre's Belgian yeast production facility in Ghent, operating under the Algist Bruggeman brand. Produces baker's yeast for Belgian and northern European food markets. New investment announced August 2025 to expand craft and specialty yeast production capacity.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged baker's yeast fermentation\nSpecialty craft yeast production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "Algist Bruggeman brand. New specialty/craft yeast investment August 2025."},

    {"id": 7021, "facility": "Biospringer (Lesaffre) – Cedar Rapids", "tier": "Captive",
     "city": "Cedar Rapids", "country": "United States", "website": "https://www.biospringer.com",
     "about": "Lesaffre's Biospringer division yeast extract production facility in Cedar Rapids, Iowa. Produces nutritional yeast extracts, flavour yeast extracts and yeast-derived ingredients for food, beverage and fermentation media applications. Capacity expansion completed 2024–2025.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Yeast fermentation and autolysis\nYeast extract concentration and spray-drying\nNutritional and flavour yeast extract production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nHalal\nKosher",
     "extra": "Biospringer division of Lesaffre. Capacity expansion 2024–2025."},

    {"id": 7022, "facility": "Lesaffre – Jaguariúna Yeast Plant", "tier": "Captive",
     "city": "Jaguariúna", "country": "Brazil", "website": "https://www.lesaffre.com",
     "about": "Lesaffre's new baker's yeast manufacturing facility near Campinas, São Paulo state, Brazil, opened in 2024. Serves Brazilian and Latin American food markets with fresh and dry baker's yeast, reducing dependency on imported yeast.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nBaker's yeast production",
     "certs": "ISO 9001\nISO 22000\nHalal\nKosher",
     "extra": "New plant opened 2024. Near Campinas, São Paulo state. Brazilian and Latin American market supply."},

    {"id": 7023, "facility": "Lesaffre – Malang Yeast Plant", "tier": "Captive",
     "city": "Malang", "country": "Indonesia", "website": "https://www.lesaffre.com",
     "about": "Lesaffre's new baker's yeast production facility in Malang Regency, East Java, Indonesia, part of the company's Southeast Asian expansion. Produces fresh and dry baker's yeast for Indonesian and ASEAN food markets.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Aerobic submerged yeast fermentation\nFresh and dry baker's yeast",
     "certs": "ISO 9001\nISO 22000\nHalal",
     "extra": "SE Asia expansion. Malang Regency, East Java."},

    # ── AB ENZYMES ────────────────────────────────────────────────────────────
    {"id": 7024, "facility": "AB Enzymes – Rajamäki Production", "tier": "Captive",
     "city": "Rajamäki", "country": "Finland", "website": "https://www.abenzymes.com",
     "about": "AB Enzymes' main global enzyme production facility in Rajamäki, 50 km north of Helsinki, Finland. Produces industrial enzymes for animal feed, baking, textile, pulp & paper and brewing by submerged fungal fermentation. Pilot plant investment completed 2021 to accelerate scale-up. Part of ABF/Schwabe group.",
     "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)", "n_tech": 4,
     "technologies": "Submerged fungal fermentation for industrial enzymes\nFeed, baking, textile and brewing enzyme production\nPilot-scale fermentation (2021 investment)\nEnzyme downstream processing and formulation",
     "certs": "ISO 9001\nISO 14001\nFAMI-QS",
     "extra": "Main global enzyme production. ABF/Schwabe group. Pilot investment 2021 for faster scale-up. Multi-year ABF investment programme ongoing."},

    {"id": 7025, "facility": "AB Enzymes – Darmstadt R&D & Pilot", "tier": "Pilot facility",
     "city": "Darmstadt", "country": "Germany", "website": "https://www.abenzymes.com",
     "about": "AB Enzymes' European headquarters, R&D centre and pilot enzyme production facility in Darmstadt, Germany. Houses enzyme application development labs for food, feed, textile and industrial markets, co-located with commercial and technical teams.",
     "tech_areas": "Microbial fermentation\nEnzymatic catalysis", "n_tech": 2,
     "technologies": "Pilot enzyme fermentation and screening\nEnzyme application development (baking, feed, textile)",
     "certs": "ISO 9001",
     "extra": "AB Enzymes European HQ. Application development co-located with pilot production."},

    # ── SENSIENT TECHNOLOGIES ─────────────────────────────────────────────────
    {"id": 7026, "facility": "Sensient – Juneau Yeast Extract Plant", "tier": "Captive",
     "city": "Juneau", "country": "United States", "website": "https://www.sensient.com",
     "about": "Sensient Technologies' yeast extract fermentation and production facility in Juneau, Wisconsin, operating since 1906. Produces yeast extracts by fermentation and autolysis with spray-drying for food, feed and fermentation media applications. $18M capacity expansion completed 2012. Acquired by Sensient 1983.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Yeast fermentation and autolysis\nSpray-drying of yeast extracts\nFermentation media ingredients",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "Operating since 1906. $18M expansion 2012. ~100 employees."},

    {"id": 7027, "facility": "Sensient – Milwaukee HQ & Fermentation", "tier": "Captive",
     "city": "Milwaukee", "country": "United States", "website": "https://www.sensient.com",
     "about": "Sensient Technologies' headquarters and fermentation R&D and production facility in Milwaukee, Wisconsin. Produces fermentation-derived colours, flavours and bio-nutrients. Launched new fermentation nutrients product line for dairy cultures in September 2026.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Fermentation-derived colour production\nFermentation nutrient ingredients for dairy cultures\nFlavour fermentation R&D",
     "certs": "ISO 9001\nISO 22000",
     "extra": "Sensient global HQ. Launched dairy culture fermentation nutrients product line September 2026."},

    {"id": 7028, "facility": "Sensient – St. Louis Natural Colours", "tier": "Captive",
     "city": "St. Louis", "country": "United States", "website": "https://www.sensient.com",
     "about": "Sensient's largest facility in St. Louis, Missouri, producing natural colour extracts (fermentation-derived and plant-extracted) for food and beverage manufacturers. Up to $250 million expansion announced in 2025 to meet growing global demand for natural colours.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Natural colour fermentation and extraction\nFermentation-derived pigment production\nColour standardisation and formulation",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "Sensient's largest plant. Up to $250M expansion announced 2025."},

    # ── KYOWA HAKKO BIO ───────────────────────────────────────────────────────
    {"id": 7029, "facility": "Kyowa Hakko Bio – Hofu Plant (Yamaguchi Center)", "tier": "Captive",
     "city": "Hofu", "country": "Japan", "website": "https://www.kyowahakko-bio.co.jp",
     "about": "Kyowa Hakko Bio's Hofu Plant in Yamaguchi Prefecture, birthplace of industrial amino acid fermentation in Japan. Part of the integrated Yamaguchi Production Center with Ube Plant since 2008. Produces specialty L-amino acids (glutamine, arginine, citrulline, histidine), nucleotides and fine chemicals. Also home to Cognizin® citicoline and Setria® glutathione specialty ingredients. Kirin Group company.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "L-amino acid fermentation (glutamine, arginine, citrulline, histidine)\nNucleotide fermentation\nCognizin® citicoline production\nSetria® L-glutathione fermentation",
     "certs": "ISO 9001\nISO 22000\nGMP (specialty ingredients)",
     "extra": "Birthplace of Japanese industrial amino acid fermentation. Kirin Group. Integrated Yamaguchi Center with Ube since 2008. Cognizin® and Setria® specialty brands."},

    {"id": 7030, "facility": "Kyowa Hakko Bio – Ube Plant (Yamaguchi Center)", "tier": "Captive",
     "city": "Ube", "country": "Japan", "website": "https://www.kyowahakko-bio.co.jp",
     "about": "Kyowa Hakko Bio's Ube Plant in Yamaguchi Prefecture, co-managed with the Hofu Plant as the integrated Yamaguchi Production Center since 2008. Produces feed-grade amino acids and fermentation specialty chemicals. Kirin Group company.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Feed-grade amino acid fermentation\nFermentation specialty chemical production",
     "certs": "ISO 9001\nFAMI-QS",
     "extra": "Integrated Yamaguchi Production Center with Hofu since 2008. Kirin Group."},

    {"id": 7031, "facility": "Thai Kyowa Biotechnologies – Rayong", "tier": "Captive",
     "city": "Rayong", "country": "Thailand", "website": "https://www.kyowahakko-bio.co.jp",
     "about": "Thai Kyowa Biotechnologies' fermentation facility in Rayong, Thailand. New HMO (human milk oligosaccharide) fermentation wing opened in 2022, the first dedicated HMO production facility in Southeast Asia. Produces 2'-fucosyllactose (2'-FL), 3'-sialyllactose (3'-SL), 6'-sialyllactose (6'-SL) and other HMOs at ~300 MT/yr. Also produces amino acids.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "HMO (human milk oligosaccharide) fermentation — 2'-FL, 3'-SL, 6'-SL\nL-amino acid fermentation\nHMO purification and drying",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "First dedicated HMO fermentation facility in SE Asia. Opened 2022. ~300 MT/yr HMO capacity. Kyowa Hakko Bio / Kirin Group."},

    # ── GLOBAL BIO-CHEM ───────────────────────────────────────────────────────
    {"id": 7032, "facility": "Global Bio-Chem – Dehui Production Base", "tier": "Captive",
     "city": "Dehui", "country": "China", "website": "https://www.gbt.com.hk",
     "about": "Global Bio-Chem Technology Group's primary corn-based biochemical production hub in Dehui District, Changchun, Jilin Province. Produces lysine (98% feed grade, 65% liquid), L-glutamic acid, threonine and starch derivatives from corn wet milling. Currently undergoing restructuring due to Chinese market margin pressure.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Corn wet milling and glucose production\nLysine fermentation (feed grade)\nThreonine and glutamic acid fermentation\nStarch derivative production",
     "certs": "ISO 9001\nISO 22000\nFAMI-QS",
     "extra": "Primary hub for Global Bio-Chem corn amino acid operations. Dehui District, Changchun. Currently restructuring due to market pressure."},

    # ── VEDAN ─────────────────────────────────────────────────────────────────
    {"id": 7033, "facility": "Vedan – Long Thanh Complex", "tier": "Captive",
     "city": "Long Thanh", "country": "Vietnam", "website": "https://www.vedan.com",
     "about": "Vedan International's flagship 120-hectare fermentation complex in Long Thanh, Dong Nai Province, Vietnam, established 1991. Vedan's largest and most important production site. Produces MSG (monosodium glutamate), glucose syrup, modified starch, lysine, polyglutamic acid (PGA) and cassava-derived starch products. Major employer in the region.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 5,
     "technologies": "Glutamic acid fermentation for MSG\nLysine submerged fermentation\nPolyglutamic acid (PGA) fermentation\nGlucose syrup and modified starch processing\nCassava starch processing",
     "certs": "ISO 9001\nISO 22000\nHACCP",
     "extra": "120-hectare flagship complex. Established 1991. Vedan's largest site. Produces MSG, lysine, PGA, glucose syrup, modified starch."},

    {"id": 7034, "facility": "Vedan – Xiamen Plant", "tier": "Captive",
     "city": "Xiamen", "country": "China", "website": "https://www.vedan.com",
     "about": "Vedan International's Chinese MSG and fermentation seasoning production facility in Xiamen, Fujian Province, acquired in 1995. Produces MSG and fermentation-derived seasonings for the Chinese domestic market.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Glutamic acid fermentation for MSG\nFermentation seasoning production",
     "certs": "ISO 9001\nISO 22000\nHACCP",
     "extra": "Acquired 1995. Serves Chinese domestic MSG and seasoning market."},

    {"id": 7035, "facility": "Vedan – Taichung Founding Site", "tier": "Captive",
     "city": "Taichung", "country": "Taiwan", "website": "https://www.vedan.com",
     "about": "Vedan's original founding production site in Taichung, Taiwan, established 1954. At peak in 1986, was the world's largest MSG output facility. Current production scale is reduced but site remains operational.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Glutamic acid fermentation for MSG\nFermentation seasoning production",
     "certs": "ISO 9001\nISO 22000",
     "extra": "Founding site (1954). At peak (1986) world's largest MSG output. Current scale reduced."},

    # ── ZHEJIANG NHU ──────────────────────────────────────────────────────────
    {"id": 7036, "facility": "NHU – Xinchang Production Base", "tier": "Captive",
     "city": "Xinchang", "country": "China", "website": "https://www.nhu.com.cn",
     "about": "Zhejiang NHU Co. Ltd's main human and animal nutrition production hub in Xinchang County, Zhejiang Province. Produces Vitamins E, A and D3, along with animal nutrition products. Includes Vityesun Animal Nutrition subsidiary.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Vitamin E and A synthesis and fermentation-assisted production\nVitamin D3 production\nAnimal nutrition ingredient manufacturing",
     "certs": "ISO 9001\nISO 22000\nISO 14001",
     "extra": "Main Zhejiang NHU nutrition hub. Vitamins E, A, D3. Vityesun Animal Nutrition subsidiary."},

    {"id": 7037, "facility": "NHU – Shangyu Production Base", "tier": "Captive",
     "city": "Shangyu", "country": "China", "website": "https://www.nhu.com.cn",
     "about": "Zhejiang NHU's Shangyu production base (Shaoxing City, Zhejiang), home to NHU Bio-Chem Co. and NHU Pharmaceutical Co. subsidiaries. Produces lutein, astaxanthin, taurine, vitamins and specialty materials.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Astaxanthin and lutein biosynthesis and purification\nTaurine production\nSpecialty vitamin and material manufacturing",
     "certs": "ISO 9001\nISO 22000\nISO 14001",
     "extra": "Shaoxing City. Houses NHU Bio-Chem Co. and NHU Pharmaceutical Co. Lutein, astaxanthin, taurine."},

    {"id": 7038, "facility": "NHU – Weifang Production Base", "tier": "Captive",
     "city": "Weifang", "country": "China", "website": "https://www.nhu.com.cn",
     "about": "NHU's largest single production site in Weifang, Shandong Province. Produces flavour and fragrance chemicals (linalool, geraniol, raspberry ketone), nutritional products and new materials. Largest NHU production base.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nEnzymatic catalysis", "n_tech": 3,
     "technologies": "Flavour and fragrance chemical production (linalool, geraniol)\nNutritional ingredient manufacturing\nNew material synthesis",
     "certs": "ISO 9001\nISO 22000\nISO 14001",
     "extra": "NHU's largest single production base. Weifang, Shandong. Flavour/fragrance + nutritional products."},

    {"id": 7039, "facility": "Heilongjiang NHU Biotechnology – Suihua", "tier": "Captive",
     "city": "Suihua", "country": "China", "website": "https://www.nhu.com.cn",
     "about": "NHU's dedicated bio-fermentation centre in Suihua, Heilongjiang Province. Produces CoQ10, Vitamin C, Vitamin B12, calcium pantothenate and serine by bio-fermentation, leveraging local corn as feedstock. Purpose-built for NHU's fermentation-first product lines.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "CoQ10 fermentation\nVitamin C two-step fermentation\nVitamin B12 fermentation\nCalcium pantothenate and serine fermentation",
     "certs": "ISO 9001\nISO 22000\nISO 14001",
     "extra": "NHU dedicated bio-fermentation centre. CoQ10, Vitamin C, B12, pantothenate. Corn feedstock from Heilongjiang."},

    # ── NEPG ──────────────────────────────────────────────────────────────────
    {"id": 7040, "facility": "Northeast Pharmaceutical Group (NEPG) – Shenyang", "tier": "Captive",
     "city": "Shenyang", "country": "China", "website": "https://www.nepg.com.cn",
     "about": "Northeast Pharmaceutical Group (NEPG) production base in Shenyang, Liaoning Province. The world's largest Vitamin C producer and the inventor of China's two-step fermentation process for Vitamin C. Also produces Vitamin B12. 180,000 m² production zone with over 30 production lines.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Two-step fermentation process for Vitamin C (ascorbic acid)\nVitamin B12 fermentation\nVitamin C crystallisation and purification",
     "certs": "ISO 9001\nISO 22000\nGMP",
     "extra": "World's largest Vitamin C producer. Inventor of two-step Vitamin C fermentation process. 180,000 m² production zone, 30+ lines. Shenyang, Liaoning."},

    # ── ANHUI TIGER BIOTECH ───────────────────────────────────────────────────
    {"id": 7041, "facility": "Anhui Tiger Biotech – Bengbu", "tier": "Captive",
     "city": "Bengbu", "country": "China", "website": "https://www.tigerbiotech.com.cn",
     "about": "Anhui Tiger Biotech Co. Ltd's production facility in Bengbu, Anhui Province, a subsidiary of BBCA Group. Houses the world's largest Vitamin C and Vitamin C derivatives production line. Also produces biotin (50 t/yr), Vitamins B5, B6, B9 and Vitamin E. Large-scale industrial fermentation and chemical synthesis.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Vitamin C (ascorbic acid) and derivative production (world's largest line)\nBiotin fermentation (50 t/yr)\nVitamin B5, B6, B9 production\nVitamin E manufacturing",
     "certs": "ISO 9001\nISO 22000\nGMP",
     "extra": "World's largest Vitamin C production line. Biotin 50 t/yr. BBCA Group subsidiary. Bengbu, Anhui."},

    # ── XINFA PHARMACEUTICAL ──────────────────────────────────────────────────
    {"id": 7042, "facility": "Xinfa Pharmaceutical – Dongying", "tier": "Captive",
     "city": "Dongying", "country": "China", "website": "https://www.xinfapharm.com",
     "about": "Xinfa Pharmaceutical Co. Ltd's production facility in Kengli District, Dongying, Shandong Province. Among the global top 1–2 producers of D-calcium pantothenate (Vitamin B5) and folic acid (Vitamin B9). Also produces Vitamins A, B1, B6, D3 by chemical synthesis and fermentation. Exports to 70+ countries. Founded 1998.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "D-calcium pantothenate production (global #1–2 capacity)\nFolic acid synthesis\nVitamin A and D3 production\nVitamin B1, B6 manufacturing",
     "certs": "ISO 9001\nISO 22000\nGMP",
     "extra": "Founded 1998. Global #1–2 D-calcium pantothenate capacity. Exports 70+ countries. Dongying, Shandong."},

    # ── KEMIN INDUSTRIES ──────────────────────────────────────────────────────
    {"id": 7043, "facility": "Kemin – Des Moines Campus", "tier": "Captive",
     "city": "Des Moines", "country": "United States", "website": "https://www.kemin.com",
     "about": "Kemin Industries' global headquarters and primary manufacturing campus in Des Moines, Iowa, covering 70 acres. Produces FloraGLO® lutein (extracted from marigold flowers), ORO GLO®/KEM GLO™ carotenoids for poultry colouring, feed antioxidants and specialty functional food ingredients. ~$10M lutein expansion completed.",
     "tech_areas": "Enzymatic catalysis\nDownstream processing\nFermentation (industrial)", "n_tech": 4,
     "technologies": "FloraGLO® lutein extraction and purification from marigold\nCarotenoid bioconversion and encapsulation\nFeed antioxidant production\nSpecialty nutritional ingredient manufacturing",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nNSF",
     "extra": "Global HQ. 70-acre campus. ~$1.4B revenue company. FloraGLO® lutein. $10M lutein expansion."},

    {"id": 7044, "facility": "Kemin Europe – Herentals", "tier": "Captive",
     "city": "Herentals", "country": "Belgium", "website": "https://www.kemin.com",
     "about": "Kemin's European manufacturing hub in Herentals, Antwerp Province, Belgium. Produces FORTIUM™ R rosemary extract (natural antioxidant for food and feed), EU-market carotenoids and specialty feed and food ingredients. Operates 1,000+ acres of proprietary rosemary cultivation.",
     "tech_areas": "Enzymatic catalysis\nDownstream processing", "n_tech": 3,
     "technologies": "Rosemary extract production (FORTIUM™ R)\nCarotenoid extraction and formulation\nNatural antioxidant ingredient manufacturing",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nOrganic",
     "extra": "European manufacturing hub. FORTIUM™ R rosemary extract. 1,000+ acres proprietary rosemary. EU regulatory hub."},

    {"id": 7045, "facility": "Kemin Asia-Pacific – Singapore", "tier": "Captive",
     "city": "Singapore", "country": "Singapore", "website": "https://www.kemin.com",
     "about": "Kemin Industries' Asia-Pacific regional headquarters and manufacturing facility in Singapore. Produces specialty food and feed ingredients for APAC markets. $35 million Kuriosity Innovation Centre under construction (groundbreaking July 2026) will add new R&D and manufacturing capability.",
     "tech_areas": "Enzymatic catalysis\nDownstream processing", "n_tech": 2,
     "technologies": "Specialty ingredient production for APAC\nFood and feed additive manufacturing",
     "certs": "ISO 9001\nISO 22000",
     "extra": "APAC regional HQ. $35M Kuriosity Centre under construction (groundbreaking July 2026)."},

    {"id": 7046, "facility": "Kemin China Enzyme Operations (CJ Youtell)", "tier": "Captive",
     "city": "Jinan", "country": "China", "website": "https://www.kemin.com",
     "about": "Kemin's Chinese fermentation enzyme production operations, acquired from CJ Bio subsidiary CJ Youtell in September 2025. Sites in Shandong and Hunan provinces. Produces fermentation-derived enzymes for animal nutrition and food processing.",
     "tech_areas": "Microbial fermentation\nEnzymatic catalysis\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Submerged fermentation for industrial enzymes\nAnimal nutrition enzyme production",
     "certs": "ISO 9001\nFAMI-QS",
     "extra": "Acquired from CJ Bio (CJ Youtell) September 2025. Sites in Shandong and Hunan. Fermentation enzyme production."},

    # ── CORBION ───────────────────────────────────────────────────────────────
    {"id": 7047, "facility": "Corbion – Gorinchem (HQ)", "tier": "Captive",
     "city": "Gorinchem", "country": "Netherlands", "website": "https://www.corbion.com",
     "about": "Corbion's headquarters and primary European lactic acid fermentation facility in Gorinchem, Netherlands. Produces lactic acid, sodium and potassium lactate, biobased preservatives and food/feed ingredients. Purac heritage. Corbion is the world's leading lactic acid producer.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Lactic acid fermentation from glucose\nLactate salt production and purification\nBiobased food preservative production\nFermentation-derived feed ingredient manufacturing",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "Corbion global HQ. Purac heritage. World's leading lactic acid producer."},

    {"id": 7048, "facility": "Corbion – Montmeló (Purac Bioquímica)", "tier": "Captive",
     "city": "Montmeló", "country": "Spain", "website": "https://www.corbion.com",
     "about": "Corbion's Spanish lactic acid and food preservation ingredient production facility near Barcelona (Purac Bioquímica brand). Produces lactic acid, lactates and specialty food preservation ingredients for the European food and feed industries.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Lactic acid fermentation\nLactate food preservation ingredient production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "Purac Bioquímica brand. Near Barcelona."},

    {"id": 7049, "facility": "Corbion – Campos (Brazil)", "tier": "Captive",
     "city": "Campos dos Goytacazes", "country": "Brazil", "website": "https://www.corbion.com",
     "about": "Corbion's lactic acid fermentation facility in Campos dos Goytacazes, Rio de Janeiro state, Brazil. Uses sugarcane as the fermentation feedstock for lactic acid production, benefiting from local sugarcane supply.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Lactic acid fermentation from sugarcane\nLactate purification and formulation",
     "certs": "ISO 9001\nISO 22000",
     "extra": "Sugarcane-derived lactic acid. Campos dos Goytacazes, Rio de Janeiro state."},

    {"id": 7050, "facility": "Corbion – Blair", "tier": "Captive",
     "city": "Blair", "country": "United States", "website": "https://www.corbion.com",
     "about": "Corbion's North American lactic acid fermentation facility in Blair, Nebraska, co-located on the Blair biocampus with NatureWorks (PLA), Veramaris (algal omega-3) and ADM. 40% capacity expansion completed ~2022. Runs on 100% renewable electricity.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Lactic acid fermentation\nLactate purification",
     "certs": "ISO 9001\nISO 22000\nISO 14001",
     "extra": "40% capacity expansion ~2022. 100% renewable electricity. Co-located on Blair biocampus with NatureWorks (6025), Veramaris (5012)."},

    {"id": 7051, "facility": "Corbion – Rayong", "tier": "Captive",
     "city": "Rayong", "country": "Thailand", "website": "https://www.corbion.com",
     "about": "Corbion's newest and lowest-carbon lactic acid fermentation facility in Rayong, Thailand, started up end 2024. Uses a circular process and feeds lactic acid directly to the adjacent TotalEnergies Corbion PLA plant. Supplies the fastest-growing Asian lactate market.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Circular lactic acid fermentation (lowest-carbon process)\nLactate purification for PLA feedstock",
     "certs": "ISO 9001\nISO 22000\nISO 14001",
     "extra": "Started end 2024. Lowest-carbon lactic acid process. Feeds adjacent TotalEnergies Corbion PLA plant."},

    # ── JUNGBUNZLAUER ─────────────────────────────────────────────────────────
    {"id": 7052, "facility": "Jungbunzlauer – Pernhofen", "tier": "Captive",
     "city": "Pernhofen", "country": "Austria", "website": "https://www.jungbunzlauer.com",
     "about": "Jungbunzlauer's flagship production site in Pernhofen, Lower Austria, operating since 1962. The world's largest citric acid plant, producing food- and industrial-grade citric acid by submerged fungal fermentation. Part of the privately held Jungbunzlauer group headquartered in Basel.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Citric acid submerged fermentation (Aspergillus niger)\nCitric acid crystallisation and purification\nFood and industrial-grade citric acid production",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "World's largest citric acid plant. Operating since 1962. Pernhofen, Lower Austria."},

    {"id": 7053, "facility": "Jungbunzlauer – Ladenburg", "tier": "Captive",
     "city": "Ladenburg", "country": "Germany", "website": "https://www.jungbunzlauer.com",
     "about": "Jungbunzlauer's pharmaceutical-grade citric acid production facility in Ladenburg, Baden-Württemberg, Germany. GMP-compliant and FDA-inspected; sole dedicated pharma-grade citric acid site in the Jungbunzlauer network.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "GMP citric acid fermentation and purification\nPharmaceutical excipient citric acid production",
     "certs": "ISO 9001\nGMP\nFDA-inspected",
     "extra": "GMP-compliant. FDA-inspected. Sole pharma-grade citric acid site in Jungbunzlauer network."},

    {"id": 7054, "facility": "Jungbunzlauer – Marckolsheim", "tier": "Captive",
     "city": "Marckolsheim", "country": "France", "website": "https://www.jungbunzlauer.com",
     "about": "Jungbunzlauer's Alsace production facility in Marckolsheim, producing ERYLITE® erythritol, gluconic acid, lactic acid and sodium gluconate — all by fermentation. Non-GMO fermentation processes. Erythritol capacity expanded to meet demand growth.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "ERYLITE® erythritol fermentation (non-GMO)\nGluconic acid and sodium gluconate fermentation\nLactic acid fermentation",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000\nNon-GMO",
     "extra": "ERYLITE® erythritol (expanded capacity), gluconate, lactic acid — all by fermentation. Non-GMO. Marckolsheim, Alsace."},

    {"id": 7055, "facility": "Jungbunzlauer – Port Colborne", "tier": "Captive",
     "city": "Port Colborne", "country": "Canada", "website": "https://www.jungbunzlauer.com",
     "about": "Jungbunzlauer's North American food-grade citric acid fermentation facility in Port Colborne, Ontario, operational since 2002. Includes corn wet milling for glucose feedstock production. Multiple capacity expansions since opening.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Citric acid submerged fermentation\nCorn wet milling for glucose feedstock\nCitric acid crystallisation and purification",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "Operational since 2002. Includes corn wet milling. Multiple capacity expansions. Port Colborne, Ontario."},

    # ── TOTALENERGIES CORBION ─────────────────────────────────────────────────
    {"id": 7056, "facility": "TotalEnergies Corbion – LUMINY® PLA Plant", "tier": "Captive",
     "city": "Rayong", "country": "Thailand", "website": "https://www.totalenergies-corbion.com",
     "about": "TotalEnergies Corbion's LUMINY® polylactic acid (PLA) biopolymer plant in Rayong, Thailand. 50/50 joint venture between TotalEnergies and Corbion. Produces 75,000 MT/yr of LUMINY® PLA biopolymer and 100,000 t/yr lactide intermediate from lactic acid. Running above nameplate capacity in 2025. Co-located with Corbion Rayong lactic acid facility.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Lactide synthesis from lactic acid\nRing-opening polymerisation to LUMINY® PLA\nPLA pelletising and packaging",
     "certs": "ISO 9001\nISO 14001\nOK Compost\nDIN CERTCO",
     "extra": "50/50 JV: TotalEnergies + Corbion. 75,000 MT/yr PLA + 100,000 t/yr lactide. Running above nameplate 2025. Co-located with Corbion Rayong (7051)."},

    # ── NOVAMONT ──────────────────────────────────────────────────────────────
    {"id": 7057, "facility": "Novamont – Terni Biopolymer Plant", "tier": "Captive",
     "city": "Terni", "country": "Italy", "website": "https://www.novamont.com",
     "about": "Novamont's flagship biopolymer production site in Terni, Umbria, Italy. The world's leading integrated biorefinery for starch-based and fermentation-derived bioplastics. Produces Mater-Bi® starch-biopolymers (120,000 t/yr), Origo-Bi biopolyesters (60,000 t/yr) and Matrol-Bi biolubricants. Regenerated a former polymer site.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Mater-Bi® starch-biopolymer compounding\nOrigo-Bi biopolyester production\nBiolubricant manufacturing",
     "certs": "ISO 9001\nISO 14001\nOK Compost\nEN 13432",
     "extra": "120,000 t/yr Mater-Bi® + 60,000 t/yr Origo-Bi. Regenerated former polymer site. World's leading starch biopolymer site."},

    {"id": 7058, "facility": "Novamont – Novara Innovation Hub", "tier": "Pilot facility",
     "city": "Novara", "country": "Italy", "website": "https://www.novamont.com",
     "about": "Novamont's headquarters and R&D/innovation centre in Novara, Piedmont, Italy. Houses pilot plants, process development facilities and scientific research teams for next-generation biobased materials and biopolymer formulations.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Biopolymer process development and pilot production\nBiobased material R&D",
     "certs": "ISO 9001",
     "extra": "Novamont global HQ + R&D pilot facilities. Novara, Piedmont."},

    {"id": 7059, "facility": "Novamont – Porto Torres Biorefinery", "tier": "Captive",
     "city": "Porto Torres", "country": "Italy", "website": "https://www.novamont.com",
     "about": "Novamont's Porto Torres industrial biorefinery in Sardinia, producing Matrilox® bio-based chemicals and biolubricants from vegetable oil feedstocks, including azelaic acid and sebacic acid. Originally the Matrìca JV with Versalis (ENI), fully absorbed by Novamont in November 2025.",
     "tech_areas": "Fermentation (industrial)\nDownstream processing\nEnzymatic catalysis", "n_tech": 3,
     "technologies": "Azelaic acid and sebacic acid production from vegetable oil\nBio-based lubricant ingredient production\nBiorefinery processing of plant-derived feedstocks",
     "certs": "ISO 9001\nISO 14001",
     "extra": "Formerly Matrìca JV (Novamont + Versalis/ENI); absorbed Nov 2025. Porto Torres, Sardinia."},

    {"id": 7060, "facility": "Mater-Biotech (Novamont) – Adria", "tier": "Captive",
     "city": "Adria", "country": "Italy", "website": "https://www.novamont.com",
     "about": "Mater-Biotech (Novamont JV) in Adria, Veneto, Italy — the world's first commercial plant to produce bio-based 1,4-butanediol (bio-BDO) by fermentation. Uses Genomatica's proprietary fermentation technology. 30,000 t/yr capacity. Opened September 2016 with €100 million investment. Bio-BDO used in bioplastics (PBS, PBAT), spandex and engineering polymers.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Genomatica fermentation technology for bio-based 1,4-BDO\nAnaerobic fermentation from glucose\nBio-BDO purification and distillation",
     "certs": "ISO 9001\nISO 14001",
     "extra": "World's first commercial bio-BDO by fermentation. Opened Sept 2016. €100M investment. 30,000 t/yr. Genomatica technology."},

    # ── BRASKEM ───────────────────────────────────────────────────────────────
    {"id": 7061, "facility": "Braskem – Green PE Plant (I'm Green™)", "tier": "Captive",
     "city": "Triunfo", "country": "Brazil", "website": "https://www.braskem.com",
     "about": "Braskem's world-leading bio-based polyethylene plant in Triunfo, Rio Grande do Sul, Brazil. Produces I'm Green™ bio-PE from sugarcane bioethanol (ethanol → ethylene → PE). 275,000 t/yr capacity following $87 million expansion completed 2023. Operational since 2010. Each tonne of bio-PE captures approximately 2 tonnes of CO₂.",
     "tech_areas": "Fermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "Sugarcane bioethanol fermentation\nBio-ethylene production from bioethanol\nI'm Green™ bio-PE polymerisation",
     "certs": "ISO 9001\nISO 14001\nUSDA BioPreferred",
     "extra": "275,000 t/yr. $87M expansion 2023. Operational since 2010. ~2 t CO₂ captured/t product. World-leading bio-PE site."},

    # ── DANIMER / TEKNOR APEX ─────────────────────────────────────────────────
    {"id": 7062, "facility": "Danimer (Teknor Apex) – Winchester PHA Plant", "tier": "Captive",
     "city": "Winchester", "country": "United States", "website": "https://www.teknorapex.com",
     "about": "PHA biopolymer fermentation facility in Winchester, Kentucky. Produces Nodax™ polyhydroxyalkanoate (PHA) biopolymer by bacterial fermentation. 65 million lb/yr capacity. Danimer Scientific filed Chapter 11 bankruptcy March 2025 and was acquired by Teknor Apex. Winchester plant remains operational under Teknor Apex ownership.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "PHA (Nodax™) bacterial fermentation\nPHA extraction and purification\nBiopolymer compounding",
     "certs": "ISO 9001\nISO 14001",
     "extra": "Danimer filed Ch.11 March 2025; acquired by Teknor Apex. Operating. 65 Mlb/yr Nodax™ PHA."},

    # ── AMYRIS ────────────────────────────────────────────────────────────────
    {"id": 7063, "facility": "Amyris – Barra Bonita Fermentation Plant", "tier": "Captive",
     "city": "Barra Bonita", "country": "Brazil", "website": "https://www.amyris.com",
     "about": "Amyris's primary commercial fermentation facility in Barra Bonita, São Paulo state, Brazil. Produces squalane, farnesene, Reb M (steviol glycoside sweetener) and other specialty ingredients by engineered yeast fermentation. Post-2023 bankruptcy restructuring, Amyris pivoted to B2B ingredient supply. Current production: 3×200 m³ fermenters plus new 2×80 m³ line.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Engineered yeast fermentation (farnesene, squalane, Reb M)\nFarnesene hydrogenation to squalane\nReb M purification",
     "certs": "ISO 9001\nISO 22000",
     "extra": "Post-2023 bankruptcy B2B pivot. 3×200 m³ + 2×80 m³ fermenters. Squalane, farnesene, Reb M sweetener."},

    # ── POET ──────────────────────────────────────────────────────────────────
    {"id": 7064, "facility": "POET – Shelbyville Bioprocessing", "tier": "Captive",
     "city": "Shelbyville", "country": "United States", "website": "https://www.poet.com",
     "about": "POET LLC's Shelbyville, Indiana bioethanol facility, currently expanding from 98 million to 193 million gallons per year (completion Q4 2027), making it one of POET's flagship plants. POET is the world's largest bioethanol producer with 35 plants and 3.1 billion gal/yr capacity across 9 US states.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Corn dry mill bioethanol fermentation\nDistillation and molecular sieve dehydration\nDDGS co-product production",
     "certs": "ISO 9001\nISO 14001",
     "extra": "98M → 193M gal/yr expansion by Q4 2027. POET: 35 plants, 3.1B gal/yr total, world's largest bioethanol network."},

    {"id": 7065, "facility": "POET – Coon Rapids Bioprocessing", "tier": "Captive",
     "city": "Coon Rapids", "country": "United States", "website": "https://www.poet.com",
     "about": "POET LLC's corn bioethanol facility in Coon Rapids, Iowa, part of POET's Iowa cluster. One of 35 POET plants in a 3.1 billion gal/yr national bioethanol network.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Corn dry mill bioethanol fermentation\nDDGS co-product production",
     "certs": "ISO 9001\nISO 14001", "extra": "POET Iowa cluster. Part of 35-plant, 3.1B gal/yr national network."},

    {"id": 7066, "facility": "POET – Jewell Bioprocessing", "tier": "Captive",
     "city": "Jewell", "country": "United States", "website": "https://www.poet.com",
     "about": "POET LLC's corn bioethanol facility in Jewell, Iowa, part of POET's Iowa cluster.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Corn dry mill bioethanol fermentation\nDDGS co-product production",
     "certs": "ISO 9001\nISO 14001", "extra": "POET Iowa cluster."},

    {"id": 7067, "facility": "POET – Gowrie Bioprocessing", "tier": "Captive",
     "city": "Gowrie", "country": "United States", "website": "https://www.poet.com",
     "about": "POET LLC's corn bioethanol facility in Gowrie, Iowa, part of POET's Iowa cluster.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Corn dry mill bioethanol fermentation\nDDGS co-product production",
     "certs": "ISO 9001\nISO 14001", "extra": "POET Iowa cluster."},

    {"id": 7068, "facility": "POET – Corning Bioprocessing", "tier": "Captive",
     "city": "Corning", "country": "United States", "website": "https://www.poet.com",
     "about": "POET LLC's corn bioethanol facility in Corning, Iowa, part of POET's Iowa cluster.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Corn dry mill bioethanol fermentation\nDDGS co-product production",
     "certs": "ISO 9001\nISO 14001", "extra": "POET Iowa cluster."},

    # ── GREEN PLAINS ──────────────────────────────────────────────────────────
    {"id": 7069, "facility": "Green Plains – Wood River", "tier": "Captive",
     "city": "Wood River", "country": "United States", "website": "https://www.gpreinc.com",
     "about": "Green Plains Inc.'s Wood River, Nebraska corn bioethanol facility, 121 million gal/yr. Active carbon capture and storage (CCS). Part of Green Plains' nine-plant Midwest bioethanol network.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Corn bioethanol fermentation\nCO₂ capture from fermentation (CCS)",
     "certs": "ISO 9001\nISO 14001",
     "extra": "121M gal/yr. CCS active. Green Plains 9-plant network."},

    {"id": 7070, "facility": "Green Plains – Central City", "tier": "Captive",
     "city": "Central City", "country": "United States", "website": "https://www.gpreinc.com",
     "about": "Green Plains Inc.'s Central City, Nebraska corn bioethanol facility, 116 million gal/yr. Active carbon capture and storage (CCS).",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Corn bioethanol fermentation\nCO₂ capture from fermentation (CCS)",
     "certs": "ISO 9001\nISO 14001", "extra": "116M gal/yr. CCS active."},

    {"id": 7071, "facility": "Green Plains – York", "tier": "Captive",
     "city": "York", "country": "United States", "website": "https://www.gpreinc.com",
     "about": "Green Plains Inc.'s York, Nebraska corn bioethanol facility with active CCS.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Corn bioethanol fermentation\nCO₂ capture (CCS)",
     "certs": "ISO 9001\nISO 14001", "extra": "CCS active. York, Nebraska."},

    {"id": 7072, "facility": "Green Plains – Superior", "tier": "Captive",
     "city": "Superior", "country": "United States", "website": "https://www.gpreinc.com",
     "about": "Green Plains Inc.'s Superior, Iowa corn bioethanol facility, 60 million gal/yr. Reached the milestone of 1 billion gallons of ethanol produced in October 2026.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Corn bioethanol fermentation",
     "certs": "ISO 9001\nISO 14001", "extra": "60M gal/yr. 1 billionth gallon milestone October 2026."},

    {"id": 7073, "facility": "Green Plains – Fairmont", "tier": "Captive",
     "city": "Fairmont", "country": "United States", "website": "https://www.gpreinc.com",
     "about": "Green Plains Inc.'s Fairmont, Minnesota corn bioethanol facility, part of the nine-plant Midwest network.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Corn bioethanol fermentation",
     "certs": "ISO 9001\nISO 14001", "extra": "Part of Green Plains 9-plant Midwest network."},

    # ── RAÍZEN ────────────────────────────────────────────────────────────────
    {"id": 7074, "facility": "Raízen – Costa Pinto E2G (Piracicaba)", "tier": "Captive",
     "city": "Piracicaba", "country": "Brazil", "website": "https://www.raizen.com.br",
     "about": "Raízen's Costa Pinto mill in Piracicaba, São Paulo — home to the world's first industrial-scale second-generation (2G/E2G) cellulosic ethanol plant, producing ethanol from sugarcane bagasse. Raízen is the world's largest sugarcane ethanol producer (50/50 JV Shell/Cosan). The E2G technology was developed with Iogen.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "2G cellulosic ethanol from sugarcane bagasse and straw\nEnzymatic hydrolysis of cellulose and hemicellulose\nLignocellulosic fermentation\n1G conventional sugarcane ethanol co-production",
     "certs": "ISO 9001\nISO 14001\nRenovaBio",
     "extra": "World's first industrial-scale 2G cellulosic ethanol plant. Raízen = 50/50 JV Shell/Cosan. Iogen technology."},

    {"id": 7075, "facility": "Raízen – Bonfim E2G (Guariba)", "tier": "Captive",
     "city": "Guariba", "country": "Brazil", "website": "https://www.raizen.com.br",
     "about": "Raízen's Bonfim E2G unit in Guariba, São Paulo state — second-generation cellulosic ethanol from sugarcane bagasse. ~82 million litres/yr capacity. Part of Raízen's E2G network targeting 440 million litres/yr total by 2025/26.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "2G cellulosic ethanol from sugarcane bagasse\nEnzymatic hydrolysis and fermentation",
     "certs": "ISO 9001\nISO 14001\nRenovaBio",
     "extra": "~82M litres/yr 2G ethanol. Raízen E2G network."},

    {"id": 7076, "facility": "Raízen – Barra E2G (Barra Bonita)", "tier": "Captive",
     "city": "Barra Bonita", "country": "Brazil", "website": "https://www.raizen.com.br",
     "about": "Raízen's Barra E2G cellulosic ethanol unit in Barra Bonita, São Paulo state. ~82 million litres/yr of second-generation ethanol from sugarcane bagasse.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 3,
     "technologies": "2G cellulosic ethanol from sugarcane bagasse\nEnzymatic hydrolysis and fermentation",
     "certs": "ISO 9001\nISO 14001\nRenovaBio",
     "extra": "~82M litres/yr 2G ethanol. Barra Bonita, SP."},

    {"id": 7077, "facility": "Raízen – Univalem E2G (Valparaíso)", "tier": "Captive",
     "city": "Valparaíso", "country": "Brazil", "website": "https://www.raizen.com.br",
     "about": "Raízen's Univalem E2G cellulosic ethanol unit in Valparaíso, São Paulo state. Part of Raízen's expanding 2G network.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "2G cellulosic ethanol from sugarcane bagasse",
     "certs": "ISO 9001\nISO 14001\nRenovaBio",
     "extra": "Raízen E2G network expansion. Valparaíso, SP."},

    {"id": 7078, "facility": "Raízen – Vale do Rosário E2G (Morro Agudo)", "tier": "Captive",
     "city": "Morro Agudo", "country": "Brazil", "website": "https://www.raizen.com.br",
     "about": "Raízen's Vale do Rosário E2G cellulosic ethanol unit in Morro Agudo, São Paulo state. Part of the total 440 million litres/yr 2G network by 2025/26.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "2G cellulosic ethanol from sugarcane bagasse",
     "certs": "ISO 9001\nISO 14001\nRenovaBio",
     "extra": "440M litres/yr total E2G network target by 2025/26. Morro Agudo, SP."},

    # ── VERBIO ────────────────────────────────────────────────────────────────
    {"id": 7079, "facility": "Verbio – Schwedt/Oder Biorefinery", "tier": "Captive",
     "city": "Schwedt", "country": "Germany", "website": "https://www.verbio.de",
     "about": "Verbio's integrated bioethanol and biomethane production facility in Schwedt/Oder, Brandenburg, Germany. Produces grain-based bioethanol and biomethane (biogas from distillation residues/stillage). Over 10 years of operation.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Grain bioethanol fermentation\nBiomethane production from distillation stillage\nBiogas upgrading to biomethane",
     "certs": "ISO 9001\nISO 14001\nISCC",
     "extra": "10+ years operation. Grain bioethanol + biomethane from stillage. Schwedt/Oder, Brandenburg."},

    {"id": 7080, "facility": "Verbio – Zörbig Biorefinery", "tier": "Captive",
     "city": "Zörbig", "country": "Germany", "website": "https://www.verbio.de",
     "about": "Verbio's integrated bioethanol and biomethane biorefinery in Zörbig, Saxony-Anhalt. Grain-based bioethanol with biomethane production from distillation residues.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Grain bioethanol fermentation\nBiomethane from stillage",
     "certs": "ISO 9001\nISO 14001\nISCC", "extra": "Zörbig, Saxony-Anhalt. Integrated bioethanol + biomethane biorefinery."},

    {"id": 7081, "facility": "Verbio – Pinnow Straw Biomethane Plant", "tier": "Captive",
     "city": "Pinnow", "country": "Germany", "website": "https://www.verbio.de",
     "about": "Verbio's Pinnow facility in Brandenburg, Germany — the first stand-alone straw-to-biomethane plant. Converts agricultural straw residues (not grain) directly into biomethane by anaerobic fermentation.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Straw anaerobic fermentation to biogas\nBiomethane upgrading\nLignocellulosic feedstock pre-treatment",
     "certs": "ISO 9001\nISCC",
     "extra": "World's first stand-alone straw-to-biomethane plant. Pinnow, Brandenburg."},

    {"id": 7082, "facility": "Verbio – Nevada Iowa Biorefinery", "tier": "Captive",
     "city": "Nevada", "country": "United States", "website": "https://www.verbio.de",
     "about": "Verbio's North American flagship biorefinery in Nevada, Iowa — the first industrial facility in North America to combine bioethanol and biomethane production from corn and corn stover. Phase II expansion completed August 2024.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 4,
     "technologies": "Corn bioethanol fermentation\nBiomethane from corn stover and residues\nCombined bioethanol + biomethane co-production (first in North America)",
     "certs": "ISO 9001\nISO 14001\nISCC",
     "extra": "First industrial bioethanol + biomethane co-production in North America. Phase II August 2024. Nevada, Story County, Iowa."},

    {"id": 7083, "facility": "Verbio – South Bend Biorefinery", "tier": "Captive",
     "city": "South Bend", "country": "United States", "website": "https://www.verbio.de",
     "about": "Verbio's South Bend, Indiana biorefinery, acquired in 2023. Converting to combined bioethanol (250,000 t/yr) and biomethane (850,000 MWh/yr) production; biomethane expected from 2026.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 3,
     "technologies": "Bioethanol fermentation\nBiomethane production (from 2026)",
     "certs": "ISO 9001\nISO 14001\nISCC",
     "extra": "Acquired 2023. 250,000 t/yr ethanol + 850,000 MWh/yr biomethane from 2026."},

    # ── QUORN FOODS ───────────────────────────────────────────────────────────
    {"id": 7084, "facility": "Quorn – Billingham Mycoprotein Plant", "tier": "Captive",
     "city": "Billingham", "country": "United Kingdom", "website": "https://www.quorn.com",
     "about": "Quorn's Billingham (Belasis) plant in County Durham, UK — the world's largest mycoprotein fermentation facility. Produces Quorn mycoprotein by continuous submerged fermentation of Fusarium venenatum fungus. £150 million expansion underway. Operational since 1985. Owned by Monde Nissin (Philippines) since 2015.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Continuous submerged fermentation of Fusarium venenatum\nMycoprotein biomass harvesting and heat treatment\nMycoprotein texturisation",
     "certs": "ISO 9001\nISO 22000\nFSSC 22000",
     "extra": "World's largest mycoprotein plant. £150M expansion. Since 1985. Monde Nissin ownership. Continuous fermentation."},

    {"id": 7085, "facility": "Quorn – Stokesley Manufacturing", "tier": "Captive",
     "city": "Stokesley", "country": "United Kingdom", "website": "https://www.quorn.com",
     "about": "Quorn's Stokesley facility in North Yorkshire, UK, producing Quorn mycoprotein-based food products from the fermentation-derived mycoprotein ingredient produced at Billingham.",
     "tech_areas": "Fermentation (industrial)\nDownstream processing", "n_tech": 2,
     "technologies": "Mycoprotein food product manufacturing\nTexturisation and formed product production",
     "certs": "ISO 9001\nISO 22000", "extra": "Stokesley, North Yorkshire. Quorn product manufacturing."},

    {"id": 7086, "facility": "Quorn – Methwold Manufacturing", "tier": "Captive",
     "city": "Methwold", "country": "United Kingdom", "website": "https://www.quorn.com",
     "about": "Quorn's Methwold facility in Norfolk, UK, producing Quorn mycoprotein-based food products.",
     "tech_areas": "Fermentation (industrial)\nDownstream processing", "n_tech": 2,
     "technologies": "Mycoprotein food product manufacturing",
     "certs": "ISO 9001\nISO 22000", "extra": "Methwold, Norfolk. Quorn product manufacturing."},

    # ── PERFECT DAY ───────────────────────────────────────────────────────────
    {"id": 7087, "facility": "Perfect Day – Gujarat Fermentation Plant (Zydus JV)", "tier": "Captive",
     "city": "Ahmedabad", "country": "India", "website": "https://www.perfectday.com",
     "about": "Perfect Day's commercial-scale precision fermentation plant in Gujarat, India, developed in partnership with Zydus Lifesciences. Produces ProFerm™ beta-lactoglobulin (animal-free whey protein) by engineered yeast fermentation. Mechanical completion September 2026; first commercial deliveries Q4 2026. ~2,500 t/yr initial capacity.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Precision fermentation of beta-lactoglobulin by engineered yeast\nProtein concentration and purification\nProFerm™ whey protein ingredient production",
     "certs": "ISO 9001\nISO 22000\nGMP",
     "extra": "Zydus JV. Mechanical completion Sept 2026. ~2,500 t/yr ProFerm™ beta-lactoglobulin. First commercial deliveries Q4 2026."},

    # ── SOLAR FOODS ───────────────────────────────────────────────────────────
    {"id": 7088, "facility": "Solar Foods – Factory 01 (Vantaa)", "tier": "Captive",
     "city": "Vantaa", "country": "Finland", "website": "https://solarfoods.com",
     "about": "Solar Foods' Factory 01 in Vantaa, Finland — the world's first commercial facility producing Solein® single-cell protein from CO₂ and hydrogen by gas fermentation. Operational since April 2024. Capacity 160 t/yr, scaling to 230 t/yr in 2026. Solein is produced by autotrophic Ideonella bacteria without agricultural land or water.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Autotrophic gas fermentation (CO₂ + H₂ → Solein® protein)\nSolein® single-cell protein biomass harvesting\nProtein concentration and drying",
     "certs": "ISO 9001\nISO 22000",
     "extra": "World's first commercial CO₂+H₂ gas fermentation protein. Operational April 2024. 160→230 t/yr. No agricultural land needed."},

    {"id": 7089, "facility": "Solar Foods – Factory 02 (Lappeenranta)", "tier": "Pilot facility",
     "city": "Lappeenranta", "country": "Finland", "website": "https://solarfoods.com",
     "about": "Solar Foods' planned Factory 02 in Lappeenranta, Finland — a 40× scale-up from Factory 01, designed for large-scale Solein® protein production. Final investment decision (FID) during 2026; €77.8 million funded. Under development.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)", "n_tech": 2,
     "technologies": "Autotrophic gas fermentation at scale (CO₂ + H₂ → Solein®)",
     "certs": "ISO 9001", "extra": "40× scale-up of Factory 01. FID 2026. €77.8M funded. Under development/construction."},

    # ── CALYSTA / CALYSSEO ────────────────────────────────────────────────────
    {"id": 7090, "facility": "Calysseo – Nanjing FeedKind® Plant (Calysta + Adisseo JV)", "tier": "Captive",
     "city": "Nanjing", "country": "China", "website": "https://www.calysta.com",
     "about": "Calysseo's commercial FeedKind® single-cell protein plant in Nanjing, Jiangsu Province, China. A 50/50 joint venture between Calysta Inc. and Adisseo. Produces FeedKind® protein ingredient by methanotrophic fermentation (methane → biomass). Operational October 2022; 20,000 t/yr. Houses the world's largest gas fermenters (2 × 10,000-tonne units). Replaces fishmeal in aquaculture and animal feed.",
     "tech_areas": "Microbial fermentation\nFermentation (industrial)\nDownstream processing", "n_tech": 4,
     "technologies": "Methanotrophic gas fermentation (methane → single-cell protein)\nWorld's largest gas fermenters (2×10,000 t)\nFeedKind® SCP biomass harvesting and drying",
     "certs": "ISO 9001\nISO 22000",
     "extra": "50/50 JV Calysta + Adisseo. Operational Oct 2022. 20,000 t/yr. World's largest gas fermenters (2×10,000 t). FeedKind® replaces fishmeal."},
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
