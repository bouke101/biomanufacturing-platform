"""
Add 'Main products' and 'Annual capacity (est.)' columns to the Excel,
populate data for major multinational industrial biotech companies.
Run with: python3 scripts/update_products_capacity.py
"""
import openpyxl
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# keyed by integer facility ID → (main_products, annual_capacity)
DATA: dict[int, tuple[str, str]] = {

    # ── BASF ──────────────────────────────────────────────────────────────────
    20: (
        "Vitamin B2 (riboflavin, Ashbya gossypii fermentation)\n"
        "Specialty biotech enzymes and biotransformation products",
        "Riboflavin: ~3,000–5,000 MT/yr (one of world's top 2 producers)"
    ),

    # ── Ennolys / Lesaffre ────────────────────────────────────────────────────
    66: (
        "trans-Resveratrol (natural, Botrytis cinerea fermentation)\n"
        "Polyphenols by yeast fermentation",
        "Resveratrol: ~10–30 MT/yr (niche premium ingredient)"
    ),

    # ── Lonza CDMOs ───────────────────────────────────────────────────────────
    140: (
        "Mammalian cell culture biologics (monoclonal antibodies, fusion proteins)\n"
        "Contract biologics manufacturing (CDMO)",
        "CDMO — capacity by contract; >10 × 15,000 L bioreactors at Portsmouth campus"
    ),
    141: (
        "Mammalian cell culture biologics (CDMO)\n"
        "Gene therapy viral vectors",
        "CDMO — capacity by contract; major Hopkinton campus"
    ),
    142: (
        "Mammalian cell culture biologics (mAbs, fusion proteins, CDMO)",
        "CDMO — capacity by contract; Vacaville ~90,000 L total bioreactor volume"
    ),
    216: (
        "Pharmaceutical APIs and intermediates (CDMO)\n"
        "Small-molecule and large-molecule synthesis\n"
        "Nicotinamide, Vitamin B3",
        "CDMO — capacity by contract; Visp is Lonza's largest site"
    ),
    231: (
        "Microbial fermentation products (CDMO)\n"
        "Bacterial and yeast-derived APIs and biologics",
        "CDMO — capacity by contract; microbial fermentation specialist"
    ),
    235: (
        "Mammalian cell culture biologics (CDMO)",
        "CDMO — capacity by contract"
    ),

    # ── Ajinomoto Bio-Pharma (CDMO) ───────────────────────────────────────────
    161: (
        "Pharmaceutical amino acid-based APIs and intermediates (CDMO)\n"
        "Injectable-grade amino acid formulations",
        "CDMO — contract volumes undisclosed"
    ),
    222: (
        "Pharmaceutical amino acids and specialty chemicals (CDMO)",
        "CDMO — contract volumes undisclosed"
    ),

    # ── Novonesis / Novozymes ─────────────────────────────────────────────────
    225: (
        "Industrial enzymes: amylases, lipases, proteases, cellulases\n"
        "Food enzymes (lactase, pectinase, glucose oxidase)\n"
        "Biofuel enzymes (cellulases, xylanases)",
        "~80% of Novonesis global enzyme production; est. ~80,000–100,000 MT/yr total enzyme products"
    ),
    271: (
        "Industrial enzymes for biofuels and agriculture\n"
        "Biological crop protection agents",
        "Several thousand MT/yr enzymes (North American production satellite)"
    ),

    # ── dsm-firmenich ─────────────────────────────────────────────────────────
    226: (
        "Enzymes: Maxazyme® (protein cross-linking), Tolerase G® (gluten tolerance)\n"
        "MaxilactLGX™ (lactase)\n"
        "HMO pilot fermentation",
        "Enzyme production: volumes not disclosed; global R&D and biotech innovation campus"
    ),
    227: (
        "Vitamin E (all-rac-α-tocopheryl acetate, RRR-α-tocopherol)\n"
        "Vitamin A (retinyl acetate, retinyl palmitate)\n"
        "Astaxanthin (Lucarotin®, algal source)\n"
        "Omega-3 fish oil concentrate (Meg-3®)",
        "Vitamin E: ~20,000–25,000 MT/yr\n"
        "Vitamin A: ~3,000–5,000 MT/yr\n"
        "Carotenoids (astaxanthin, beta-carotene): hundreds of MT/yr"
    ),
    272: (
        "Vitamin C (L-ascorbic acid, two-step fermentation)\n"
        "Vitamin E\n"
        "Carotenoids (beta-carotene, lycopene)",
        "Vitamin C: ~10,000–15,000 MT/yr\n"
        "Vitamin E: several thousand MT/yr"
    ),

    # ── CJ CheilJedang ────────────────────────────────────────────────────────
    228: (
        "L-Lysine HCl 98.5% (CJ Bio™ Lysine, feed grade)\n"
        "L-Tryptophan (CJ Bio™ Tryptophan)\n"
        "L-Threonine (CJ Bio™ Threonine)\n"
        "L-Valine\nL-Isoleucine",
        "L-Lysine: ~500,000 MT/yr (Incheon; CJ total global >1,000,000 MT/yr)\n"
        "L-Tryptophan: ~30,000 MT/yr\n"
        "L-Threonine: ~200,000 MT/yr"
    ),

    # ── Evonik Health Care Hanau ──────────────────────────────────────────────
    229: (
        "Pharmaceutical-grade L-amino acids (parenteral nutrition grade)\n"
        "L-methionine (pharma)\nGlycine (pharma)\nL-alanine (pharma)",
        "Pharma amino acids: ~500–2,000 MT/yr combined (GMP-grade, high value)"
    ),

    # ── Cargill Blair ─────────────────────────────────────────────────────────
    298: (
        "L-Lysine HCl (feed grade, corn-fermentation)\n"
        "Lysine liquid (70% solution)",
        "L-Lysine: ~200,000 MT/yr"
    ),

    # ── dsm-firmenich 5xxx range ──────────────────────────────────────────────
    5001: (
        "Nutritional premixes (Quali-Blends™ vitamin/mineral/amino acid premixes)\n"
        "Pharmaceutical vitamin formulations\n"
        "Microencapsulated and coated vitamins",
        "Premixes and vitamin formulations: tens of thousands MT/yr"
    ),
    5002: (
        "Vitamin D3 (cholecalciferol, from lanolin wool-grease photosynthesis)\n"
        "Vitamin D2 (ergocalciferol)\n"
        "D3 oil solutions and emulsions (human and animal nutrition grades)",
        "Vitamin D3 pure: ~500–900 MT/yr (world's largest single D3 plant; "
        "~20–30% of global supply)"
    ),
    5003: (
        "Natamycin (DelvoCid®, natural antifungal food preservative)\n"
        "Specialty food enzymes\n"
        "Functional dairy ingredients",
        "Natamycin: ~1,000–2,000 MT/yr"
    ),
    5004: (
        "Fine fragrance compounds and bases (Firmenich heritage)\n"
        "Perfumery ingredients (musks, florals, aromatic chemicals)\n"
        "Encapsulated fragrance ingredients\n"
        "Flavor creation and application",
        "Fragrance ingredients: tens of thousands MT/yr; exact volumes confidential"
    ),
    5005: (
        "Vitamin and mineral premixes (animal and human nutrition)\n"
        "Feed-grade micronutrient blends",
        "Premix blends: several thousand MT/yr"
    ),
    5006: (
        "Animal nutrition premixes and supplements (Tortuga brand)\n"
        "Mineral licks and feed blocks for Brazilian livestock\n"
        "Feed additives and mineral mixes",
        "Animal nutrition products: tens of thousands MT/yr (largest Brazilian animal nutrition brand)"
    ),
    5007: (
        "Industrial enzymes: amylases (Spirizyme®, Termamyl®), lipases, proteases\n"
        "Biofuel enzymes (Cellic® CTec3)\n"
        "Agricultural bioprotection (Taegro®, Actinovate®)\n"
        "Food enzymes (Novozym® 435 lipase, Palatase®)\n"
        "Laundry enzymes (Mannaway®, Lipolase®)",
        "~80,000–100,000 MT/yr total fermentation output (crude enzyme broth); "
        "concentrated enzyme products ~20,000–30,000 MT/yr; "
        "~85% of Novonesis global enzyme volume"
    ),
    5008: (
        "Dairy starter cultures (Chr. Hansen heritage): yogurt (Yo-Mix®), "
        "cheese (DVS® Direct Vat Set), butter, sour cream\n"
        "Probiotic cultures (HN001™ Lactobacillus rhamnosus, BB-12® Bifidobacterium)\n"
        "Food protection cultures (FreshQ®, SafePro®)\n"
        "Wine and kombucha cultures",
        "Cultures and probiotics: hundreds of MT/yr freeze-dried (high CFU concentrates)"
    ),
    5009: (
        "Enzymes for North American biofuel and agriculture markets\n"
        "Biological crop protection agents",
        "Several thousand MT/yr (North American enzyme production satellite)"
    ),
    5010: (
        "Food cultures, probiotics (Chr. Hansen legacy production site)\n"
        "Dairy and specialty fermentation cultures",
        "Hundreds of MT/yr freeze-dried cultures and probiotics"
    ),
    5011: (
        "Dairy starter cultures (yogurt, cheese, butter)\n"
        "Probiotic blends for food and beverage applications",
        "Hundreds of MT/yr freeze-dried cultures"
    ),
    5012: (
        "Algal DHA + EPA omega-3 oil (Veramaris® 50% DHA+EPA)\n"
        "Animal-free omega-3 for salmon aquaculture and pet nutrition",
        "~15,000 MT/yr algal omega-3 oil (Veramaris®)"
    ),
    5013: (
        "Canthaxanthin (Carophyll® Red, feed and food grade)\n"
        "Beta-carotene (Carophyll® Yellow)\n"
        "Apocarotenal (Carophyll® Roche-orange)",
        "Canthaxanthin: ~100–300 MT/yr\n"
        "Beta-carotene: ~200–500 MT/yr"
    ),
    5014: (
        "Encapsulated flavor ingredients (Firmenich heritage)\n"
        "Fragrance ingredients for personal care and home care\n"
        "Spray-dried flavor emulsions\n"
        "Taste molecules (fermentation-derived)",
        "Flavors and fragrances: several thousand MT/yr"
    ),
    5015: (
        "Pilot fermentation for taste, flavor and functional ingredients\n"
        "Customer co-creation and scale-up",
        "Pilot scale only — not commercial production"
    ),
    5016: (
        "Vitamin and mineral premixes (Quali-Blends™)\n"
        "Custom nutritional blends for food fortification\n"
        "Dietary supplement premixes",
        "Several thousand MT/yr premix blends"
    ),
    5017: (
        "Custom vitamin, mineral and amino acid premixes for pet food\n"
        "Micro-dosed specialty ingredient blends",
        "Thousands of MT/yr pet nutrition premixes"
    ),

    # ── IFF 6001–6008 ─────────────────────────────────────────────────────────
    6001: (
        "Food cultures for dairy (yogurt, cheese, sour cream, kefir)\n"
        "Meat and vegetable fermentation cultures\n"
        "Probiotics (Lactobacillus strains, FloraFIT® range)",
        "Food cultures: hundreds of MT/yr freeze-dried\n"
        "Probiotics: tens of MT/yr concentrated biomass"
    ),
    6002: (
        "Functional protein hydrolysates (AMIZATE®, COLLATE™)\n"
        "Yeast-derived flavor proteins\n"
        "Specialty dairy protein fractions",
        "Protein hydrolysates: several thousand MT/yr"
    ),
    6003: (
        "Culture innovation and enzyme R&D\n"
        "Pilot production for new fermentation products",
        "Pilot scale — R&D and innovation campus"
    ),
    6004: (
        "Baking enzymes (Grindamyl® xylanase, amylase, lipase)\n"
        "Food-processing enzymes (lactase, pectinase, glucose oxidase)\n"
        "Animal feed enzymes",
        "Food and feed enzymes: thousands of MT/yr"
    ),
    6005: (
        "Industrial biofuel enzymes (Accellerase® cellulase complex, "
        "Stellar™ glucoamylase)\n"
        "Grain processing enzymes (amylase, glucoamylase)\n"
        "Biobased chemical enzymes",
        "Industrial enzymes: tens of thousands MT/yr (major Genencor heritage site)"
    ),
    6006: (
        "Probiotics (Lactobacillus acidophilus, Bifidobacterium strains)\n"
        "Dairy starter cultures for European food industry",
        "Probiotics and cultures: hundreds of MT/yr"
    ),
    6007: (
        "Enzyme discovery, R&D and pilot production (Genencor heritage)\n"
        "Protein engineering and directed evolution",
        "Pilot scale — enzyme R&D"
    ),
    6008: (
        "Food and industrial enzymes for Latin American markets\n"
        "Regional enzyme production satellite",
        "Several thousand MT/yr enzymes"
    ),

    # ── Evonik 6009–6015 ──────────────────────────────────────────────────────
    6009: (
        "DL-Methionine (MetAMINO®, feed grade)",
        "~250,000 MT/yr DL-methionine"
    ),
    6010: (
        "DL-Methionine (MetAMINO®, feed grade)",
        "~300,000 MT/yr DL-methionine (world's largest single methionine plant)"
    ),
    6011: (
        "3-Methylthiopropionaldehyde (MMP, methionine precursor)\n"
        "Methionine synthetic intermediates",
        "Methionine intermediates: hundreds of thousands MT/yr"
    ),
    6012: (
        "DL-Methionine (MetAMINO®, feed grade)",
        "~200,000 MT/yr DL-methionine"
    ),
    6013: (
        "L-Threonine (BioAMINO®, fermentation-derived, feed grade)\n"
        "L-Tryptophan (BioAMINO®, fermentation-derived)",
        "L-Threonine: ~100,000 MT/yr\n"
        "L-Tryptophan: ~15,000–20,000 MT/yr"
    ),
    6014: (
        "Pharmaceutical-grade L-cysteine (REXIM® Cys)\n"
        "L-Methionine (pharma grade)\n"
        "N-Acetyl-L-cysteine (NAC)\n"
        "Glycine (pharma grade)",
        "Pharmaceutical amino acids: ~500–1,500 MT/yr combined (GMP-compliant)"
    ),
    6015: (
        "Pharmaceutical and specialty amino acids for Asian markets\n"
        "L-Cysteine, L-methionine derivatives (REXIM® China)",
        "Specialty pharma amino acids: hundreds to ~1,000 MT/yr"
    ),

    # ── Kerry 6016–6023 ───────────────────────────────────────────────────────
    6016: (
        "Food enzymes (lipase, protease, amylase)\n"
        "Probiotics (Lactobacillus, Bifidobacterium strains)\n"
        "Fermented dairy and beverage ingredients",
        "Enzymes: several hundred MT/yr\n"
        "Probiotics: tens of MT/yr concentrated"
    ),
    6017: (
        "Custom industrial biocatalysts (enzyme engineering, C-LEcta heritage)\n"
        "Enzyme discovery and directed evolution",
        "Pilot to commercial-scale biocatalysts; volumes by project"
    ),
    6018: (
        "Yeast extracts for savory flavors\n"
        "Fermentation-derived umami and taste ingredients\n"
        "Specialty flavor compounds",
        "Yeast extracts: several thousand MT/yr"
    ),
    6019: (
        "Dairy starter cultures (cheese, yogurt, cultured butter)\n"
        "Propionibacterium cultures (Swiss-type cheese eyes)\n"
        "Specialty dairy cultures",
        "Dairy cultures: hundreds of MT/yr"
    ),
    6020: (
        "L. plantarum HEAL9® (respiratory health probiotic)\n"
        "Clinically validated probiotic strains\n"
        "Encapsulated probiotic ingredients",
        "Probiotics: tens of MT/yr (concentrated, clinical-grade)"
    ),
    6021: (
        "Taste and texture ingredients for Asian food markets\n"
        "Fermentation-derived savory and umami flavors",
        "Taste ingredients: thousands of MT/yr"
    ),
    6022: (
        "Fermentation-derived taste and texture ingredients\n"
        "Savory and umami ingredients for SE Asian food industry",
        "Thousands of MT/yr food taste ingredients"
    ),
    6023: (
        "Savory and umami fermentation flavors\n"
        "Fermented plant-based flavor extracts",
        "Several thousand MT/yr savory ingredients"
    ),

    # ── Cargill / JVs 6024–6029 ───────────────────────────────────────────────
    6024: (
        "Bio-based 1,3-propanediol (PDO) from corn glucose\n"
        "PDO for polytrimethylene terephthalate (PTT) fibers and polyurethanes",
        "Bio-based 1,3-PDO: ~65,000 MT/yr"
    ),
    6025: (
        "Ingeo™ polylactic acid (PLA) biopolymer\n"
        "Ingeo™ PLA grades: fiber, film, rigid packaging, foam, 3D printing",
        "~75,000 MT/yr Ingeo™ PLA"
    ),
    6026: (
        "Corn bioethanol\n"
        "Distillers dried grains with solubles (DDGS)\n"
        "Corn oil (distillers corn oil, DCO)",
        "~100M gal/yr (~380,000 MT/yr) bioethanol"
    ),
    6027: (
        "ABUNDA® mycoprotein (Fusarium venenatum fermentation)\n"
        "Mycoprotein ingredient for meat alternatives and food applications",
        "~20,000 MT/yr ABUNDA® mycoprotein (scaling to 50,000 MT/yr)"
    ),
    6028: (
        "Wheat starch (native, modified)\n"
        "Wheat glucose syrup and dextrose\n"
        "Vital wheat gluten\n"
        "Maltodextrin and cyclodextrin",
        "Wheat starch + derivatives: ~150,000–200,000 MT/yr"
    ),
    6029: (
        "Wheat starch (native, modified)\n"
        "Wheat glucose and dextrose\n"
        "Vital wheat gluten\n"
        "Bioethanol (from wheat processing)",
        "Wheat starch + derivatives: ~100,000–150,000 MT/yr\n"
        "Bioethanol: ~50–100M gal/yr"
    ),

    # ── ADM 6030–6035 ─────────────────────────────────────────────────────────
    6030: (
        "Precision fermentation specialty ingredients (pilot and commercial scale)\n"
        "Lactic acid (corn-based fermentation)\n"
        "Biobased chemicals",
        "Precision fermentation hub; exact volumes not publicly disclosed"
    ),
    6031: (
        "High-fructose corn syrup (HFCS-55, HFCS-42)\n"
        "Dextrose (glucose, food and industrial grade)\n"
        "Corn starch and starch derivatives\n"
        "Bioethanol\n"
        "Corn oil and corn gluten meal/feed",
        "HFCS: ~500,000 MT/yr (est.)\n"
        "Dextrose: ~200,000 MT/yr (est.)\n"
        "Bioethanol: ~300M gal/yr (est.)"
    ),
    6032: (
        "Corn bioethanol\n"
        "CO₂ (captured via geological CCS)",
        "~100M gal/yr (~380,000 MT/yr) bioethanol\n"
        "CCS: ~500,000 MT/yr CO₂ captured and stored"
    ),
    6033: (
        "Corn bioethanol\n"
        "DDGS\n"
        "Distillers corn oil",
        "~100M gal/yr bioethanol"
    ),
    6034: (
        "Natural flavors and flavor extracts (fruit, botanical, vegetable)\n"
        "Natural colorants and juice concentrates\n"
        "Botanical extracts and functional food ingredients",
        "Natural flavors and extracts: thousands of MT/yr"
    ),
    6035: (
        "Natural flavors, flavor compounds and blends\n"
        "Food ingredient solutions",
        "Thousands of MT/yr natural flavor products"
    ),

    # ── Chinese producers 3xxx ────────────────────────────────────────────────
    3001: (
        "L-Glutamic acid (MSG precursor)\n"
        "L-Lysine HCl (feed grade)\n"
        "L-Threonine\n"
        "Xanthan gum\n"
        "Corn starch and derivatives",
        "L-Glutamic acid: ~500,000 MT/yr\n"
        "L-Lysine HCl: ~300,000–500,000 MT/yr\n"
        "Xanthan gum: ~50,000 MT/yr"
    ),
    3002: (
        "MSG (monosodium glutamate, AJI-NO-MOTO® equivalent)\n"
        "Xanthan gum\n"
        "L-Threonine\n"
        "Corn starch and glucose syrup",
        "MSG: ~900,000 MT/yr (world's largest single MSG company)\n"
        "Xanthan gum: ~100,000 MT/yr (world's #1 xanthan producer)\n"
        "L-Threonine: ~200,000 MT/yr"
    ),
    3003: (
        "L-Lysine HCl (feed grade)\n"
        "L-Threonine\n"
        "Other feed amino acids",
        "L-Lysine: ~200,000–300,000 MT/yr"
    ),
    3006: (
        "Baker's yeast (fresh, active dry, instant dry)\n"
        "Specialty yeast for Chinese bakery and food market",
        "Baker's yeast: ~20,000–40,000 MT/yr (wet weight)"
    ),
    3007: (
        "Bioethanol (corn-based)\n"
        "Lactic acid (corn fermentation)\n"
        "Corn starch and glucose\n"
        "Amino acids",
        "Bioethanol: ~300M liters/yr\n"
        "Lactic acid: ~50,000–80,000 MT/yr"
    ),
    3010: (
        "Industrial enzymes for Chinese market (amylases, proteases, lipases)\n"
        "Agricultural bioprotection enzymes",
        "Several thousand MT/yr enzymes (Novonesis China production)"
    ),
    3015: (
        "Corn bioethanol\n"
        "Corn starch, glucose syrup and HFCS\n"
        "Amino acids\n"
        "CO₂ (food grade, from fermentation)",
        "Bioethanol: ~1 billion liters/yr\n"
        "Starch/glucose: hundreds of thousands MT/yr"
    ),
    3019: (
        "Corn starch (native, modified)\n"
        "Maltodextrin\n"
        "Glucose syrups and dextrose\n"
        "Sorbitol and mannitol (polyols)",
        "Corn starch + derivatives: ~100,000–200,000 MT/yr"
    ),
    3021: (
        "Food and probiotic cultures for Chinese market\n"
        "Industrial enzymes (amylase, protease, cellulase)\n"
        "Specialty fermentation ingredients",
        "Cultures and enzymes: thousands of MT/yr combined"
    ),

    # ── Ajinomoto industrial ──────────────────────────────────────────────────
    4001: (
        "MSG (AJI-NO-MOTO® monosodium glutamate)\n"
        "L-Glutamic acid\n"
        "Aspartame (Equal® co-production, Tokai)\n"
        "Nucleotides (5'-IMP, 5'-GMP, IMP·GMP blend)\n"
        "L-Lysine, L-Threonine (food and feed grade)",
        "MSG: Tokai est. ~50,000–100,000 MT/yr (Ajinomoto global: ~600,000 MT/yr)\n"
        "Nucleotides: ~10,000–15,000 MT/yr\n"
        "Amino acids: ~50,000–100,000 MT/yr (Tokai share)"
    ),

    # ── CJ CheilJedang Bio (Incheon, ID 4009 — may overlap with 228) ─────────
    4009: (
        "L-Lysine HCl and sulfate (CJ Bio™, largest global lysine producer)\n"
        "L-Tryptophan\nL-Threonine\nL-Valine\nL-Isoleucine",
        "L-Lysine: CJ Bio global >1,000,000 MT/yr total; "
        "Incheon core site est. ~500,000 MT/yr\n"
        "L-Tryptophan: ~30,000 MT/yr\n"
        "L-Threonine: ~200,000 MT/yr"
    ),

    # ── Novonesis 5007–5011 (already covered above for 225, 271) ─────────────

    # ── Lallemand 7001–7009 ───────────────────────────────────────────────────
    7001: (
        "Baker's yeast (Saccharomyces cerevisiae): fresh cream, compressed, "
        "active dry, instant dry\n"
        "Wine yeast (Bourgovin RC 212®, Lalvin™ range)\n"
        "Distilling yeast (SafSpirit American Whiskey™)\n"
        "Selenium-enriched yeast (Selplex® equivalent)",
        "Baker's yeast: ~30,000–50,000 MT/yr (wet weight)\n"
        "Specialty yeast: hundreds of MT/yr"
    ),
    7002: (
        "Baker's yeast (fresh compressed, active dry yeast)\n"
        "Cream yeast",
        "Baker's yeast: ~20,000–30,000 MT/yr (wet weight)"
    ),
    7003: (
        "Baker's yeast (fresh compressed)\n"
        "Cream yeast for food manufacturers",
        "Baker's yeast: ~10,000–20,000 MT/yr"
    ),
    7004: (
        "Baker's yeast (fresh compressed)",
        "Baker's yeast: ~5,000–10,000 MT/yr"
    ),
    7005: (
        "Lactic acid bacteria (LAB) cultures for wine, dairy and feed\n"
        "Probiotic bacteria (Lactobacillus, Bifidobacterium, Enterococcus strains)\n"
        "Freeze-dried bacterial culture concentrates",
        "Bacteria cultures and probiotics: hundreds of MT/yr freeze-dried"
    ),
    7006: (
        "LAB bacteria cultures for oenology (wine malolactic fermentation)\n"
        "Dairy and feed bacteria cultures\n"
        "Freeze-dried culture concentrates (industrial scale)",
        "Bacteria cultures: hundreds of MT/yr freeze-dried"
    ),
    7007: (
        "Organic-certified cream yeast\n"
        "Specialty baker's yeast (organic range)",
        "Baker's yeast: ~5,000–15,000 MT/yr (organic cream yeast specialist)"
    ),
    7008: (
        "Baker's yeast (compressed, active dry)\n"
        "Specialty yeast (European market)",
        "Baker's yeast: ~10,000–20,000 MT/yr"
    ),
    7009: (
        "Lactic acid bacteria cultures (LAB) for food, feed and agriculture\n"
        "Probiotic bacteria for food and supplements\n"
        "Freeze-dried culture concentrates",
        "Bacteria cultures and probiotics: hundreds of MT/yr freeze-dried"
    ),

    # ── AB Mauri 7010–7015 ────────────────────────────────────────────────────
    7010: (
        "Compressed baker's yeast\n"
        "Active dry yeast (ADY)\n"
        "Instant dry yeast (IDY)\n"
        "Cream yeast",
        "~50,000–80,000 MT/yr baker's yeast (wet weight; Europe's largest single yeast plant)"
    ),
    7011: (
        "Baker's yeast (cream yeast, compressed, ADY, IDY)\n"
        "Specialty yeast blends",
        "~15,000–25,000 MT/yr baker's yeast"
    ),
    7012: (
        "Fresh baker's yeast\n"
        "Active dry yeast",
        "~5,000–10,000 MT/yr baker's yeast"
    ),
    7013: (
        "Fresh baker's yeast",
        "~5,000–10,000 MT/yr baker's yeast"
    ),
    7014: (
        "Baker's yeast (compressed, ADY, IDY)\n"
        "Cream yeast",
        "~10,000–20,000 MT/yr baker's yeast"
    ),
    7015: (
        "Baker's yeast (fresh compressed, ADY)\n"
        "Cream yeast for Latin American markets",
        "~10,000–20,000 MT/yr baker's yeast"
    ),

    # ── Ohly 7016–7018 ────────────────────────────────────────────────────────
    7016: (
        "Autolyzed yeast extracts (high-nucleotide, low-salt, organic)\n"
        "Yeast cell walls (beta-1,3/1,6-glucan, mannan)\n"
        "Specialty flavor yeast extracts (umami, roast, dairy notes)\n"
        "Fermentation media nutrients (yeast nitrogen base, autolysates)",
        "Yeast extracts: ~20,000–40,000 MT/yr (dry weight; including +50% expansion)"
    ),
    7017: (
        "Torula yeast extracts (Cyberlindnera jadinii)\n"
        "Specialty yeast extracts with distinctive flavor profiles\n"
        "Fermentation media nutrients",
        "Torula yeast extracts: ~3,000–8,000 MT/yr"
    ),
    7018: (
        "Spray-dried yeast extracts (autolyzed, hydrolyzed)\n"
        "Natural flavor yeast extracts",
        "Yeast extracts: ~5,000–10,000 MT/yr"
    ),

    # ── Lesaffre 7019–7023 ────────────────────────────────────────────────────
    7019: (
        "Baker's yeast (fresh compressed, active dry, instant dry)\n"
        "Specialty yeast (oenological, distilling, nutritional)\n"
        "Bread improvement ingredients (Ibis range)\n"
        "Fermentation-derived health ingredients",
        "Baker's yeast: >100,000 MT/yr (wet weight; world's largest single baker's yeast plant)"
    ),
    7020: (
        "Baker's yeast (compressed, ADY, IDY) — Algist Bruggeman brand\n"
        "Craft and specialty yeast",
        "Baker's yeast: ~20,000–40,000 MT/yr"
    ),
    7021: (
        "Yeast extracts (autolyzed): nutritional, flavoring and fermentation media grades\n"
        "High-nucleotide yeast extracts (Biospringer™ range)\n"
        "Yeast-derived ingredients for food and beverage",
        "Yeast extracts: ~10,000–20,000 MT/yr (post-2024 expansion)"
    ),
    7022: (
        "Baker's yeast (compressed, ADY) for Brazilian and Latin American market",
        "Baker's yeast: ~10,000–20,000 MT/yr"
    ),
    7023: (
        "Baker's yeast (fresh, ADY) for Indonesian and SE Asian market",
        "Baker's yeast: ~5,000–15,000 MT/yr"
    ),

    # ── AB Enzymes 7024–7025 ──────────────────────────────────────────────────
    7024: (
        "Baking enzymes (Veron® xylanase, amylase, lipase — world-leading baking enzyme brand)\n"
        "Animal feed enzymes (RONOZYME® equivalent: phytase, xylanase, protease)\n"
        "Textile processing enzymes (cellulase, laccase)\n"
        "Brewing and distilling enzymes",
        "Industrial enzymes: ~10,000–20,000 MT/yr"
    ),
    7025: (
        "Enzyme R&D and application development (baking, feed, textile, industrial)\n"
        "Pilot enzyme production",
        "Pilot scale — R&D and application development"
    ),

    # ── Sensient 7026–7028 ────────────────────────────────────────────────────
    7026: (
        "Autolyzed yeast extracts (Sensient Yeast™)\n"
        "High-glutamate yeast extracts for fermentation media\n"
        "Natural flavor-active yeast extracts",
        "Yeast extracts: ~10,000–15,000 MT/yr"
    ),
    7027: (
        "Fermentation-derived colors (carotenoids, riboflavin-based)\n"
        "Yeast-based fermentation nutrients for dairy cultures\n"
        "Natural color formulations",
        "Fermentation ingredients: thousands of MT/yr"
    ),
    7028: (
        "Natural color extracts (anthocyanins, carotenoids, beetroot, paprika)\n"
        "Fermentation-derived natural colors\n"
        "Color formulations for food and beverage",
        "Natural colors: ~50,000–100,000 MT/yr (liquid extracts and solutions; "
        "up to $250M expansion 2025)"
    ),

    # ── Kyowa Hakko Bio 7029–7031 ─────────────────────────────────────────────
    7029: (
        "L-Glutamine\n"
        "L-Arginine\n"
        "L-Citrulline\n"
        "L-Histidine\n"
        "Cognizin® citicoline (CDP-choline)\n"
        "Setria® L-Glutathione\n"
        "5'-IMP and 5'-GMP nucleotides",
        "Specialty amino acids: ~10,000–20,000 MT/yr combined\n"
        "Cognizin® citicoline: hundreds of MT/yr\n"
        "Setria® L-glutathione: tens of MT/yr"
    ),
    7030: (
        "Feed-grade amino acids (L-lysine, L-threonine, branched-chain)\n"
        "Fermentation specialty chemicals",
        "Feed amino acids: several thousand MT/yr"
    ),
    7031: (
        "2'-Fucosyllactose (2'-FL, HMO)\n"
        "3'-Sialyllactose (3'-SL, HMO)\n"
        "6'-Sialyllactose (6'-SL, HMO)\n"
        "L-Amino acids (site also produces amino acids)",
        "HMOs total: ~300 MT/yr (first dedicated HMO plant in SE Asia, 2022)\n"
        "Amino acids: thousands of MT/yr"
    ),

    # ── Global Bio-Chem 7032 ──────────────────────────────────────────────────
    7032: (
        "L-Lysine HCl 98.5% (feed grade, corn fermentation)\n"
        "L-Lysine 65% liquid solution\n"
        "L-Glutamic acid\n"
        "L-Threonine\n"
        "Corn starch and glucose",
        "L-Lysine: ~200,000–300,000 MT/yr\n"
        "L-Threonine: ~50,000–100,000 MT/yr\n"
        "L-Glutamic acid: ~100,000 MT/yr"
    ),

    # ── Vedan 7033–7035 ───────────────────────────────────────────────────────
    7033: (
        "MSG (monosodium glutamate)\n"
        "L-Lysine HCl\n"
        "Polyglutamic acid (γ-PGA, cosmetic and agricultural grade)\n"
        "Glucose syrup and starch derivatives\n"
        "Modified starch and cassava products",
        "MSG: ~150,000–200,000 MT/yr\n"
        "L-Lysine: ~50,000 MT/yr\n"
        "γ-PGA: ~3,000–5,000 MT/yr"
    ),
    7034: (
        "MSG (monosodium glutamate)\n"
        "Fermentation-derived seasonings",
        "MSG: ~50,000–80,000 MT/yr (Chinese domestic market)"
    ),
    7035: (
        "MSG (monosodium glutamate) — founding site 1954",
        "MSG: ~20,000–50,000 MT/yr (reduced scale vs. peak)"
    ),

    # ── Zhejiang NHU 7036–7039 ────────────────────────────────────────────────
    7036: (
        "Vitamin E (all-rac-α-tocopheryl acetate)\n"
        "Vitamin A palmitate and acetate\n"
        "Vitamin D3 (cholecalciferol)\n"
        "Animal nutrition vitamin products",
        "Vitamin E: ~15,000–25,000 MT/yr (world top-3 producer)\n"
        "Vitamin A: ~5,000–8,000 MT/yr\n"
        "Vitamin D3: ~500–1,000 MT/yr"
    ),
    7037: (
        "Astaxanthin (fermentation and extraction)\n"
        "Lutein\n"
        "Taurine\n"
        "Vitamin B6 (pyridoxine)\n"
        "Specialty bioactive compounds",
        "Taurine: ~10,000 MT/yr\n"
        "Astaxanthin: ~100–200 MT/yr\n"
        "Lutein: hundreds of MT/yr"
    ),
    7038: (
        "Linalool (fragrance)\n"
        "Geraniol (fragrance and flavor)\n"
        "Vitamin E intermediates and derivatives\n"
        "Flavour and fragrance specialty chemicals",
        "Flavour/fragrance chemicals: ~10,000–20,000 MT/yr combined\n"
        "NHU's largest production base"
    ),
    7039: (
        "Coenzyme Q10 (CoQ10, by fermentation)\n"
        "Vitamin C (ascorbic acid, two-step fermentation)\n"
        "Vitamin B12 (cyanocobalamin)\n"
        "Calcium pantothenate (Vitamin B5)\n"
        "L-Serine",
        "Vitamin C: ~30,000 MT/yr\n"
        "Calcium pantothenate: ~3,000–5,000 MT/yr\n"
        "CoQ10: ~100–200 MT/yr\n"
        "Vitamin B12: ~50–100 MT/yr"
    ),

    # ── NEPG 7040 ─────────────────────────────────────────────────────────────
    7040: (
        "Vitamin C (L-ascorbic acid, two-step fermentation — NEPG-invented process)\n"
        "Vitamin C derivatives (sodium ascorbate, calcium ascorbate, ascorbyl palmitate)\n"
        "Vitamin B12 (cyanocobalamin)",
        "Vitamin C: ~80,000–100,000 MT/yr (world's largest single Vitamin C producer)"
    ),

    # ── Anhui Tiger Biotech 7041 ──────────────────────────────────────────────
    7041: (
        "Vitamin C (ascorbic acid) and derivatives (ascorbyl palmitate, calcium ascorbate)\n"
        "Biotin (Vitamin B7/H)\n"
        "Calcium pantothenate (Vitamin B5)\n"
        "Folic acid (Vitamin B9)\n"
        "Vitamin E (dl-α-tocopheryl acetate)",
        "Vitamin C: ~100,000 MT/yr (world's largest single Vitamin C production line)\n"
        "Biotin: ~50 MT/yr\n"
        "Calcium pantothenate: ~5,000–8,000 MT/yr"
    ),

    # ── Xinfa Pharmaceutical 7042 ─────────────────────────────────────────────
    7042: (
        "D-Calcium pantothenate (Vitamin B5) — global top 1–2 capacity\n"
        "Folic acid (Vitamin B9)\n"
        "Vitamin A (retinyl acetate)\n"
        "Vitamin D3 (cholecalciferol)\n"
        "Vitamin B1 (thiamine HCl)\n"
        "Vitamin B6 (pyridoxine HCl)",
        "D-Calcium pantothenate: ~20,000–30,000 MT/yr (global #1–2)\n"
        "Folic acid: ~3,000–5,000 MT/yr\n"
        "Vitamin A: ~3,000–5,000 MT/yr"
    ),

    # ── Kemin 7043–7046 ───────────────────────────────────────────────────────
    7043: (
        "FloraGLO® lutein (marigold extraction, world's largest lutein brand)\n"
        "OROGLO® zeaxanthin (marigold)\n"
        "KEM GLO™ mixed carotenoids (poultry pigmentation)\n"
        "Antioxidants for food and feed (ENDOX®, SHIELD®)\n"
        "Rosemary extracts",
        "FloraGLO® lutein: ~500–1,500 MT/yr (est.)\n"
        "Antioxidants: thousands of MT/yr combined"
    ),
    7044: (
        "FORTIUM™ R rosemary extract (natural antioxidant for food, feed, cosmetics)\n"
        "Natural tocopherol (Vitamin E) extracts\n"
        "Carotenoid products for European market",
        "FORTIUM™ R: thousands of MT/yr (1,000+ acres proprietary rosemary)"
    ),
    7045: (
        "Specialty food and feed ingredients for APAC markets\n"
        "Nutraceutical ingredients\n"
        "Antioxidants and preservation solutions",
        "Thousands of MT/yr specialty ingredients (APAC regional hub)"
    ),
    7046: (
        "Fermentation-derived enzymes for animal nutrition\n"
        "Food processing enzymes",
        "Several thousand MT/yr enzymes (acquired from CJ Bio/CJ Youtell Sept 2025)"
    ),

    # ── Corbion 7047–7051 ─────────────────────────────────────────────────────
    7047: (
        "L-Lactic acid (food, pharmaceutical and industrial grade)\n"
        "Sodium lactate and potassium lactate (Purasal®)\n"
        "Calcium lactate\n"
        "Lactic acid esters (LACTEM, DATEM, sodium stearoyl lactylate)\n"
        "Biobased food preservative blends (Verdad®)",
        "Lactic acid: ~50,000–80,000 MT/yr (Gorinchem; Corbion global ~200,000 MT/yr total)"
    ),
    7048: (
        "L-Lactic acid (food and bioplastic grade)\n"
        "Lactate salts and esters for European food industry",
        "Lactic acid: ~30,000–50,000 MT/yr"
    ),
    7049: (
        "L-Lactic acid from sugarcane (food and industrial grade)",
        "Lactic acid: ~20,000–40,000 MT/yr (sugarcane feedstock)"
    ),
    7050: (
        "L-Lactic acid (food and bioplastic grade, for NatureWorks PLA feedstock)\n"
        "Lactate salts",
        "Lactic acid: ~40,000–60,000 MT/yr (post-2022 40% expansion)"
    ),
    7051: (
        "L-Lactic acid (lowest-carbon, feedstock for TotalEnergies Corbion PLA plant)\n"
        "Circular fermentation process using sugarcane or starch",
        "Lactic acid: ~80,000–100,000 MT/yr (new plant, started end 2024)"
    ),

    # ── Jungbunzlauer 7052–7055 ───────────────────────────────────────────────
    7052: (
        "Citric acid (anhydrous and monohydrate, food/beverage/industrial grade)\n"
        "Sodium citrate (trisodium citrate)\n"
        "Calcium citrate\n"
        "Potassium citrate",
        "Citric acid: ~200,000–250,000 MT/yr (world's largest single citric acid plant)"
    ),
    7053: (
        "Pharmaceutical-grade citric acid (PhEur, USP, FDA-inspected)\n"
        "Pharmaceutical sodium citrate",
        "Pharma citric acid: ~5,000–10,000 MT/yr (sole pharma-grade site in network)"
    ),
    7054: (
        "ERYLITE® erythritol (by Monilliella pollinis fermentation, non-GMO)\n"
        "Gluconic acid and sodium gluconate\n"
        "Lactic acid",
        "Erythritol: ~20,000–30,000 MT/yr\n"
        "Gluconate: ~30,000–50,000 MT/yr\n"
        "Lactic acid: ~10,000–20,000 MT/yr"
    ),
    7055: (
        "Citric acid (food/beverage grade, North American market)\n"
        "Sodium citrate",
        "Citric acid: ~100,000–150,000 MT/yr"
    ),

    # ── TotalEnergies Corbion 7056 ────────────────────────────────────────────
    7056: (
        "LUMINY® PLA (polylactic acid) biopolymer — fiber, film, rigid packaging, foam grades\n"
        "Lactide (PLA precursor intermediate)",
        "LUMINY® PLA: ~75,000 MT/yr (running above nameplate in 2025)\n"
        "Lactide: ~100,000 MT/yr"
    ),

    # ── Novamont 7057–7060 ────────────────────────────────────────────────────
    7057: (
        "Mater-Bi® starch-biopolymer (compostable bags, cutlery, packaging)\n"
        "Origo-Bi biopolyesters (PBAT-equivalent, compostable film)\n"
        "Matrol-Bi biolubricants",
        "Mater-Bi®: ~120,000 MT/yr\n"
        "Origo-Bi: ~60,000 MT/yr"
    ),
    7058: (
        "Next-generation bioplastics R&D and pilot production",
        "Pilot scale — R&D and process development"
    ),
    7059: (
        "Matrilox® azelaic acid (C9 diacid, from Brassica carinata oil)\n"
        "Sebacic acid (C10 diacid)\n"
        "Biolubricant base ingredients",
        "Azelaic acid: ~10,000–20,000 MT/yr\n"
        "Biolubricant ingredients: thousands of MT/yr"
    ),
    7060: (
        "Bio-based 1,4-butanediol (bio-BDO, Genomatica fermentation technology)\n"
        "Feedstock for PBAT, PBS bioplastics and spandex fibres",
        "Bio-BDO: ~30,000 MT/yr (world's first commercial bio-BDO plant)"
    ),

    # ── Braskem 7061 ──────────────────────────────────────────────────────────
    7061: (
        "I'm Green™ bio-based HDPE (high-density polyethylene, from sugarcane bioethanol)\n"
        "I'm Green™ bio-based LLDPE (linear low-density polyethylene)\n"
        "Bio-ethylene (intermediate)",
        "Bio-PE: ~275,000 MT/yr (HDPE + LLDPE, after $87M expansion 2023)"
    ),

    # ── Danimer/Teknor Apex 7062 ──────────────────────────────────────────────
    7062: (
        "Nodax™ PHA (polyhydroxyalkanoate, bacterial fermentation)\n"
        "Biodegradable and compostable biopolymer for packaging, coatings, fibers",
        "Nodax™ PHA: ~65 million lb/yr (~29,500 MT/yr)"
    ),

    # ── Amyris 7063 ───────────────────────────────────────────────────────────
    7063: (
        "Neossance® hemisqualane / squalane (cosmetic and pharma grade)\n"
        "Beta-farnesene (biobased chemical feedstock)\n"
        "Purecane™ Reb M sweetener (steviol glycoside, no-sugar)\n"
        "Biossance® squalane (DTC personal care)",
        "Squalane: ~2,000–5,000 MT/yr\n"
        "Reb M: ~500–1,000 MT/yr (est.)\n"
        "3 × 200 m³ + 2 × 80 m³ fermenters"
    ),

    # ── POET 7064–7068 ────────────────────────────────────────────────────────
    7064: (
        "Corn bioethanol (E10, E15, E85 grade)\n"
        "DDGS (distillers dried grains with solubles)\n"
        "Distillers corn oil (DCO)\n"
        "CO₂ (food/beverage grade, from fermentation)",
        "Bioethanol: 98M → 193M gal/yr (expansion completing Q4 2027)"
    ),
    7065: (
        "Corn bioethanol\nDDGS\nDistillers corn oil",
        "Bioethanol: ~60–100M gal/yr"
    ),
    7066: (
        "Corn bioethanol\nDDGS\nDistillers corn oil",
        "Bioethanol: ~60–100M gal/yr"
    ),
    7067: (
        "Corn bioethanol\nDDGS\nDistillers corn oil",
        "Bioethanol: ~60–100M gal/yr"
    ),
    7068: (
        "Corn bioethanol\nDDGS\nDistillers corn oil",
        "Bioethanol: ~60–100M gal/yr"
    ),

    # ── Green Plains 7069–7073 ────────────────────────────────────────────────
    7069: (
        "Corn bioethanol\nDDGS\nDistillers corn oil\nCO₂ captured (CCS, geological storage)",
        "Bioethanol: ~121M gal/yr"
    ),
    7070: (
        "Corn bioethanol\nDDGS\nDistillers corn oil\nCO₂ captured (CCS)",
        "Bioethanol: ~116M gal/yr"
    ),
    7071: (
        "Corn bioethanol\nDDGS\nCO₂ captured (CCS)",
        "Bioethanol: ~60–90M gal/yr"
    ),
    7072: (
        "Corn bioethanol\nDDGS",
        "Bioethanol: ~60M gal/yr"
    ),
    7073: (
        "Corn bioethanol\nDDGS",
        "Bioethanol: ~60M gal/yr"
    ),

    # ── Raízen 7074–7078 ──────────────────────────────────────────────────────
    7074: (
        "2G cellulosic ethanol (from sugarcane bagasse and straw)\n"
        "1G conventional sugarcane ethanol\n"
        "Sugarcane bioelectricity (bagasse co-generation)",
        "2G ethanol: ~82M liters/yr (world's first industrial 2G cellulosic ethanol plant)"
    ),
    7075: (
        "2G cellulosic ethanol (from sugarcane bagasse)\n"
        "1G sugarcane ethanol",
        "2G ethanol: ~82M liters/yr"
    ),
    7076: (
        "2G cellulosic ethanol (from sugarcane bagasse)\n"
        "1G sugarcane ethanol",
        "2G ethanol: ~82M liters/yr"
    ),
    7077: (
        "2G cellulosic ethanol (from sugarcane bagasse)\n"
        "1G sugarcane ethanol",
        "2G ethanol: ~40–82M liters/yr (est.)"
    ),
    7078: (
        "2G cellulosic ethanol (from sugarcane bagasse)\n"
        "1G sugarcane ethanol",
        "2G ethanol: ~40–82M liters/yr (est.)\n"
        "Raízen total E2G target: 440M liters/yr by 2025/26"
    ),

    # ── Verbio 7079–7083 ──────────────────────────────────────────────────────
    7079: (
        "Grain bioethanol (wheat/rye-based)\n"
        "Biomethane (biogas from distillation stillage, upgraded to grid quality)\n"
        "DDGS feed co-product",
        "Bioethanol: ~80–100M liters/yr\n"
        "Biomethane: ~50–80 million m³/yr"
    ),
    7080: (
        "Grain bioethanol\n"
        "Biomethane (from distillation stillage)\n"
        "DDGS",
        "Bioethanol: ~80–100M liters/yr\n"
        "Biomethane: ~50–80 million m³/yr"
    ),
    7081: (
        "Biomethane (from agricultural straw, anaerobic fermentation)\n"
        "No ethanol — straw-only feedstock",
        "Biomethane: ~30–50 million m³/yr (world's first stand-alone straw-to-biomethane plant)"
    ),
    7082: (
        "Corn bioethanol\n"
        "Biomethane (from corn stover, Phase II — first in North America)\n"
        "DDGS",
        "Bioethanol: ~85M gal/yr (est.)\n"
        "Biomethane: Phase II operational from ~2025"
    ),
    7083: (
        "Bioethanol (corn-based)\n"
        "Biomethane (from 2026)\n"
        "DDGS",
        "Bioethanol: ~250,000 MT/yr (~66M gal/yr est.)\n"
        "Biomethane: ~850,000 MWh/yr (from 2026)"
    ),

    # ── Quorn 7084–7086 ───────────────────────────────────────────────────────
    7084: (
        "Quorn mycoprotein (Fusarium venenatum, continuous submerged fermentation)\n"
        "Heat-treated mycoprotein ingredient (40% protein, 25% dietary fibre DWB)",
        "Mycoprotein: ~50,000–80,000 MT/yr (wet weight; world's largest mycoprotein plant)"
    ),
    7085: (
        "Quorn food products (formed mycoprotein pieces, mince, fillets)\n"
        "Consumer food production from mycoprotein ingredient",
        "Quorn food products: ~50,000+ MT/yr finished products"
    ),
    7086: (
        "Quorn food products (consumer ready meals, formed pieces)\n"
        "Mycoprotein food product manufacturing",
        "Quorn food products: tens of thousands MT/yr"
    ),

    # ── Perfect Day 7087 ──────────────────────────────────────────────────────
    7087: (
        "ProFerm™ beta-lactoglobulin (animal-free precision fermentation whey protein)\n"
        "Whey protein ingredient for food and beverage applications",
        "ProFerm™: ~2,500 MT/yr (initial capacity; first deliveries Q4 2026)"
    ),

    # ── Solar Foods 7088–7089 ─────────────────────────────────────────────────
    7088: (
        "Solein® single-cell protein (autotrophic gas fermentation: CO₂ + H₂ → biomass)\n"
        "65% protein, contains all essential amino acids, complete amino acid profile",
        "Solein®: ~160 MT/yr (scaling to ~230 MT/yr in 2026)"
    ),
    7089: (
        "Solein® single-cell protein (Factory 02 — 40× scale-up of Factory 01)",
        "Target: ~9,000 MT/yr Solein® (under development; FID 2026)"
    ),

    # ── Calysseo 7090 ─────────────────────────────────────────────────────────
    7090: (
        "FeedKind® single-cell protein (methanotrophic gas fermentation: CH₄ → SCP)\n"
        "SCP ingredient to replace fishmeal in aquaculture, poultry and swine feed",
        "FeedKind® SCP: ~20,000 MT/yr (world's largest gas fermenters: 2 × 10,000-tonne units)"
    ),
}


