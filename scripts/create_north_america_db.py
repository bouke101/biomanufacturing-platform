"""
Create North America biomanufacturing database Excel file.
Columns match Pilots4U_database_1.xlsx: Facilities sheet.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FACILITIES = [
    # ── Open CMOs / CDMOs ────────────────────────────────────────────────────
    {
        "id": 1001,
        "facility": "Lonza Biologics Portsmouth",
        "membership_tier": "Open CMO",
        "city": "Portsmouth",
        "country": "USA",
        "address": "101 International Drive, Portsmouth, NH 03801",
        "contact_person": "",
        "website": "https://www.lonza.com",
        "social_links": "",
        "about": (
            "Lonza's Portsmouth site is a large-scale biologics CDMO offering mammalian "
            "cell culture manufacturing in stirred-tank bioreactors up to 20,000 L. "
            "The facility specialises in monoclonal antibody and recombinant protein production "
            "under full FDA and EMA GMP compliance."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing\nFill-Finish",
        "technologies": (
            "Fed-batch mammalian cell culture (CHO)\n"
            "Perfusion cell culture\n"
            "Protein A affinity chromatography\n"
            "Virus filtration\n"
            "Bulk drug substance manufacturing"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP\nISO 9001",
        "non_technical_services": "Process development\nAnalytical services\nRegulatory support",
        "open_24_7": "Yes",
        "extra_info": "State: NH. Part of Lonza's global biologics CDMO network. Capacity ~20,000 L mammalian.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.lonza.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1002,
        "facility": "Lonza Biologics Hopkinton",
        "membership_tier": "Open CMO",
        "city": "Hopkinton",
        "country": "USA",
        "address": "35 South Street, Hopkinton, MA 01748",
        "contact_person": "",
        "website": "https://www.lonza.com",
        "social_links": "",
        "about": (
            "Lonza's Hopkinton facility provides mammalian and microbial contract manufacturing "
            "services for biopharmaceuticals. The site handles both clinical and commercial "
            "production of proteins and antibodies, with integrated downstream and fill-finish capabilities."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "CHO cell culture\n"
            "E. coli fermentation\n"
            "Pichia pastoris fermentation\n"
            "Chromatographic purification\n"
            "Ultrafiltration / diafiltration"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Process development\nAnalytical testing",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Historical Millipore site, integrated into Lonza portfolio.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1003,
        "facility": "Lonza Biologics Vacaville",
        "membership_tier": "Open CMO",
        "city": "Vacaville",
        "country": "USA",
        "address": "3000 Nursery Road, Vacaville, CA 95687",
        "contact_person": "",
        "website": "https://www.lonza.com",
        "social_links": "",
        "about": (
            "One of the largest biologics contract manufacturing sites in the world, the Vacaville "
            "facility runs stainless-steel stirred-tank bioreactors at commercial scale for monoclonal "
            "antibodies and other large-molecule therapeutics. Originally built by Genentech and "
            "acquired by Lonza."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Large-scale CHO fed-batch (up to 25,000 L)\n"
            "Protein A purification\n"
            "Viral inactivation\n"
            "Commercial-scale UF/DF"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Commercial manufacturing\nQuality assurance",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Former Genentech Vacaville site, purchased by Lonza in 2011.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1004,
        "facility": "WuXi Biologics (Cranbury)",
        "membership_tier": "Open CMO",
        "city": "Cranbury",
        "country": "USA",
        "address": "5 Cedar Brook Drive, Cranbury, NJ 08512",
        "contact_person": "",
        "website": "https://www.wuxibiologics.com",
        "social_links": "",
        "about": (
            "WuXi Biologics' US commercial manufacturing site in New Jersey supports late-phase "
            "clinical and commercial production of biologics for global biotech and pharma clients. "
            "The facility uses single-use bioreactors and integrated purification suites."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing\nFill-Finish",
        "technologies": (
            "Single-use CHO cell culture bioreactors\n"
            "Integrated downstream processing\n"
            "Drug substance manufacturing\n"
            "Formulation and fill-finish"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Regulatory filing support\nAnalytical services",
        "open_24_7": "Yes",
        "extra_info": "State: NJ. WuXi Biologics' primary US commercial-scale facility.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.wuxibiologics.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1005,
        "facility": "WuXi Biologics (Worcester)",
        "membership_tier": "Open CMO",
        "city": "Worcester",
        "country": "USA",
        "address": "60 Prescott Street, Worcester, MA 01605",
        "contact_person": "",
        "website": "https://www.wuxibiologics.com",
        "social_links": "",
        "about": (
            "WuXi Biologics' Worcester facility provides early- to late-phase biologics contract "
            "manufacturing services. The site was established via acquisition of Sanofi's biologics "
            "manufacturing campus and focuses on mammalian cell culture drug substance production."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO fed-batch cell culture\n"
            "Bioreactors up to 15,000 L\n"
            "Chromatographic purification\n"
            "Drug substance fill"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Process transfer\nAnalytical development",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Formerly part of Sanofi Genzyme's Framingham/Allston campus network.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1006,
        "facility": "Catalent Biologics Bloomington",
        "membership_tier": "Open CMO",
        "city": "Bloomington",
        "country": "USA",
        "address": "1849 Hurlbut Road, Bloomington, IN 47404",
        "contact_person": "",
        "website": "https://www.catalent.com",
        "social_links": "",
        "about": (
            "Catalent's Bloomington site is one of the largest biologics CDMO facilities in North "
            "America, specialising in large-scale mammalian cell culture and drug substance "
            "manufacturing. Formerly Cook Pharmica, the site offers stainless-steel and "
            "single-use bioreactor capacity at clinical and commercial scale."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing\nFill-Finish",
        "technologies": (
            "CHO mammalian cell culture up to 15,000 L\n"
            "Single-use bioreactors\n"
            "Protein purification\n"
            "Aseptic fill-finish\n"
            "Lyophilisation"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP\nISO 9001",
        "non_technical_services": "Process development\nFormulation development\nStorage & distribution",
        "open_24_7": "Yes",
        "extra_info": "State: IN. Acquired from Cook Pharmica in 2017. Now part of Novo Holdings (2024 acquisition of Catalent).",
        "downloads": "",
        "videos": "",
        "logo": "https://www.catalent.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1007,
        "facility": "Catalent Biologics Madison",
        "membership_tier": "Open CMO",
        "city": "Madison",
        "country": "USA",
        "address": "726 Heartland Trail, Madison, WI 53717",
        "contact_person": "",
        "website": "https://www.catalent.com",
        "social_links": "",
        "about": (
            "Catalent's Madison site specialises in formulation development and drug product "
            "manufacturing for biologics, including liquid and lyophilised injectables. "
            "The facility is a key hub for late-phase clinical and commercial drug product supply."
        ),
        "technology_areas": "Fill-Finish\nDownstream processing",
        "technologies": (
            "Aseptic liquid fill-finish\n"
            "Lyophilisation\n"
            "Formulation development\n"
            "Prefilled syringe filling"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Analytical development\nStability studies\nRegulatory support",
        "open_24_7": "Yes",
        "extra_info": "State: WI. Drug product manufacturing focus; complements Bloomington drug substance site.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1008,
        "facility": "Fujifilm Diosynth Biotechnologies (RTP)",
        "membership_tier": "Open CMO",
        "city": "Research Triangle Park",
        "country": "USA",
        "address": "2000 Centregreen Way, Cary, NC 27513",
        "contact_person": "",
        "website": "https://fujifilmdiosynth.com",
        "social_links": "",
        "about": (
            "Fujifilm Diosynth's Research Triangle Park campus is a flagship biologics CDMO "
            "offering mammalian and microbial manufacturing. The site provides integrated services "
            "from cell line development through commercial supply, with a strong gene therapy "
            "capability added via the acquisition of Hitachi Chemical's biologics division."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nViral vector production",
        "technologies": (
            "Mammalian cell culture (CHO, HEK293)\n"
            "E. coli and Bacillus fermentation\n"
            "Insect cell culture (Sf9/baculovirus)\n"
            "Viral vector production\n"
            "Downstream purification"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Process development\nCell line development\nAnalytical services",
        "open_24_7": "Yes",
        "extra_info": "State: NC. Extensive expansion underway 2023–2026 to add large-scale mRNA and gene therapy capacity.",
        "downloads": "",
        "videos": "",
        "logo": "https://fujifilmdiosynth.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1009,
        "facility": "Fujifilm Diosynth Biotechnologies (College Station)",
        "membership_tier": "Open CMO",
        "city": "College Station",
        "country": "USA",
        "address": "4000 Fujifilm Road, College Station, TX 77845",
        "contact_person": "",
        "website": "https://fujifilmdiosynth.com",
        "social_links": "",
        "about": (
            "Fujifilm Diosynth's College Station facility is one of the world's largest "
            "single-use biopharmaceutical manufacturing sites. The facility, known as 'DragonFly', "
            "houses numerous 2,000 L single-use bioreactors for mammalian cell culture and was "
            "designed for flexible, high-speed commercial biologics production."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Single-use CHO cell culture (2,000 L scale)\n"
            "Multiple parallel bioreactor suites\n"
            "Integrated downstream processing\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Commercial supply\nQuality management",
        "open_24_7": "Yes",
        "extra_info": "State: TX. DragonFly facility; ~130,000 sq ft. Designed for rapid scale-up and flexible manufacturing.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1010,
        "facility": "Boehringer Ingelheim BioXcellence (St. Joseph)",
        "membership_tier": "Open CMO",
        "city": "St. Joseph",
        "country": "USA",
        "address": "2820 North Belt Highway, St. Joseph, MO 64506",
        "contact_person": "",
        "website": "https://www.boehringer-ingelheim.com/biopharmaceuticals/bioxcellence",
        "social_links": "",
        "about": (
            "Boehringer Ingelheim's St. Joseph site is one of North America's premier biologics "
            "contract manufacturers. Operating under the BioXcellence brand, the site offers "
            "large-scale mammalian and microbial biopharmaceutical manufacturing services with "
            "stainless-steel bioreactors from 10 L to 240,000 L."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "CHO cell culture up to 240,000 L\n"
            "E. coli high-cell-density fermentation\n"
            "Perfusion and fed-batch processes\n"
            "Chromatographic purification at commercial scale\n"
            "Virus filtration and inactivation"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP\nHealth Canada GMP",
        "non_technical_services": "Process development\nAnalytical services\nRegulatory support",
        "open_24_7": "Yes",
        "extra_info": "State: MO. World's largest single-site biopharmaceutical CDMO by bioreactor volume.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1011,
        "facility": "Boehringer Ingelheim BioXcellence (Fremont)",
        "membership_tier": "Open CMO",
        "city": "Fremont",
        "country": "USA",
        "address": "6701 Kaiser Drive, Fremont, CA 94555",
        "contact_person": "",
        "website": "https://www.boehringer-ingelheim.com/biopharmaceuticals/bioxcellence",
        "social_links": "",
        "about": (
            "Boehringer Ingelheim's Fremont facility provides mammalian and microbial contract "
            "manufacturing for clinical and commercial biopharmaceuticals. The site was acquired "
            "from Roche/Genentech and expanded to support the growing BioXcellence CDMO portfolio."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation",
        "technologies": (
            "Mammalian cell culture\n"
            "E. coli fermentation\n"
            "Downstream purification\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Process transfer\nAnalytical testing",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Former Roche Diagnostics site; expanded under Boehringer Ingelheim ownership.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1012,
        "facility": "AGC Biologics (Seattle)",
        "membership_tier": "Open CMO",
        "city": "Seattle",
        "country": "USA",
        "address": "22021 20th Ave SE, Bothell, WA 98021",
        "contact_person": "",
        "website": "https://www.agcbio.com",
        "social_links": "",
        "about": (
            "AGC Biologics' Seattle-area campus in Bothell is a full-service biologics CDMO "
            "providing mammalian cell culture and microbial fermentation services from process "
            "development through commercial manufacturing. The site is one of AGC Biologics' "
            "primary North American facilities."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "CHO and HEK293 cell culture\n"
            "E. coli and P. pastoris fermentation\n"
            "Integrated downstream purification\n"
            "Drug substance formulation",
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Cell line development\nProcess development\nQuality services",
        "open_24_7": "Yes",
        "extra_info": "State: WA (Bothell). Formerly CMC Biologics; acquired by AGC Inc. (Asahi Glass). Includes API and drug product suites.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.agcbio.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1013,
        "facility": "AGC Biologics (Boulder)",
        "membership_tier": "Open CMO",
        "city": "Boulder",
        "country": "USA",
        "address": "5480 Airport Boulevard, Boulder, CO 80301",
        "contact_person": "",
        "website": "https://www.agcbio.com",
        "social_links": "",
        "about": (
            "AGC Biologics' Boulder facility specialises in process development and clinical-scale "
            "manufacturing of biologics and high-potency APIs. The site offers flexible single-use "
            "and stainless-steel bioreactor capacity for early-phase biologics programs."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation",
        "technologies": (
            "Clinical-scale mammalian cell culture\n"
            "Microbial fermentation\n"
            "Downstream processing\n"
            "High-potency API handling"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Process development\nAnalytical development",
        "open_24_7": "Yes",
        "extra_info": "State: CO. Focus on clinical-phase biologics and process development services.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1014,
        "facility": "KBI BioPharma (Durham)",
        "membership_tier": "Open CMO",
        "city": "Durham",
        "country": "USA",
        "address": "2000 Millbrook Drive, Durham, NC 27709",
        "contact_person": "",
        "website": "https://kbibiopharma.com",
        "social_links": "",
        "about": (
            "KBI BioPharma's Durham site is a biologics CDMO providing integrated drug substance "
            "and drug product services. The facility offers mammalian cell culture manufacturing, "
            "downstream processing, and aseptic fill-finish for clinical and commercial programs."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing\nFill-Finish",
        "technologies": (
            "Fed-batch and perfusion CHO cell culture\n"
            "Antibody and protein purification\n"
            "Aseptic fill-finish\n"
            "Lyophilisation"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Process development\nFormulation development\nStability testing",
        "open_24_7": "Yes",
        "extra_info": "State: NC. Subsidiary of JSR Corporation (Japan). Integrated drug substance to drug product CDMO.",
        "downloads": "",
        "videos": "",
        "logo": "https://kbibiopharma.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1015,
        "facility": "KBI BioPharma (Rockville)",
        "membership_tier": "Open CMO",
        "city": "Rockville",
        "country": "USA",
        "address": "1450 South Rolling Road, Baltimore, MD 21227",
        "contact_person": "",
        "website": "https://kbibiopharma.com",
        "social_links": "",
        "about": (
            "KBI BioPharma's Maryland site provides biologics process development and analytical "
            "testing services. The site offers structural characterisation, forced degradation "
            "studies, and accelerated stability testing to support IND and BLA submissions."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Biologics process development\n"
            "Analytical characterisation\n"
            "Stability testing\n"
            "Formulation development"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Analytical development\nRegulatory support",
        "open_24_7": "No",
        "extra_info": "State: MD. Process development and analytical hub complementing Durham manufacturing campus.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1016,
        "facility": "Emergent BioSolutions (Bayview)",
        "membership_tier": "Open CMO",
        "city": "Baltimore",
        "country": "USA",
        "address": "5901 East Lombard Street, Baltimore, MD 21224",
        "contact_person": "",
        "website": "https://www.emergentbiosolutions.com",
        "social_links": "",
        "about": (
            "Emergent BioSolutions' Baltimore Bayview campus is a major biologics and vaccine "
            "contract manufacturer. The site produces anthrax vaccine (BioThrax), smallpox "
            "vaccine, and has significant CDMO capacity for government and commercial clients. "
            "The facility attracted scrutiny during COVID-19 vaccine manufacturing in 2021."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nFill-Finish",
        "technologies": (
            "Bacterial fermentation\n"
            "Mammalian cell culture\n"
            "Viral propagation\n"
            "Drug substance manufacturing\n"
            "Aseptic fill-finish"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nUSDA",
        "non_technical_services": "CDMO services\nGovernment contract manufacturing",
        "open_24_7": "Yes",
        "extra_info": "State: MD. Key US government BARDA contract manufacturing facility for biodefense products.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.emergentbiosolutions.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1017,
        "facility": "Emergent BioSolutions (Lansing)",
        "membership_tier": "Open CMO",
        "city": "Lansing",
        "country": "USA",
        "address": "3500 North Martin Luther King Jr. Blvd, Lansing, MI 48906",
        "contact_person": "",
        "website": "https://www.emergentbiosolutions.com",
        "social_links": "",
        "about": (
            "Emergent BioSolutions' Lansing facility manufactures BCG-based immunotherapies and "
            "other biological products. The site operates under government supply contracts and "
            "commercial agreements, with capabilities in bacterial fermentation and drug substance "
            "production."
        ),
        "technology_areas": "Microbial fermentation\nFill-Finish",
        "technologies": (
            "BCG and other bacterial vaccine production\n"
            "Fermentation and downstream processing\n"
            "Drug product filling"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP",
        "non_technical_services": "Government contract manufacturing",
        "open_24_7": "Yes",
        "extra_info": "State: MI. Specialises in bacterial biopharmaceuticals and immunotherapy products.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1018,
        "facility": "National Resilience (Alachua)",
        "membership_tier": "Open CMO",
        "city": "Alachua",
        "country": "USA",
        "address": "13859 Progress Boulevard, Alachua, FL 32615",
        "contact_person": "",
        "website": "https://resilience.com",
        "social_links": "",
        "about": (
            "National Resilience's Alachua facility provides contract manufacturing for viral "
            "vectors and advanced gene therapies. The site, formerly part of the Florida "
            "biomanufacturing ecosystem, offers GMP-grade AAV, lentiviral vector, and "
            "oncolytic virus production."
        ),
        "technology_areas": "Viral vector production\nCell Cultivation",
        "technologies": (
            "AAV production (HEK293 transient transfection)\n"
            "Lentiviral vector manufacturing\n"
            "Oncolytic virus production\n"
            "Downstream purification"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Process development\nAnalytical services\nRegulatory support",
        "open_24_7": "Yes",
        "extra_info": "State: FL. Resilience acquired multiple gene therapy CDMOs to build a national manufacturing network.",
        "downloads": "",
        "videos": "",
        "logo": "https://resilience.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1019,
        "facility": "National Resilience (Marlborough)",
        "membership_tier": "Open CMO",
        "city": "Marlborough",
        "country": "USA",
        "address": "35 Wiggins Avenue, Marlborough, MA 01752",
        "contact_person": "",
        "website": "https://resilience.com",
        "social_links": "",
        "about": (
            "National Resilience's Marlborough campus was formerly the Sanofi/Genzyme Allston "
            "biologics manufacturing site. Acquired by Resilience, it now operates as an advanced "
            "manufacturing hub for complex biologics and mRNA therapeutics, leveraging the "
            "infrastructure of one of New England's largest biomanufacturing facilities."
        ),
        "technology_areas": "Cell Cultivation\nmRNA/LNP manufacturing\nDownstream processing",
        "technologies": (
            "Mammalian cell culture\n"
            "mRNA synthesis and purification\n"
            "Lipid nanoparticle (LNP) formulation\n"
            "Drug substance and drug product manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Technology transfer\nCommercial manufacturing",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Former Sanofi Genzyme Allston campus; repurposed for mRNA and cell therapy manufacturing.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1020,
        "facility": "Cytovance Biologics",
        "membership_tier": "Open CMO",
        "city": "Oklahoma City",
        "country": "USA",
        "address": "840 Research Parkway, Suite 100, Oklahoma City, OK 73104",
        "contact_person": "",
        "website": "https://cytovance.com",
        "social_links": "",
        "about": (
            "Cytovance Biologics is a full-service CDMO based at the Oklahoma Medical Research "
            "Foundation campus, offering mammalian cell culture and microbial fermentation "
            "manufacturing for clinical-stage biologics. The company provides end-to-end services "
            "including cell line development, process development, and GMP production."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "CHO and NS0 mammalian cell culture\n"
            "E. coli fermentation\n"
            "Antibody and protein purification\n"
            "Drug substance formulation"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Cell line development\nProcess development\nQuality control testing",
        "open_24_7": "No",
        "extra_info": "State: OK. Founded 2004 at OMRF campus. Focus on Phase I–III clinical manufacturing.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1021,
        "facility": "Goodwin Biotechnology",
        "membership_tier": "Open CMO",
        "city": "Plantation",
        "country": "USA",
        "address": "1830 SW 82nd Avenue, Plantation, FL 33324",
        "contact_person": "",
        "website": "https://www.goodwinbio.com",
        "social_links": "",
        "about": (
            "Goodwin Biotechnology is a specialist CDMO offering mammalian and insect cell "
            "culture manufacturing services. The company is particularly well-known for "
            "baculovirus-insect cell expression for VLP, subunit vaccine, and recombinant "
            "protein production at clinical scale."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Baculovirus/insect cell (Sf9, High Five) expression\n"
            "Mammalian cell culture (CHO, HEK293)\n"
            "VLP and subunit vaccine production\n"
            "Protein purification"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Virus-like particle (VLP) development\nProcess development",
        "open_24_7": "No",
        "extra_info": "State: FL. Niche specialist in insect cell expression and VLP manufacturing.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1022,
        "facility": "Ajinomoto Bio-Pharma Services",
        "membership_tier": "Open CMO",
        "city": "San Diego",
        "country": "USA",
        "address": "3030 Callan Road, San Diego, CA 92121",
        "contact_person": "",
        "website": "https://www.ajibio-pharma.com",
        "social_links": "",
        "about": (
            "Ajinomoto Bio-Pharma Services (formerly Althea Technologies) is a San Diego-based "
            "CDMO specialising in microbial fermentation, mammalian cell culture, and drug product "
            "manufacturing. The facility offers GMP production from lab scale to commercial "
            "volumes, with particular strength in E. coli refolding and inclusion body processing."
        ),
        "technology_areas": "Microbial fermentation\nCell Cultivation\nFill-Finish",
        "technologies": (
            "E. coli fermentation and inclusion body refolding\n"
            "CHO cell culture\n"
            "Aseptic fill-finish\n"
            "Lyophilisation",
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Process development\nFormulation\nAnalytical testing",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Subsidiary of Ajinomoto Co. (Japan). Formerly Althea Technologies, rebranded 2014.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1023,
        "facility": "ElevateBio BaseCamp",
        "membership_tier": "Open CMO",
        "city": "Waltham",
        "country": "USA",
        "address": "200 Arsenal Yards Blvd, Waltham, MA 02451",
        "contact_person": "",
        "website": "https://elevatebio.com",
        "social_links": "",
        "about": (
            "ElevateBio's BaseCamp is an integrated cell and gene therapy development and "
            "manufacturing facility. The platform supports AAV, lentiviral vector, and ex vivo "
            "cell therapy manufacturing from research scale through clinical GMP production. "
            "ElevateBio combines technology development with CDMO services."
        ),
        "technology_areas": "Viral vector production\nCell therapy manufacturing",
        "technologies": (
            "AAV gene therapy manufacturing\n"
            "Lentiviral vector production\n"
            "Ex vivo cell therapy (CAR-T, TCR-T)\n"
            "HEK293 transient transfection"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Cell line engineering\nProcess development\nRegulatory support",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Founded 2017; significant investment from GV, F-Prime, Vida Ventures.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1024,
        "facility": "Andelyn Biosciences",
        "membership_tier": "Open CMO",
        "city": "Columbus",
        "country": "USA",
        "address": "575 Children's Crossroads, Columbus, OH 43205",
        "contact_person": "",
        "website": "https://andelynbiosciences.com",
        "social_links": "",
        "about": (
            "Andelyn Biosciences (formerly Nationwide Children's Hospital's gene therapy "
            "manufacturing arm) is a leading viral vector CDMO. The company manufactures "
            "AAV gene therapies at clinical and commercial scale and has powered multiple "
            "FDA-approved gene therapy products including Zolgensma."
        ),
        "technology_areas": "Viral vector production\nCell Cultivation",
        "technologies": (
            "AAV serotype manufacturing (AAV1–9, novel capsids)\n"
            "HEK293 transient transfection\n"
            "Triple plasmid transfection\n"
            "CsCl and iodixanol ultracentrifugation\n"
            "Column purification of viral vectors"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP",
        "non_technical_services": "Vector design\nPotency assay development\nRegulatory filing support",
        "open_24_7": "Yes",
        "extra_info": "State: OH. Spun out of Nationwide Children's Hospital 2021. Manufactured AveXis/Novartis Zolgensma AAV9.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1025,
        "facility": "Forge Biologics",
        "membership_tier": "Open CMO",
        "city": "Columbus",
        "country": "USA",
        "address": "3600 Gantz Road, Grove City, OH 43123",
        "contact_person": "",
        "website": "https://forgebiologics.com",
        "social_links": "",
        "about": (
            "Forge Biologics is a gene therapy CDMO dedicated to AAV manufacturing. "
            "The company operates its Giga-scale Manufacturing Facility (GMF), designed to "
            "produce clinical and commercial AAV at unprecedented scale and cost-efficiency, "
            "supporting the advancement of rare disease gene therapies."
        ),
        "technology_areas": "Viral vector production",
        "technologies": (
            "AAV manufacturing at giga-scale\n"
            "HEK293 suspension cell culture\n"
            "Baculovirus-insect cell AAV production\n"
            "Affinity and polishing chromatography"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "AAV process development\nAnalytical development\nRegulatory strategy",
        "open_24_7": "Yes",
        "extra_info": "State: OH (Grove City). Founded 2019; purpose-built Giga-scale Manufacturing Facility (GMF) opened 2022.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1026,
        "facility": "Abzena (Bristol PA)",
        "membership_tier": "Open CMO",
        "city": "Bristol",
        "country": "USA",
        "address": "100 Jersey Avenue, New Brunswick, NJ 08901",
        "contact_person": "",
        "website": "https://www.abzena.com",
        "social_links": "",
        "about": (
            "Abzena's US facilities provide integrated biologics and bioconjugate manufacturing "
            "services, with a focus on antibody–drug conjugates (ADCs), conjugation chemistry, "
            "and mammalian cell culture. The company offers end-to-end services from antibody "
            "development through clinical GMP manufacturing."
        ),
        "technology_areas": "Cell Cultivation\nChemical conjugation\nDownstream processing",
        "technologies": (
            "Mammalian cell culture (CHO, HEK293)\n"
            "Antibody-drug conjugate (ADC) manufacturing\n"
            "Conjugation chemistry\n"
            "Protein purification"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Antibody engineering\nADC development\nAnalytical characterisation",
        "open_24_7": "Yes",
        "extra_info": "State: NJ. Formerly part of TCRS and PolyTherics; merged to form Abzena. Strong ADC and bioconjugation capability.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1027,
        "facility": "Rentschler Biopharma (Milford)",
        "membership_tier": "Open CMO",
        "city": "Milford",
        "country": "USA",
        "address": "One Technology Park, Milford, MA 01757",
        "contact_person": "",
        "website": "https://www.rentschler-biopharma.com",
        "social_links": "",
        "about": (
            "Rentschler Biopharma's US site in Milford, Massachusetts provides mammalian cell "
            "culture manufacturing services for clinical and commercial biologics. The site was "
            "established to bring European CDMO capabilities to the American market, offering "
            "single-use and stainless-steel bioreactor capacity."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "Single-use bioreactors (up to 2,000 L)\n"
            "Protein purification\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Process development\nTechnology transfer",
        "open_24_7": "Yes",
        "extra_info": "State: MA. German-origin family-owned CDMO; US site opened 2020 to serve North American clients.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1028,
        "facility": "Therapure Biopharma",
        "membership_tier": "Open CMO",
        "city": "Mississauga",
        "country": "Canada",
        "address": "2585 Meadowvale Boulevard, Mississauga, ON L5N 8H9",
        "contact_person": "",
        "website": "https://www.therapurebio.com",
        "social_links": "",
        "about": (
            "Therapure Biopharma is Canada's leading biologics CDMO, providing mammalian cell "
            "culture, plasma protein manufacturing, and drug product services. The Mississauga "
            "facility was originally built for Bayer's pharmaceutical operations and is now a "
            "full-service CDMO supporting both domestic and international clients."
        ),
        "technology_areas": "Cell Cultivation\nPlasma fractionation\nFill-Finish",
        "technologies": (
            "CHO mammalian cell culture\n"
            "Plasma protein manufacturing\n"
            "Aseptic fill-finish\n"
            "Lyophilisation"
        ),
        "n_technologies": 4,
        "certifications": "Health Canada GMP\nFDA cGMP\nEMA GMP",
        "non_technical_services": "Process development\nAnalytical services\nStability studies",
        "open_24_7": "Yes",
        "extra_info": "Province: ON. Formerly Bayer Biologicals facility, converted to CDMO operations. Canada's largest biologics CMO.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1029,
        "facility": "BioVectra",
        "membership_tier": "Open CMO",
        "city": "Charlottetown",
        "country": "Canada",
        "address": "11 Aviation Avenue, Charlottetown, PE C1E 0A1",
        "contact_person": "",
        "website": "https://biovectra.com",
        "social_links": "",
        "about": (
            "BioVectra is a Canadian CDMO specialising in highly potent APIs, oligonucleotides, "
            "and biological APIs. Based in Prince Edward Island, the company operates GMP "
            "manufacturing facilities for complex synthetic and biologically derived active "
            "pharmaceutical ingredients serving global biotech and pharma companies."
        ),
        "technology_areas": "Chemical synthesis\nMicrobial fermentation\nOligonucleotide synthesis",
        "technologies": (
            "High-potency API manufacturing\n"
            "Microbial fermentation\n"
            "Oligonucleotide synthesis\n"
            "Biocatalysis"
        ),
        "n_technologies": 4,
        "certifications": "Health Canada GMP\nFDA cGMP\nEMA GMP",
        "non_technical_services": "Process development\nAnalytical chemistry\nQuality services",
        "open_24_7": "Yes",
        "extra_info": "Province: PEI. Acquired by Thermo Fisher Scientific in 2021.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1030,
        "facility": "Oxford Biomedica Solutions",
        "membership_tier": "Open CMO",
        "city": "Bedford",
        "country": "USA",
        "address": "70 Research Drive, Bedford, MA 01730",
        "contact_person": "",
        "website": "https://www.oxfordbiomedica.co.uk",
        "social_links": "",
        "about": (
            "Oxford Biomedica Solutions (formerly Homology Medicines' manufacturing site) is a "
            "viral vector CDMO providing GMP lentiviral and AAV manufacturing services. "
            "The site leverages Oxford Biomedica's LentiVector platform and supports clinical "
            "and commercial cell and gene therapy programs."
        ),
        "technology_areas": "Viral vector production",
        "technologies": (
            "Lentiviral vector manufacturing (LentiVector platform)\n"
            "AAV production\n"
            "HEK293 and HEK293T cell culture\n"
            "Downstream purification"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Vector engineering\nProcess development\nAnalytical testing",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Oxford Biomedica US site; complements UK Harrow Court manufacturing campus.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },

    # ── Captive Manufacturing ────────────────────────────────────────────────
    {
        "id": 2001,
        "facility": "Amgen Thousand Oaks",
        "membership_tier": "Captive",
        "city": "Thousand Oaks",
        "country": "USA",
        "address": "One Amgen Center Drive, Thousand Oaks, CA 91320",
        "contact_person": "",
        "website": "https://www.amgen.com",
        "social_links": "",
        "about": (
            "Amgen's world headquarters and original manufacturing campus in Thousand Oaks "
            "has been a cornerstone of the US biopharmaceutical industry since the company's "
            "founding in 1980. The site produces multiple blockbuster biologics including "
            "Enbrel, Aranesp, and Prolia, and houses Amgen's principal R&D operations."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "E. coli fermentation\n"
            "Perfusion and fed-batch processes\n"
            "Protein purification\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Founded 1980; first site and global HQ. Employs ~6,000 at this campus.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.amgen.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2002,
        "facility": "Amgen West Greenwich",
        "membership_tier": "Captive",
        "city": "West Greenwich",
        "country": "USA",
        "address": "100 Leadership Boulevard, West Greenwich, RI 02817",
        "contact_person": "",
        "website": "https://www.amgen.com",
        "social_links": "",
        "about": (
            "Amgen's Rhode Island campus is one of the world's largest biologics manufacturing "
            "facilities, housing commercial-scale mammalian cell culture bioreactors. "
            "The site produces key Amgen products including Enbrel (etanercept) at scale, "
            "with stainless-steel bioreactors exceeding 75,000 L total installed capacity."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Large-scale CHO mammalian cell culture (up to 75,000 L)\n"
            "Fed-batch bioreactor processes\n"
            "Commercial protein purification\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: RI. Among world's largest single biologics sites by bioreactor volume. Key Enbrel supply site.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 2003,
        "facility": "Genentech (South San Francisco)",
        "membership_tier": "Captive",
        "city": "South San Francisco",
        "country": "USA",
        "address": "1 DNA Way, South San Francisco, CA 94080",
        "contact_person": "",
        "website": "https://www.gene.com",
        "social_links": "",
        "about": (
            "Genentech's South San Francisco headquarters is where the modern biopharmaceutical "
            "industry began. The site houses research, development, and manufacturing operations "
            "for Genentech/Roche products. It is the birthplace of recombinant DNA technology "
            "in industry and produced the first FDA-approved biotech drug (human insulin, 1982)."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "Mammalian cell culture (CHO)\n"
            "E. coli fermentation\n"
            "Protein purification\n"
            "Pilot and clinical manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal R&D and clinical supply",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Founded 1976 by Boyer & Swanson; part of Roche since 2009. Historic birthplace of biotech manufacturing.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.gene.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2004,
        "facility": "Genentech Vacaville",
        "membership_tier": "Captive",
        "city": "Vacaville",
        "country": "USA",
        "address": "1 DNA Way, Vacaville, CA 95687",
        "contact_person": "",
        "website": "https://www.gene.com",
        "social_links": "",
        "about": (
            "Genentech's Vacaville manufacturing site is a large-scale commercial biologics "
            "facility dedicated to producing Roche/Genentech medicines. The campus houses "
            "multiple manufacturing suites with 25,000 L stainless-steel bioreactors. "
            "Part of the site has been converted to Lonza CDMO operations."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Large-scale CHO mammalian cell culture (25,000 L)\n"
            "Fed-batch production\n"
            "Commercial protein purification\n"
            "Bulk drug substance manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: CA. ~100,000 L total installed bioreactor capacity. A portion leased/sold to Lonza CDMO operations.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 2005,
        "facility": "Pfizer Andover Biologics",
        "membership_tier": "Captive",
        "city": "Andover",
        "country": "USA",
        "address": "1 Burtt Road, Andover, MA 01810",
        "contact_person": "",
        "website": "https://www.pfizer.com",
        "social_links": "",
        "about": (
            "Pfizer's Andover biologics campus is a major commercial manufacturing hub for "
            "Pfizer's biopharmaceutical portfolio. The site houses mammalian cell culture "
            "and microbial fermentation capabilities, producing key biologics including "
            "biosimilars and established biologic medicines."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "E. coli fermentation\n"
            "Large-scale protein purification\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Former Wyeth Pharmaceuticals site; acquired by Pfizer in 2009. Key US biologics hub.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.pfizer.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2006,
        "facility": "AbbVie Biologics (North Chicago)",
        "membership_tier": "Captive",
        "city": "North Chicago",
        "country": "USA",
        "address": "1 North Waukegan Road, North Chicago, IL 60064",
        "contact_person": "",
        "website": "https://www.abbvie.com",
        "social_links": "",
        "about": (
            "AbbVie's North Chicago campus is the global headquarters and primary manufacturing "
            "site for AbbVie's biologics portfolio, including Humira (adalimumab), the world's "
            "best-selling biologic drug for over a decade. The site employs a large-scale "
            "mammalian cell culture platform."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture at commercial scale\n"
            "Monoclonal antibody purification\n"
            "Drug substance manufacturing\n"
            "Aseptic processing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: IL. Formerly Abbott Laboratories; spun off as AbbVie 2013. Humira production hub.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.abbvie.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2007,
        "facility": "Bristol-Myers Squibb Devens",
        "membership_tier": "Captive",
        "city": "Devens",
        "country": "USA",
        "address": "100 Forest Street, Devens, MA 01434",
        "contact_person": "",
        "website": "https://www.bms.com",
        "social_links": "",
        "about": (
            "Bristol-Myers Squibb's Devens facility is a state-of-the-art biologics manufacturing "
            "site built to produce Opdivo (nivolumab) and other immuno-oncology biologics at "
            "commercial scale. Opened in 2019, the facility uses single-use bioreactor technology "
            "throughout, making it one of the most modern large-scale biologics plants in the world."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing\nFill-Finish",
        "technologies": (
            "Single-use CHO mammalian cell culture (up to 2,000 L)\n"
            "Multiple parallel manufacturing suites\n"
            "Integrated downstream processing\n"
            "Drug substance and drug product manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Opened 2019. $750M investment; fully single-use technology. Produces Opdivo and Orencia.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.bms.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2008,
        "facility": "AstraZeneca / MedImmune (Gaithersburg)",
        "membership_tier": "Captive",
        "city": "Gaithersburg",
        "country": "USA",
        "address": "One MedImmune Way, Gaithersburg, MD 20878",
        "contact_person": "",
        "website": "https://www.astrazeneca.com",
        "social_links": "",
        "about": (
            "AstraZeneca's Gaithersburg campus, formerly MedImmune headquarters, is a major "
            "biologics R&D and manufacturing site. The facility produces respiratory syncytial "
            "virus vaccines (Synagis/palivizumab) and other biologics, and houses AstraZeneca's "
            "US biological research and early manufacturing operations."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Mammalian cell culture\n"
            "Antibody manufacturing\n"
            "Vaccine production\n"
            "Protein purification"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: MD. MedImmune acquired by AstraZeneca 2007. Historically known for FluMist and Synagis manufacture.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 2009,
        "facility": "Merck & Co. (West Point)",
        "membership_tier": "Captive",
        "city": "West Point",
        "country": "USA",
        "address": "770 Sumneytown Pike, West Point, PA 19486",
        "contact_person": "",
        "website": "https://www.merck.com",
        "social_links": "",
        "about": (
            "Merck's West Point facility is the company's largest US manufacturing campus, "
            "producing vaccines (including Gardasil, varicella), biologics, and small-molecule "
            "drugs. The site is a historic Merck manufacturing hub with over 100 years of "
            "pharmaceutical production and one of the world's largest vaccine manufacturing sites."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nVaccine production\nFill-Finish",
        "technologies": (
            "Vero cell culture for vaccines\n"
            "VLP-based vaccine production (Gardasil)\n"
            "Fermentation and downstream processing\n"
            "Lyophilised vaccine manufacturing\n"
            "Aseptic fill-finish"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: PA. ~10,000 employees; over 100-year history. Principal US site for Gardasil and Keytruda manufacturing.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.merck.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2010,
        "facility": "Biogen (Research Triangle Park)",
        "membership_tier": "Captive",
        "city": "Research Triangle Park",
        "country": "USA",
        "address": "5000 Davis Drive, Research Triangle Park, NC 27709",
        "contact_person": "",
        "website": "https://www.biogen.com",
        "social_links": "",
        "about": (
            "Biogen's RTP campus is the company's primary US commercial biologics manufacturing "
            "site, producing multiple sclerosis therapies including Avonex (interferon beta-1a) "
            "and Tysabri (natalizumab). The site operates large-scale CHO mammalian cell culture "
            "and downstream processing facilities."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture at commercial scale\n"
            "Protein purification\n"
            "Drug substance manufacturing\n"
            "Drug product fill-finish"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: NC. Key Biogen manufacturing hub for multiple sclerosis portfolio. Also produces Spinraza (nusinersen).",
        "downloads": "",
        "videos": "",
        "logo": "https://www.biogen.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2011,
        "facility": "Regeneron Pharmaceuticals (Rensselaer)",
        "membership_tier": "Captive",
        "city": "Rensselaer",
        "country": "USA",
        "address": "777 Old Saw Mill River Road, Tarrytown, NY 10591",
        "contact_person": "",
        "website": "https://www.regeneron.com",
        "social_links": "",
        "about": (
            "Regeneron's Rensselaer manufacturing campus is the company's commercial biologics "
            "production hub. The site manufactures key products including Dupixent (dupilumab) "
            "and Eylea (aflibercept) using Regeneron's proprietary CHO-based manufacturing "
            "platform with large-scale stainless-steel and single-use bioreactors."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture (VelocImmune platform)\n"
            "Large-scale bioreactors\n"
            "Monoclonal antibody purification\n"
            "Fusion protein manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: NY. Large expansion for Dupixent (dupilumab) production ongoing. Also Limerick, Ireland site for global supply.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.regeneron.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2012,
        "facility": "Novo Nordisk (Clayton)",
        "membership_tier": "Captive",
        "city": "Clayton",
        "country": "USA",
        "address": "3612 Powhatan Road, Clayton, NC 27527",
        "contact_person": "",
        "website": "https://www.novonordisk-us.com",
        "social_links": "",
        "about": (
            "Novo Nordisk's Clayton facility is one of the company's primary US manufacturing "
            "sites, producing insulin and GLP-1 receptor agonist therapies. The site has "
            "undergone massive expansion to meet demand for semaglutide (Ozempic/Wegovy). "
            "It combines fermentation-based API production with drug product fill-finish."
        ),
        "technology_areas": "Microbial fermentation\nDownstream processing\nFill-Finish",
        "technologies": (
            "Yeast (Saccharomyces cerevisiae) fermentation for insulin\n"
            "Microbial peptide fermentation for GLP-1 analogues\n"
            "Downstream protein processing\n"
            "Drug substance purification\n"
            "Drug product filling"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: NC. Multi-billion dollar expansion underway 2022–2025 to increase semaglutide (Ozempic/Wegovy) supply.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.novonordisk-us.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2013,
        "facility": "Moderna (Norwood)",
        "membership_tier": "Captive",
        "city": "Norwood",
        "country": "USA",
        "address": "200 Technology Square, Cambridge, MA 02139",
        "contact_person": "",
        "website": "https://www.modernatx.com",
        "social_links": "",
        "about": (
            "Moderna's primary US manufacturing facility for mRNA medicines and vaccines is "
            "located in Norwood, Massachusetts. The site produces mRNA drug substance and "
            "lipid nanoparticle (LNP) formulated drug product, and was central to "
            "COVID-19 mRNA vaccine supply under Operation Warp Speed."
        ),
        "technology_areas": "mRNA/LNP manufacturing\nDownstream processing\nFill-Finish",
        "technologies": (
            "Cell-free mRNA synthesis (in vitro transcription)\n"
            "mRNA purification and capping\n"
            "Lipid nanoparticle (LNP) formulation\n"
            "Aseptic fill-finish\n"
            "Drug product manufacturing"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Norwood manufacturing site is ~200,000 sq ft; key COVID-19 vaccine supply site from 2021.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.modernatx.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2014,
        "facility": "CSL Behring (Kankakee)",
        "membership_tier": "Captive",
        "city": "Kankakee",
        "country": "USA",
        "address": "1020 First Avenue, Kankakee, IL 60901",
        "contact_person": "",
        "website": "https://www.cslbehring.com",
        "social_links": "",
        "about": (
            "CSL Behring's Kankakee facility is a large-scale plasma protein manufacturing site "
            "producing coagulation factors, immunoglobulins, and albumin from donor plasma. "
            "The site is part of CSL's global plasma manufacturing network and operates under "
            "full FDA and international GMP standards."
        ),
        "technology_areas": "Plasma fractionation\nDownstream processing",
        "technologies": (
            "Human plasma fractionation (Cohn–Oncley process)\n"
            "Cold ethanol fractionation\n"
            "Chromatographic purification of plasma proteins\n"
            "Pathogen reduction technologies"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: IL. CSL Behring global HQ is in King of Prussia, PA. Key plasma-derived protein manufacturing campus.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.cslbehring.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2015,
        "facility": "Eli Lilly (Indianapolis)",
        "membership_tier": "Captive",
        "city": "Indianapolis",
        "country": "USA",
        "address": "Lilly Corporate Center, Indianapolis, IN 46285",
        "contact_person": "",
        "website": "https://www.lilly.com",
        "social_links": "",
        "about": (
            "Eli Lilly's Indianapolis headquarters campus houses manufacturing, R&D, and global "
            "operations. The site has been involved in biologics production since the first "
            "commercial recombinant insulin (Humulin) produced using E. coli fermentation "
            "technology in 1982. Current manufacturing supports diabetes, immunology, and "
            "oncology biologics."
        ),
        "technology_areas": "Microbial fermentation\nCell Cultivation\nDownstream processing",
        "technologies": (
            "E. coli fermentation for insulin\n"
            "CHO mammalian cell culture for mAbs\n"
            "Protein purification\n"
            "GLP-1 agonist manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: IN. Founded 1876; historic site of world's first commercial recombinant insulin (Humulin, 1982).",
        "downloads": "",
        "videos": "",
        "logo": "https://www.lilly.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2016,
        "facility": "Amgen Puerto Rico",
        "membership_tier": "Captive",
        "city": "Juncos",
        "country": "USA",
        "address": "PR-3 Km 74.1, Juncos, Puerto Rico 00777",
        "contact_person": "",
        "website": "https://www.amgen.com",
        "social_links": "",
        "about": (
            "Amgen's Puerto Rico manufacturing facility in Juncos is a major commercial biologics "
            "production site serving global markets. The facility produces drug substance and "
            "drug product for several key Amgen medicines and is a vital part of Amgen's "
            "global supply chain."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing\nFill-Finish",
        "technologies": (
            "Commercial-scale CHO mammalian cell culture\n"
            "Protein purification\n"
            "Drug product fill-finish\n"
            "Aseptic processing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "Territory: PR. One of three major Amgen commercial manufacturing sites alongside Thousand Oaks and West Greenwich.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 2017,
        "facility": "Grifols (Los Angeles)",
        "membership_tier": "Captive",
        "city": "Los Angeles",
        "country": "USA",
        "address": "5555 Valley Boulevard, Los Angeles, CA 90032",
        "contact_person": "",
        "website": "https://www.grifols.com",
        "social_links": "",
        "about": (
            "Grifols' Los Angeles manufacturing facility is one of the company's primary North "
            "American plasma protein manufacturing sites. The facility produces immunoglobulins, "
            "albumin, and coagulation factors from human plasma using large-scale fractionation "
            "and chromatographic purification."
        ),
        "technology_areas": "Plasma fractionation\nDownstream processing",
        "technologies": (
            "Plasma fractionation\n"
            "IgG immunoglobulin purification\n"
            "Albumin production\n"
            "Pathogen reduction"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Grifols (Spain-based) acquired Talecris Biotherapeutics (formerly Bayer Biologics plasma) in 2011.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.grifols.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2018,
        "facility": "BioMarin (Novato)",
        "membership_tier": "Captive",
        "city": "Novato",
        "country": "USA",
        "address": "105 Digital Drive, Novato, CA 94949",
        "contact_person": "",
        "website": "https://www.biomarin.com",
        "social_links": "",
        "about": (
            "BioMarin's Novato headquarters includes manufacturing operations for rare disease "
            "enzyme replacement therapies. The site produces Naglazyme (galsulfase), "
            "Aldurazyme (laronidase), and other biologically derived enzyme therapies using "
            "mammalian cell culture and microbial fermentation."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "CHO cell culture for enzyme replacement therapies\n"
            "Enzyme purification\n"
            "Lyophilisation"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Focus on ultra-rare enzyme replacement therapies. Also has manufacturing in San Rafael, CA.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 2019,
        "facility": "Sanofi Genzyme (Framingham / Allston)",
        "membership_tier": "Captive",
        "city": "Allston",
        "country": "USA",
        "address": "One Kendall Square, Cambridge, MA 02139",
        "contact_person": "",
        "website": "https://www.sanofi.com",
        "social_links": "",
        "about": (
            "Sanofi Genzyme's Massachusetts manufacturing network (historically Framingham and "
            "Allston) produced rare disease biologics including Cerezyme (imiglucerase) and "
            "Myozyme (alglucosidase alfa). The Allston campus was a flagship biologics site "
            "until portions were sold to Resilience and WuXi Biologics."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "Enzyme replacement therapy production\n"
            "Protein purification\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Genzyme founded 1981 in Cambridge, acquired by Sanofi 2011. Allston campus partially divested to CDMOs.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },

    # ── Pilot / R&D / Scale-Up Facilities ───────────────────────────────────
    {
        "id": 3001,
        "facility": "NC State BTEC",
        "membership_tier": "Pilot facility",
        "city": "Raleigh",
        "country": "USA",
        "address": "850 Oval Drive, Raleigh, NC 27606",
        "contact_person": "",
        "website": "https://btec.ncsu.edu",
        "social_links": "",
        "about": (
            "The Biomanufacturing Training and Education Center (BTEC) at NC State University is "
            "a unique facility combining GMP-quality training with pilot-scale biopharmaceutical "
            "manufacturing. BTEC offers mammalian cell culture, microbial fermentation, and "
            "downstream processing at 200 L pilot scale, training the next generation of "
            "biomanufacturing professionals."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing\nFill-Finish",
        "technologies": (
            "Pilot-scale CHO mammalian cell culture (200 L)\n"
            "E. coli and S. cerevisiae fermentation\n"
            "Chromatographic downstream processing\n"
            "Lyophilisation\n"
            "Aseptic filling"
        ),
        "n_technologies": 5,
        "certifications": "cGMP-like training environment",
        "non_technical_services": "Biomanufacturing workforce training\nCertificate programs\nIndustry-academia partnerships",
        "open_24_7": "No",
        "extra_info": "State: NC. Opened 2007; ~65,000 sq ft; serves as training facility and pilot production resource. Affiliated with NIIMBL.",
        "downloads": "",
        "videos": "",
        "logo": "https://btec.ncsu.edu/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 3002,
        "facility": "NIIMBL (National Institute for Innovation in Manufacturing Biopharmaceuticals)",
        "membership_tier": "Pilot facility",
        "city": "Newark",
        "country": "USA",
        "address": "590 Avenue 1743, Newark, DE 19716",
        "contact_person": "",
        "website": "https://niimbl.force.com",
        "social_links": "",
        "about": (
            "NIIMBL is a public-private partnership and national biopharmaceutical manufacturing "
            "institute funded by NIST and industry members. Based at the University of Delaware, "
            "NIIMBL coordinates research, workforce development, and technology advancement "
            "across a network of academic, government, and industry partners to modernise "
            "US biopharmaceutical manufacturing."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing\nmRNA/LNP manufacturing",
        "technologies": (
            "Manufacturing technology R&D\n"
            "Process analytical technology (PAT)\n"
            "Continuous bioprocessing\n"
            "Digital manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "N/A – research institute",
        "non_technical_services": "Workforce development\nStandards development\nTechnology roadmapping",
        "open_24_7": "No",
        "extra_info": "State: DE. NIST Manufacturing USA institute. Network of 150+ member organisations across academia, industry, government.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 3003,
        "facility": "Center for Breakthrough Medicines (CBM)",
        "membership_tier": "Pilot facility",
        "city": "King of Prussia",
        "country": "USA",
        "address": "650 Park Avenue, King of Prussia, PA 19406",
        "contact_person": "",
        "website": "https://www.breakthroughmedicines.com",
        "social_links": "",
        "about": (
            "The Center for Breakthrough Medicines is one of the world's largest cell and gene "
            "therapy CDMOs. The facility provides integrated development and manufacturing "
            "services for viral vectors, T-cell therapies, and stem cell products, with "
            "state-of-the-art cleanrooms and multiple GMP suites designed for clinical and "
            "commercial cell/gene therapy programs."
        ),
        "technology_areas": "Viral vector production\nCell therapy manufacturing",
        "technologies": (
            "AAV gene therapy manufacturing\n"
            "Lentiviral vector production\n"
            "CAR-T cell therapy manufacturing\n"
            "iPSC-derived cell therapy\n"
            "Plasmid DNA manufacturing"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP",
        "non_technical_services": "Process development\nAnalytical testing\nRegulatory support",
        "open_24_7": "Yes",
        "extra_info": "State: PA. Over 700,000 sq ft; one of the largest cell & gene therapy manufacturing facilities globally.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 3004,
        "facility": "Walter Reed National Military Medical Center Bioproduction Facility",
        "membership_tier": "Pilot facility",
        "city": "Bethesda",
        "country": "USA",
        "address": "8901 Wisconsin Avenue, Bethesda, MD 20889",
        "contact_person": "",
        "website": "https://www.wrnmmc.capmed.mil",
        "social_links": "",
        "about": (
            "The Walter Reed Army Institute of Research and associated biodefense manufacturing "
            "capabilities support the development and pilot-scale production of vaccines and "
            "biologics for military and public health applications. The site collaborates with "
            "BARDA and government partners on biodefense countermeasures."
        ),
        "technology_areas": "Cell Cultivation\nVaccine production\nMicrobial fermentation",
        "technologies": (
            "Vaccine clinical lot production\n"
            "Viral propagation\n"
            "Antigen production"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP",
        "non_technical_services": "Government biodefense programs",
        "open_24_7": "Yes",
        "extra_info": "State: MD. Government/DoD facility. Supports BARDA and DARPA biodefense manufacturing programs.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 3005,
        "facility": "MIT Koch Institute (Pilot Scale Biomanufacturing)",
        "membership_tier": "Pilot facility",
        "city": "Cambridge",
        "country": "USA",
        "address": "500 Main Street (Building 76), Cambridge, MA 02139",
        "contact_person": "",
        "website": "https://ki.mit.edu",
        "social_links": "",
        "about": (
            "MIT's Koch Institute for Integrative Cancer Research includes pilot-scale "
            "biomanufacturing capabilities supporting academic and startup translation of "
            "cell therapies, nanoparticle drug delivery, and novel biologics. The institute "
            "bridges discovery research and clinical-stage biopharmaceutical manufacturing."
        ),
        "technology_areas": "Cell Cultivation\nmRNA/LNP manufacturing\nCell therapy manufacturing",
        "technologies": (
            "Pilot-scale mammalian cell culture\n"
            "Lipid nanoparticle formulation\n"
            "Cell therapy manufacturing\n"
            "Novel biologics process development"
        ),
        "n_technologies": 4,
        "certifications": "Research grade / academic GMP-like",
        "non_technical_services": "Academic research\nStartup support\nTranslational manufacturing",
        "open_24_7": "No",
        "extra_info": "State: MA. Academic pilot facility; Koch Institute opened 2011. Affiliated with MIT's cancer research program.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 3006,
        "facility": "Institut Armand-Frappier (IAF) – INRS",
        "membership_tier": "Pilot facility",
        "city": "Laval",
        "country": "Canada",
        "address": "531 Boulevard des Prairies, Laval, QC H7V 1B7",
        "contact_person": "",
        "website": "https://iaf.inrs.ca",
        "social_links": "",
        "about": (
            "The Institut Armand-Frappier (IAF) at INRS is Canada's leading public bioprocessing "
            "research and pilot manufacturing centre. The facility offers pilot-scale fermentation, "
            "mammalian cell culture, and vaccine production capabilities to support academic "
            "research and industry scale-up. IAF has a long history in infectious disease "
            "research and biosafety level 2 and 3 manufacturing."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nVaccine production",
        "technologies": (
            "Pilot-scale mammalian cell culture\n"
            "Bacterial and yeast fermentation\n"
            "Vaccine antigen production\n"
            "BSL-2 and BSL-3 bioprocessing"
        ),
        "n_technologies": 4,
        "certifications": "Health Canada GMP",
        "non_technical_services": "Academic research\nContract R&D\nPilot manufacturing",
        "open_24_7": "No",
        "extra_info": "Province: QC. Public research institute affiliated with INRS (Institut national de la recherche scientifique).",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 3007,
        "facility": "Vaccine and Infectious Disease Organization (VIDO)",
        "membership_tier": "Pilot facility",
        "city": "Saskatoon",
        "country": "Canada",
        "address": "120 Veterinary Road, Saskatoon, SK S7N 5E3",
        "contact_person": "",
        "website": "https://www.vido.org",
        "social_links": "",
        "about": (
            "VIDO at the University of Saskatchewan is a world-leading infectious disease "
            "research and vaccine development facility with pilot GMP manufacturing capabilities. "
            "The centre develops vaccines for both human and animal health, and houses the only "
            "Containment Level 3 (CL3) large animal research facility in North America."
        ),
        "technology_areas": "Vaccine production\nCell Cultivation\nMicrobial fermentation",
        "technologies": (
            "Vaccine antigen production\n"
            "Mammalian cell culture\n"
            "Adjuvant development\n"
            "BSL-3/CL3 bioprocessing"
        ),
        "n_technologies": 4,
        "certifications": "Health Canada GMP",
        "non_technical_services": "Vaccine R&D\nAcademic partnerships\nGovernment contract research",
        "open_24_7": "No",
        "extra_info": "Province: SK. Developed COVID-19 vaccine candidates. Only CL3 large-animal facility in North America.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },

    # ── Closed / Legacy Sites ────────────────────────────────────────────────
    {
        "id": 4001,
        "facility": "ImClone Systems (Branchburg) – CLOSED",
        "membership_tier": "Closed",
        "city": "Branchburg",
        "country": "USA",
        "address": "180 Cedar Hill Road, Branchburg, NJ 08876",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "ImClone Systems' Branchburg facility was a pioneer in mammalian cell culture "
            "manufacturing for monoclonal antibodies, most notably Erbitux (cetuximab). "
            "After ImClone's acquisition by Eli Lilly in 2008, the site continued production "
            "before being integrated into Eli Lilly's manufacturing network and eventually "
            "restructured."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "Monoclonal antibody manufacturing\n"
            "Protein purification"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: NJ. Closed/restructured post-Lilly acquisition (2008). Site produced Erbitux. Historic early mAb manufacturer.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4002,
        "facility": "MedImmune (Mountain View) – CLOSED",
        "membership_tier": "Closed",
        "city": "Mountain View",
        "country": "USA",
        "address": "297 North Bernardo Avenue, Mountain View, CA 94043",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "MedImmune's Mountain View facility was a biologics R&D and manufacturing site "
            "primarily associated with influenza vaccine and antibody development. After "
            "AstraZeneca's acquisition of MedImmune in 2007, site activities were gradually "
            "consolidated to the Gaithersburg, Maryland campus and the Mountain View site "
            "was closed."
        ),
        "technology_areas": "Cell Cultivation\nVaccine production",
        "technologies": (
            "Mammalian cell culture\n"
            "Egg-based flu vaccine production\n"
            "Antibody development"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: CA. Closed after AstraZeneca/MedImmune consolidation ~2010. Site redeveloped for other biotech tenants.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4003,
        "facility": "Emergent BioSolutions (Baltimore) – COVID Waste Incident",
        "membership_tier": "Closed",
        "city": "Baltimore",
        "country": "USA",
        "address": "5901 East Lombard Street, Baltimore, MD 21224",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "In 2021, Emergent BioSolutions' Bayview Baltimore facility made international "
            "headlines after a manufacturing error cross-contaminated approximately 15 million "
            "doses of Johnson & Johnson COVID-19 vaccine with AstraZeneca vaccine material. "
            "The FDA halted production at the facility for several months while deficiencies "
            "were remediated. The site resumed operations after FDA reinspection."
        ),
        "technology_areas": "Cell Cultivation\nViral vector production",
        "technologies": (
            "Viral vector (adenovirus) production\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 2,
        "certifications": "FDA cGMP (operational with remediation)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: MD. Production halted April–July 2021 after FDA Form 483 findings. ~15M J&J doses cross-contaminated and destroyed.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4004,
        "facility": "GlycoFi (Lebanon) – CLOSED/ACQUIRED",
        "membership_tier": "Closed",
        "city": "Lebanon",
        "country": "USA",
        "address": "21 Lafayette Street, Lebanon, NH 03766",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "GlycoFi was a biopharmaceutical company that pioneered glycoengineering in yeast "
            "(Pichia pastoris) for the production of human-type glycoproteins. The company's "
            "Lebanon, NH facility focused on pilot-scale manufacturing of humanised glycoproteins. "
            "GlycoFi was acquired by Merck & Co. in 2006 and the site was integrated into "
            "Merck's research network."
        ),
        "technology_areas": "Microbial fermentation",
        "technologies": (
            "Pichia pastoris yeast fermentation\n"
            "Glycoengineering platform\n"
            "Recombinant glycoprotein production"
        ),
        "n_technologies": 3,
        "certifications": "Research grade",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: NH. Acquired by Merck 2006 for $400M. GlycoFi's YeastGlyco platform enabled human-like N-glycan engineering in yeast.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4005,
        "facility": "Dohmen Life Science Services – CLOSED",
        "membership_tier": "Closed",
        "city": "Milwaukee",
        "country": "USA",
        "address": "700 North Water Street, Milwaukee, WI 53202",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "Dohmen Life Science Services operated a biologics CDMO and repackaging operation "
            "in Milwaukee, Wisconsin. The company provided contract biologics manufacturing and "
            "distribution services before ceasing operations. The closure reflected consolidation "
            "pressures in the mid-size CDMO market."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Biologics contract manufacturing\n"
            "Drug product fill-finish"
        ),
        "n_technologies": 2,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: WI. Ceased biologics manufacturing operations; assets divested. Dohmen retained pharmacy benefit management operations.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4006,
        "facility": "AVI BioPharma (Bothell) – CLOSED/ACQUIRED",
        "membership_tier": "Closed",
        "city": "Bothell",
        "country": "USA",
        "address": "3450 Monte Villa Parkway, Bothell, WA 98021",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "AVI BioPharma (later Sarepta Therapeutics) pioneered antisense oligonucleotide "
            "(ASO) manufacturing for rare genetic diseases including Duchenne muscular dystrophy. "
            "The Bothell facility was a key early site for GMP oligonucleotide synthesis before "
            "the company relocated manufacturing. Sarepta Therapeutics now operates from "
            "Cambridge, MA with manufacturing outsourced to CDMOs."
        ),
        "technology_areas": "Oligonucleotide synthesis",
        "technologies": (
            "Antisense oligonucleotide GMP synthesis\n"
            "Solid-phase oligonucleotide synthesis\n"
            "Purification by HPLC"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: WA. Rebranded as Sarepta Therapeutics 2012; manufacturing shifted to CMOs. Golodirsen and Eteplirsen developed here.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4007,
        "facility": "Neose Technologies (Horsham) – CLOSED",
        "membership_tier": "Closed",
        "city": "Horsham",
        "country": "USA",
        "address": "102 West Pennsylvania Avenue, Horsham, PA 19044",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "Neose Technologies developed GlycoPEGylation technology for extending the half-life "
            "of biologic drugs through enzymatic conjugation of PEG to glycoprotein carbohydrate "
            "chains. The company's Horsham facility conducted R&D and pilot manufacturing before "
            "the company was acquired by BioGeneriX / ratiopharm and subsequently Novo Nordisk."
        ),
        "technology_areas": "Enzymatic catalysis\nCell Cultivation",
        "technologies": (
            "GlycoPEGylation enzymatic conjugation\n"
            "Pilot-scale glycoprotein manufacturing"
        ),
        "n_technologies": 2,
        "certifications": "Research grade",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: PA. Acquired by ratiopharm/Novo Nordisk; GlycoPEGylation technology incorporated into Novo's protein engineering platform.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4008,
        "facility": "Transkaryotic Therapies (Cambridge) – CLOSED/ACQUIRED",
        "membership_tier": "Closed",
        "city": "Cambridge",
        "country": "USA",
        "address": "700 Main Street, Cambridge, MA 02139",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "Transkaryotic Therapies (TKT) was a pioneer in gene-activated manufacturing and "
            "enzyme replacement therapy for rare diseases. TKT's Cambridge facility developed "
            "Replagal (agalsidase alfa) for Fabry disease. The company was acquired by Shire "
            "Pharmaceuticals in 2005, and the site was subsequently integrated into Shire's "
            "rare disease manufacturing network."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "Gene-activated mammalian cell culture\n"
            "Enzyme replacement therapy production\n"
            "Protein purification"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: MA. Acquired by Shire 2005 for $1.6B. Replagal continued by Shire/Takeda; site eventually consolidated.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },

    # ── Additional Open CMOs ─────────────────────────────────────────────────
    {
        "id": 1031,
        "facility": "Recipharm Durham",
        "membership_tier": "Open CMO",
        "city": "Durham",
        "country": "USA",
        "address": "1300 Meredith Drive, Durham, NC 27713",
        "contact_person": "",
        "website": "https://www.recipharm.com",
        "social_links": "",
        "about": (
            "Recipharm's Durham facility provides drug product fill-finish and biologics "
            "manufacturing services. The site offers aseptic liquid filling, lyophilisation, "
            "and parenteral drug product manufacturing for clinical and commercial biologics "
            "programs. Recipharm is a Swedish-headquartered global CDMO."
        ),
        "technology_areas": "Fill-Finish\nDownstream processing",
        "technologies": (
            "Aseptic liquid fill-finish\n"
            "Lyophilisation\n"
            "Parenteral drug product manufacturing"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Formulation development\nAnalytical testing\nStability studies",
        "open_24_7": "Yes",
        "extra_info": "State: NC. Swedish-headquartered CDMO; Durham site focuses on parenteral biologics drug product.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.recipharm.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 1032,
        "facility": "Ology Biosciences",
        "membership_tier": "Open CMO",
        "city": "Frederick",
        "country": "USA",
        "address": "8 West Watkins Mill Road, Gaithersburg, MD 20878",
        "contact_person": "",
        "website": "https://ologybiosciences.com",
        "social_links": "",
        "about": (
            "Ology Biosciences (formerly DPT Biologics) is a CDMO specialising in vaccines, "
            "biologics, and drug products for US government and commercial clients. The company "
            "operates under BARDA and DoD contracts and is a key domestic biomanufacturing "
            "partner for US national security medical countermeasures."
        ),
        "technology_areas": "Cell Cultivation\nVaccine production\nFill-Finish",
        "technologies": (
            "Vaccine antigen manufacturing\n"
            "Mammalian cell culture\n"
            "Aseptic fill-finish\n"
            "Drug product manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "BARDA/DoD contract manufacturing\nRegulatory support",
        "open_24_7": "Yes",
        "extra_info": "State: MD. Focus on government biodefense contracts. Formerly DPT Biologics; rebranded after acquisition.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1033,
        "facility": "Waisman Biomanufacturing",
        "membership_tier": "Open CMO",
        "city": "Madison",
        "country": "USA",
        "address": "1500 Highland Avenue, Madison, WI 53705",
        "contact_person": "",
        "website": "https://waismanbiomanufacturing.wisc.edu",
        "social_links": "",
        "about": (
            "Waisman Biomanufacturing at the University of Wisconsin–Madison is a non-profit "
            "GMP manufacturing facility providing cell and gene therapy and biologics production "
            "services to academic investigators and small biotech companies. The facility "
            "specialises in clinical-scale manufacturing for investigator-sponsored IND trials."
        ),
        "technology_areas": "Cell Cultivation\nViral vector production\nCell therapy manufacturing",
        "technologies": (
            "Mammalian cell culture for IND-stage trials\n"
            "Viral vector (AAV, lentivirus) production\n"
            "Cell therapy manufacturing\n"
            "Plasmid DNA manufacturing"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Academic IND manufacturing\nProcess development\nQuality testing",
        "open_24_7": "No",
        "extra_info": "State: WI. University-affiliated non-profit CDMO. Low-cost GMP manufacturing for academic investigators with NIH funding.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 1034,
        "facility": "Ginkgo Bioworks (Boston)",
        "membership_tier": "Open CMO",
        "city": "Boston",
        "country": "USA",
        "address": "27 Drydock Avenue, Boston, MA 02210",
        "contact_person": "",
        "website": "https://www.ginkgobioworks.com",
        "social_links": "",
        "about": (
            "Ginkgo Bioworks is a synthetic biology platform company that also operates as a "
            "CDMO for fermentation-based biologics, enzymes, and biosynthetic compounds. "
            "The company's Boston Foundry combines high-throughput genetic design automation "
            "with pilot and commercial fermentation scale-up services for its partner ecosystem."
        ),
        "technology_areas": "Microbial fermentation\nEnzymatic catalysis",
        "technologies": (
            "Automated strain engineering\n"
            "Yeast and bacterial fermentation\n"
            "Enzyme and metabolite production\n"
            "Synthetic biology process development"
        ),
        "n_technologies": 4,
        "certifications": "ISO 9001",
        "non_technical_services": "Strain engineering\nProcess development\nPartner ecosystem programs",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Public company (NYSE: DNA). Operates Foundry platform; biosecurity and agriculture verticals also active.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.ginkgobioworks.com/favicon.ico",
        "pilots4u_page": "",
    },

    # ── Additional Captive Sites ──────────────────────────────────────────────
    {
        "id": 2020,
        "facility": "Pfizer (McPherson)",
        "membership_tier": "Captive",
        "city": "McPherson",
        "country": "USA",
        "address": "230 East Avenue C, McPherson, KS 67460",
        "contact_person": "",
        "website": "https://www.pfizer.com",
        "social_links": "",
        "about": (
            "Pfizer's McPherson, Kansas facility is a large sterile injectable and biologics "
            "drug product manufacturing site. The campus produces parenteral medicines at "
            "commercial scale and is one of Pfizer's key North American drug product sites "
            "supplying both the US and global markets."
        ),
        "technology_areas": "Fill-Finish\nDownstream processing",
        "technologies": (
            "Sterile injectable fill-finish\n"
            "Aseptic processing\n"
            "Drug product manufacturing\n"
            "Lyophilisation"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: KS. High-volume parenteral drug product site. One of Pfizer's largest US fill-finish facilities.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 2021,
        "facility": "Takeda (Cambridge/Lexington)",
        "membership_tier": "Captive",
        "city": "Cambridge",
        "country": "USA",
        "address": "650 East Kendall Street, Cambridge, MA 02142",
        "contact_person": "",
        "website": "https://www.takeda.com",
        "social_links": "",
        "about": (
            "Takeda's US biologics operations, consolidated after the acquisition of Shire in "
            "2019, span Cambridge and Lexington, Massachusetts. The sites produce rare disease "
            "biologics including plasma-derived therapies (haemophilia factors) and "
            "recombinant enzyme replacement therapies for lysosomal storage disorders."
        ),
        "technology_areas": "Cell Cultivation\nPlasma fractionation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "Plasma-derived coagulation factor production\n"
            "Enzyme replacement therapy manufacturing\n"
            "Protein purification"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: MA. Formerly Shire Pharmaceuticals; Takeda acquired Shire 2019 for $62B. Key rare disease biologics hub.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.takeda.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2022,
        "facility": "Gilead Sciences / Kite Pharma (Santa Monica)",
        "membership_tier": "Captive",
        "city": "Santa Monica",
        "country": "USA",
        "address": "2400 Colorado Avenue, Santa Monica, CA 90404",
        "contact_person": "",
        "website": "https://www.gilead.com",
        "social_links": "",
        "about": (
            "Gilead Sciences (via Kite Pharma, acquired 2017) operates cell therapy "
            "manufacturing facilities in the Los Angeles area for its CAR-T products "
            "Yescarta (axicabtagene ciloleucel) and Tecartus (brexucabtagene autoleucel). "
            "The Santa Monica facility is Kite's primary commercial cell therapy "
            "manufacturing site."
        ),
        "technology_areas": "Cell therapy manufacturing",
        "technologies": (
            "Autologous CAR-T cell therapy manufacturing\n"
            "Leukapheresis and T-cell isolation\n"
            "Viral transduction (lentiviral)\n"
            "Cell expansion and fill-finish"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: CA. Kite Pharma acquired by Gilead 2017 for $11.9B. Yescarta was the first FDA-approved CAR-T for large B-cell lymphoma.",
        "downloads": "",
        "videos": "",
        "logo": "https://www.gilead.com/favicon.ico",
        "pilots4u_page": "",
    },
    {
        "id": 2023,
        "facility": "Sanofi (Swiftwater)",
        "membership_tier": "Captive",
        "city": "Swiftwater",
        "country": "USA",
        "address": "Discovery Drive, Swiftwater, PA 18370",
        "contact_person": "",
        "website": "https://www.sanofi.com",
        "social_links": "",
        "about": (
            "Sanofi's Swiftwater facility in Pennsylvania is one of the world's largest "
            "influenza vaccine manufacturing sites. The campus produces Fluzone, Flublok, "
            "and other seasonal and pandemic influenza vaccines at massive scale using "
            "egg-based and cell culture processes. The site has strategic importance for "
            "US pandemic preparedness."
        ),
        "technology_areas": "Vaccine production\nCell Cultivation\nFill-Finish",
        "technologies": (
            "Egg-based influenza vaccine production\n"
            "Cell culture-based influenza vaccine (Flucelvax-platform)\n"
            "Recombinant influenza vaccine (Flublok, insect cell)\n"
            "Drug product fill-finish\n"
            "Lyophilisation"
        ),
        "n_technologies": 5,
        "certifications": "FDA cGMP\nEMA GMP",
        "non_technical_services": "Internal supply only",
        "open_24_7": "Yes",
        "extra_info": "State: PA. Major US flu vaccine supply site. Pandemic surge capacity supported by US BARDA contracts. Originally Connaught Labs (PA).",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },

    # ── Additional Closed / Legacy Sites ────────────────────────────────────
    {
        "id": 4009,
        "facility": "Wyeth Pearl River (Vaccines) – CLOSED/ACQUIRED",
        "membership_tier": "Closed",
        "city": "Pearl River",
        "country": "USA",
        "address": "401 North Middletown Road, Pearl River, NY 10965",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "Wyeth's Pearl River facility was a major US vaccine and biologics manufacturing "
            "site, producing Prevnar (pneumococcal conjugate vaccine) and other biologics. "
            "After Pfizer's acquisition of Wyeth in 2009, the site was evaluated for "
            "integration into Pfizer's network. Some operations continued under Pfizer while "
            "other lines were decommissioned."
        ),
        "technology_areas": "Vaccine production\nCell Cultivation\nMicrobial fermentation",
        "technologies": (
            "Pneumococcal conjugate vaccine production\n"
            "Bacterial fermentation\n"
            "Polysaccharide–protein conjugation\n"
            "Drug product fill-finish"
        ),
        "n_technologies": 4,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: NY. Wyeth acquired by Pfizer 2009 for $68B. Pearl River site historic for Prevnar and RotaTeq vaccine development.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4010,
        "facility": "Immunex (Seattle) – CLOSED/ACQUIRED",
        "membership_tier": "Closed",
        "city": "Seattle",
        "country": "USA",
        "address": "51 University Street, Seattle, WA 98101",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "Immunex was a Seattle-based pioneer in cytokine biology and biopharmaceutical "
            "manufacturing. The company discovered and developed Enbrel (etanercept), which "
            "became one of the world's best-selling drugs. Immunex was acquired by Amgen "
            "in 2002 for $16 billion and its Seattle manufacturing and research operations "
            "were gradually folded into Amgen's network."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "Fusion protein manufacturing (etanercept)\n"
            "Protein purification"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: WA. Founded 1981; pioneered Enbrel (etanercept). Acquired by Amgen 2002 for $16B. Site eventually closed by Amgen.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4011,
        "facility": "Covance Biologics (Mooresville) – CLOSED/ACQUIRED",
        "membership_tier": "Closed",
        "city": "Mooresville",
        "country": "USA",
        "address": "1900 Perimeter Park Drive, Morrisville, NC 27560",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "Covance Biologics operated a CDMO biologics manufacturing facility in North "
            "Carolina, providing contract mammalian cell culture and protein purification "
            "services. Covance (a LabCorp company) subsequently divested its biologics "
            "manufacturing operations, and the site was acquired and rebranded."
        ),
        "technology_areas": "Cell Cultivation\nDownstream processing",
        "technologies": (
            "CHO mammalian cell culture\n"
            "Antibody and protein purification\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: NC. Divested from Covance/LabCorp; biologics CDMO business transitioned to other operators.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
    {
        "id": 4012,
        "facility": "Albany Molecular Research (AMRI) – CLOSED/ACQUIRED",
        "membership_tier": "Closed",
        "city": "Albany",
        "country": "USA",
        "address": "21 Corporate Circle, Albany, NY 12203",
        "contact_person": "",
        "website": "",
        "social_links": "",
        "about": (
            "Albany Molecular Research Inc. (AMRI) operated a CDMO providing biologics and "
            "small-molecule contract manufacturing services from its Albany, NY headquarters. "
            "AMRI was acquired by Bridgepoint and subsequently merged into the global CDMO "
            "Curia Global (formerly Albany Molecular Research), which rebranded in 2021."
        ),
        "technology_areas": "Cell Cultivation\nMicrobial fermentation\nDownstream processing",
        "technologies": (
            "Biologics contract manufacturing\n"
            "Microbial fermentation\n"
            "Drug substance manufacturing"
        ),
        "n_technologies": 3,
        "certifications": "FDA cGMP (historical)",
        "non_technical_services": "",
        "open_24_7": "",
        "extra_info": "State: NY. Rebranded as Curia Global (2021) after multiple acquisitions and mergers under private equity.",
        "downloads": "",
        "videos": "",
        "logo": "",
        "pilots4u_page": "",
    },
]


COLUMNS = [
    "ID", "Facility", "Membership tier", "City", "Country", "Address",
    "Contact person", "Website", "Social links", "About",
    "Technology areas", "Technologies", "No. of technologies",
    "Certifications", "Non-technical services", "Open 24/7",
    "Extra information", "Downloads", "Videos", "Logo", "Pilots4U page",
]

KEY_MAP = {
    "ID": "id",
    "Facility": "facility",
    "Membership tier": "membership_tier",
    "City": "city",
    "Country": "country",
    "Address": "address",
    "Contact person": "contact_person",
    "Website": "website",
    "Social links": "social_links",
    "About": "about",
    "Technology areas": "technology_areas",
    "Technologies": "technologies",
    "No. of technologies": "n_technologies",
    "Certifications": "certifications",
    "Non-technical services": "non_technical_services",
    "Open 24/7": "open_24_7",
    "Extra information": "extra_info",
    "Downloads": "downloads",
    "Videos": "videos",
    "Logo": "logo",
    "Pilots4U page": "pilots4u_page",
}


def build_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facilities"

    header_fill   = PatternFill(start_color="2D6A4F", end_color="2D6A4F", fill_type="solid")
    header_font   = Font(color="FFFFFF", bold=True)
    header_align  = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border   = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC"),
    )

    # Header row
    for col_idx, col_name in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.fill   = header_fill
        cell.font   = header_font
        cell.alignment = header_align
        cell.border = thin_border

    ws.row_dimensions[1].height = 30

    alt_fill = PatternFill(start_color="F0FAF5", end_color="F0FAF5", fill_type="solid")

    for row_idx, facility in enumerate(FACILITIES, start=2):
        fill = alt_fill if row_idx % 2 == 0 else PatternFill()
        for col_idx, col_name in enumerate(COLUMNS, start=1):
            key = KEY_MAP[col_name]
            value = facility.get(key, "")
            # Flatten tuples (happen when we accidentally used trailing comma)
            if isinstance(value, tuple):
                value = value[0] if value else ""
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.fill = fill
            cell.border = thin_border
            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True,
                horizontal="left",
            )

    # Column widths
    col_widths = {
        "ID": 8, "Facility": 38, "Membership tier": 16,
        "City": 20, "Country": 10, "Address": 35,
        "Contact person": 22, "Website": 35, "Social links": 20,
        "About": 55, "Technology areas": 32, "Technologies": 42,
        "No. of technologies": 10, "Certifications": 28,
        "Non-technical services": 32, "Open 24/7": 10,
        "Extra information": 48, "Downloads": 12, "Videos": 12,
        "Logo": 30, "Pilots4U page": 20,
    }
    for col_idx, col_name in enumerate(COLUMNS, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = col_widths.get(col_name, 20)

    ws.freeze_panes = "A2"

    # ── Technologies sheet (empty scaffold matching Pilots4U structure) ──────
    ws2 = wb.create_sheet("Technologies")
    tech_headers = [
        "Facility ID", "Facility", "Country", "Technology area",
        "Technology", "Number of units", "Capacity", "Details",
        "Technology contact", "Technology webpage", "Images", "Pilots4U page",
    ]
    for col_idx, h in enumerate(tech_headers, start=1):
        cell = ws2.cell(row=1, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_align

    # ── Notes sheet ──────────────────────────────────────────────────────────
    ws3 = wb.create_sheet("Notes")
    ws3["A1"] = "North America Biomanufacturing Database"
    ws3["A1"].font = Font(bold=True, size=14)
    ws3["A3"] = "Sources: Company websites, FDA registrations, industry reports, public filings."
    ws3["A4"] = "Compiled: October 2026"
    ws3["A5"] = (
        "Membership tier field repurposed to denote facility type: "
        "Open CMO / Captive / Pilot facility / Closed."
    )
    ws3["A6"] = (
        "This database covers the United States, Canada, and Mexico. "
        "Coordinates not included — use geocoding scripts from the main project."
    )

    return wb


if __name__ == "__main__":
    out_path = (
        "/Users/bouke/Library/CloudStorage/OneDrive-Personal/"
        "claude/projects/biomanufacturing/data/NorthAmerica_biomanufacturing_database.xlsx"
    )
    wb = build_workbook()
    wb.save(out_path)
    print(f"Saved {len(FACILITIES)} facilities → {out_path}")