def add_or_update_columns(ws, new_cols: list[str]) -> dict[str, int]:
    """Add new columns if missing, return col-name → 1-based index mapping."""
    header = [cell.value for cell in ws[1]]
    col_idx = {v: i + 1 for i, v in enumerate(header) if v}
    for col_name in new_cols:
        if col_name not in col_idx:
            next_col = ws.max_column + 1
            ws.cell(row=1, column=next_col, value=col_name)
            col_idx[col_name] = next_col
    return col_idx


if __name__ == "__main__":
    path = DATA_DIR / "Global_biomanufacturing_database.xlsx"
    wb = openpyxl.load_workbook(path)
    ws = wb["All Facilities"]

    col_idx = add_or_update_columns(ws, ["Main products", "Annual capacity (est.)"])
    prod_col = col_idx["Main products"]
    cap_col  = col_idx["Annual capacity (est.)"]

    id_col = col_idx.get("ID", 1)
    updated = 0
    for row_num, row in enumerate(ws.iter_rows(min_row=2), start=2):
        fac_id = row[id_col - 1].value
        if fac_id is None:
            continue
        try:
            fac_id = int(fac_id)
        except (ValueError, TypeError):
            continue
        if fac_id in DATA:
            products, capacity = DATA[fac_id]
            ws.cell(row=row_num, column=prod_col, value=products)
            ws.cell(row=row_num, column=cap_col, value=capacity)
            updated += 1

    wb.save(path)
    print(f"Updated {updated} facilities with product + capacity data")
    print(f"Columns: 'Main products' → col {prod_col}, "
          f"'Annual capacity (est.)' → col {cap_col}")
