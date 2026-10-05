# Biomanufacturing Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a web app with a searchable/filterable facility table and a synced interactive map for biomanufacturing and CMO facilities worldwide.

**Architecture:** A Next.js 14 App Router application with a static JSON data layer. TanStack Table drives a fully filterable, sortable, expandable facility library. React-Leaflet renders facility markers on a map. Both views share a single `useFacilityFilters` hook so filtering either updates both simultaneously.

**Tech Stack:** Next.js 14 · React 18 · TypeScript · Tailwind CSS · TanStack Table v8 · React-Leaflet 4 · Leaflet 1.9 · Vercel

**Spec:** `CLAUDE.md` (project root)

## Global Constraints

- Node ≥ 20, npm ≥ 10
- Next.js 14 App Router (`src/app/`) — no Pages Router
- TypeScript strict mode throughout — no `any` except where Leaflet requires it
- Tailwind CSS only — no inline `style=` except inside Leaflet div-icons
- All text content from the spec — do not invent copy
- Leaflet map must be dynamically imported with `ssr: false` — Leaflet uses `window` and breaks SSR
- Seed data: ≥ 20 real, named biomanufacturing/CMO facilities with accurate coordinates
- No API keys required for MVP — use OpenStreetMap tiles (free, no key)

---

## File Map

```
biomanufacturing/
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── data/
│   └── facilities.json          ← master dataset (20+ seed records)
├── src/
│   ├── types/
│   │   └── facility.ts          ← Facility interface + Region/Modality enums
│   ├── lib/
│   │   └── facilities.ts        ← loadFacilities(), getFilterOptions()
│   ├── hooks/
│   │   └── useFacilityFilters.ts ← shared filter state (table ↔ map)
│   ├── components/
│   │   ├── FilterBar.tsx         ← global search + modality/region/type dropdowns
│   │   ├── FacilityTable/
│   │   │   ├── columns.tsx       ← TanStack column definitions
│   │   │   ├── FacilityTable.tsx ← table + column header filters
│   │   │   └── FacilityDetail.tsx ← expanded row detail panel
│   │   └── FacilityMap/
│   │       ├── Map.tsx           ← actual Leaflet map (ssr:false target)
│   │       └── index.tsx         ← dynamic() wrapper, exports FacilityMap
│   └── app/
│       ├── layout.tsx
│       ├── globals.css
│       └── page.tsx              ← wires FilterBar + FacilityTable + FacilityMap
└── public/
    └── images/facilities/        ← aerial images (empty dir, images added later)
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `package.json`, `next.config.ts`, `tailwind.config.ts`, `tsconfig.json`
- Create: `src/app/layout.tsx`, `src/app/globals.css`, `src/app/page.tsx` (placeholder)
- Create: `public/images/facilities/.gitkeep`

**Interfaces:**
- Produces: running `npm run dev` serves `http://localhost:3000` with a blank page

- [ ] **Step 1: Scaffold Next.js project**

Run inside `/Users/bouke/onedrive/claude/projects/biomanufacturing/`:
```bash
npx create-next-app@14 . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-git
```
Answer prompts: accept all defaults. This creates `package.json`, `tsconfig.json`, `tailwind.config.ts`, `next.config.ts`, `src/app/`.

- [ ] **Step 2: Install additional dependencies**

```bash
npm install @tanstack/react-table react-leaflet leaflet leaflet.markercluster
npm install -D @types/leaflet @types/leaflet.markercluster
```

- [ ] **Step 3: Replace `src/app/page.tsx` with placeholder**

```tsx
// src/app/page.tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-2xl font-bold text-gray-800">
        Biomanufacturing Facility Platform
      </h1>
      <p className="mt-2 text-gray-500">Loading…</p>
    </main>
  )
}
```

- [ ] **Step 4: Replace `src/app/layout.tsx`**

```tsx
// src/app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Biomanufacturing Facility Map',
  description: 'Global overview of biomanufacturing and CMO/CDMO facilities',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

- [ ] **Step 5: Add Leaflet CSS import to `globals.css`**

```css
/* src/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@import 'leaflet/dist/leaflet.css';
@import 'leaflet.markercluster/dist/MarkerCluster.css';
@import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
```

- [ ] **Step 6: Verify dev server starts**

```bash
npm run dev
```
Expected: `http://localhost:3000` shows "Biomanufacturing Facility Platform" heading. No console errors.

- [ ] **Step 7: Create placeholder image dir**

```bash
mkdir -p public/images/facilities && touch public/images/facilities/.gitkeep
```

- [ ] **Step 8: Commit**

```bash
git init && git add -A && git commit -m "feat: scaffold Next.js 14 project with Tailwind, TanStack Table, Leaflet"
```

---

## Task 2: Data Schema + Seed Dataset

**Files:**
- Create: `src/types/facility.ts`
- Create: `data/facilities.json`

**Interfaces:**
- Produces: `Facility` type (used by all subsequent tasks)
- Produces: `facilities.json` with ≥ 20 records matching the `Facility` type exactly

- [ ] **Step 1: Write `src/types/facility.ts`**

```typescript
// src/types/facility.ts
export type FacilityType = 'CMO' | 'CDMO' | 'Captive' | 'Toll'
export type Scale = 'Development' | 'Pilot' | 'Commercial'
export type Modality =
  | 'Mammalian cell culture'
  | 'Microbial fermentation'
  | 'Fermentation (industrial)'
  | 'Viral vector'
  | 'mRNA'
  | 'ADC'
  | 'Lipid nanoparticle'
  | 'Enzymes'
  | 'Probiotics & cultures'

export interface FacilityLocation {
  city: string
  country: string
  region: 'Europe' | 'North America' | 'Asia-Pacific' | 'Other'
  lat: number
  lng: number
}

export interface Facility {
  id: string
  name: string
  owner: string
  location: FacilityLocation
  facilityType: FacilityType
  modalities: Modality[]
  scale: Scale[]
  capacity: string          // e.g. "80,000 L bioreactor volume" — empty string if unknown
  clients: string[]         // known clients; empty array if confidential
  products: string[]        // product/ingredient categories
  legacy: string            // founding year + key history (1–2 sentences)
  certifications: string[]  // e.g. ["FDA", "EMA GMP", "ISO 9001"]
  website: string
  imageUrl: string          // relative path under /images/facilities/ or empty string
  notes: string
}
```

- [ ] **Step 2: Write `data/facilities.json`**

Create the file with this exact content (20 seed facilities):

```json
[
  {
    "id": "lonza-visp",
    "name": "Lonza Visp",
    "owner": "Lonza Group AG",
    "location": { "city": "Visp", "country": "Switzerland", "region": "Europe", "lat": 46.294, "lng": 7.881 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture", "Microbial fermentation", "ADC"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "~100,000 L total bioreactor volume",
    "clients": [],
    "products": ["Monoclonal antibodies", "Recombinant proteins", "ADCs", "Small molecules"],
    "legacy": "Founded 1897 as an electrochemical plant. Pivoted to biopharmaceutical CDMO services in the 1990s; now one of the world's largest CDMO sites.",
    "certifications": ["FDA", "EMA GMP", "Swissmedic"],
    "website": "https://www.lonza.com",
    "imageUrl": "",
    "notes": "Flagship Lonza CDMO campus; multiple biologics suites."
  },
  {
    "id": "samsung-biologics-incheon",
    "name": "Samsung Biologics Incheon",
    "owner": "Samsung Biologics Co., Ltd.",
    "location": { "city": "Incheon", "country": "South Korea", "region": "Asia-Pacific", "lat": 37.456, "lng": 126.706 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture"],
    "scale": ["Commercial"],
    "capacity": "~620,000 L total bioreactor volume (4 plants)",
    "clients": ["Roche", "Bristol Myers Squibb", "Pfizer", "AstraZeneca"],
    "products": ["Monoclonal antibodies", "Biosimilars", "Recombinant proteins"],
    "legacy": "Founded 2011; built the world's largest single-site biologics manufacturing campus. Listed on KRX in 2016.",
    "certifications": ["FDA", "EMA GMP", "MFDS"],
    "website": "https://www.samsungbiologics.com",
    "imageUrl": "",
    "notes": "Plants 1–4 operational; Plant 5 under construction."
  },
  {
    "id": "wuxi-biologics-wuxi",
    "name": "WuXi Biologics Wuxi",
    "owner": "WuXi Biologics",
    "location": { "city": "Wuxi", "country": "China", "region": "Asia-Pacific", "lat": 31.574, "lng": 120.287 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture", "Microbial fermentation"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": ">180,000 L bioreactor volume across sites",
    "clients": [],
    "products": ["Monoclonal antibodies", "Bispecific antibodies", "ADCs", "Vaccines"],
    "legacy": "Founded 2010 as part of the WuXi AppTec group. Rapid expansion to become a top-3 global biologics CDMO.",
    "certifications": ["FDA", "EMA GMP", "NMPA"],
    "website": "https://www.wuxibiologics.com",
    "imageUrl": "",
    "notes": "Headquarters site; additional facilities in Ireland and the US."
  },
  {
    "id": "fujifilm-diosynth-billingham",
    "name": "Fujifilm Diosynth Biotechnologies Billingham",
    "owner": "Fujifilm Holdings",
    "location": { "city": "Billingham", "country": "United Kingdom", "region": "Europe", "lat": 54.601, "lng": -1.274 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture", "Microbial fermentation", "Viral vector"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Up to 6 × 20,000 L bioreactors",
    "clients": [],
    "products": ["Monoclonal antibodies", "Viral vectors", "Recombinant proteins"],
    "legacy": "Originated as ICI Biologicals (1980s); became Diosynth after multiple acquisitions; acquired by Fujifilm in 2011.",
    "certifications": ["MHRA", "FDA", "EMA GMP"],
    "website": "https://www.fujifilmdiosynth.com",
    "imageUrl": "",
    "notes": "Primary UK site; sister sites in Durham NC (US) and Hillerød (Denmark)."
  },
  {
    "id": "rentschler-laupheim",
    "name": "Rentschler Biopharma Laupheim",
    "owner": "Rentschler Biopharma SE",
    "location": { "city": "Laupheim", "country": "Germany", "region": "Europe", "lat": 48.230, "lng": 9.881 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Up to 4 × 15,000 L bioreactors",
    "clients": [],
    "products": ["Monoclonal antibodies", "Recombinant proteins", "Bispecific antibodies"],
    "legacy": "Family-owned company founded 1927 as a pharmaceutical manufacturer. Pivoted fully to CDMO biologics services in the 2000s.",
    "certifications": ["EMA GMP", "FDA"],
    "website": "https://www.rentschler-biopharma.com",
    "imageUrl": "",
    "notes": "Fully independent, family-owned CDMO — rare at commercial scale."
  },
  {
    "id": "boehringer-ingelheim-biberach",
    "name": "Boehringer Ingelheim BioXcellence Biberach",
    "owner": "Boehringer Ingelheim GmbH",
    "location": { "city": "Biberach an der Riß", "country": "Germany", "region": "Europe", "lat": 48.097, "lng": 9.789 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture", "Microbial fermentation"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": ">1,000,000 L total bioreactor volume (largest single-site mammalian CDMO)",
    "clients": [],
    "products": ["Monoclonal antibodies", "Bispecific antibodies", "Recombinant proteins"],
    "legacy": "Boehringer Ingelheim's biologics division started in the 1980s. BioXcellence launched as commercial CDMO brand in 2019.",
    "certifications": ["EMA GMP", "FDA"],
    "website": "https://www.boehringer-ingelheim.com/bioxcellence",
    "imageUrl": "",
    "notes": "Claims the world's largest mammalian cell culture CDMO capacity at a single site."
  },
  {
    "id": "ajinomoto-bio-pharma-olean",
    "name": "Ajinomoto Bio-Pharma Services Olean",
    "owner": "Ajinomoto Co., Inc.",
    "location": { "city": "Olean", "country": "United States", "region": "North America", "lat": 42.079, "lng": -78.429 },
    "facilityType": "CDMO",
    "modalities": ["Microbial fermentation", "ADC"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Commercial-scale fermentation up to 80,000 L",
    "clients": [],
    "products": ["Amino acids", "Peptides", "ADC payloads", "HPAPIs"],
    "legacy": "Site originated as Pfizer's fermentation facility; acquired by Ajinomoto in 2010 to expand their bio-pharma services division.",
    "certifications": ["FDA", "EMA GMP"],
    "website": "https://www.ajibio-pharma.com",
    "imageUrl": "",
    "notes": "Strong heritage in fermentation-derived small molecules and amino acids."
  },
  {
    "id": "novasep-pompey",
    "name": "Novasep Pompey",
    "owner": "Novasep",
    "location": { "city": "Pompey", "country": "France", "region": "Europe", "lat": 48.776, "lng": 6.133 },
    "facilityType": "CDMO",
    "modalities": ["Microbial fermentation"],
    "scale": ["Pilot", "Commercial"],
    "capacity": "Commercial fermentation up to 50,000 L",
    "clients": [],
    "products": ["APIs", "Vitamins", "Fermentation-derived small molecules"],
    "legacy": "Founded 1994 as a purification technology specialist; expanded into fermentation CDMO services through acquisitions.",
    "certifications": ["EMA GMP", "FDA"],
    "website": "https://www.novasep.com",
    "imageUrl": "",
    "notes": "Specialises in chromatography purification combined with fermentation."
  },
  {
    "id": "catalent-bloomington",
    "name": "Catalent Biologics Bloomington",
    "owner": "Catalent, Inc.",
    "location": { "city": "Bloomington", "country": "United States", "region": "North America", "lat": 39.165, "lng": -86.526 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture", "Viral vector"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Up to 4 × 4,000 L single-use bioreactors + fill-finish",
    "clients": [],
    "products": ["Monoclonal antibodies", "Viral vectors", "Gene therapies"],
    "legacy": "Site acquired from Eli Lilly in 2018; significantly expanded for biologics and gene therapy manufacturing.",
    "certifications": ["FDA", "EMA GMP"],
    "website": "https://www.catalent.com",
    "imageUrl": "",
    "notes": "One of Catalent's largest biologics campuses; strong in gene therapy fill-finish."
  },
  {
    "id": "kbi-biopharma-durham",
    "name": "KBI Biopharma Durham",
    "owner": "JSR Corporation",
    "location": { "city": "Durham", "country": "United States", "region": "North America", "lat": 35.994, "lng": -78.899 },
    "facilityType": "CDMO",
    "modalities": ["Mammalian cell culture", "Microbial fermentation"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Up to 2,000 L single-use bioreactors",
    "clients": [],
    "products": ["Monoclonal antibodies", "Recombinant proteins", "Vaccines"],
    "legacy": "Founded 2013; acquired by JSR Corporation (Japan) in 2020. Known for fast-track development timelines.",
    "certifications": ["FDA"],
    "website": "https://www.kbibiopharma.com",
    "imageUrl": "",
    "notes": "Focused on speed-to-clinic for early-phase biologics."
  },
  {
    "id": "novonesis-kalundborg",
    "name": "Novonesis Kalundborg",
    "owner": "Novonesis A/S",
    "location": { "city": "Kalundborg", "country": "Denmark", "region": "Europe", "lat": 55.676, "lng": 11.090 },
    "facilityType": "Captive",
    "modalities": ["Microbial fermentation", "Enzymes", "Fermentation (industrial)"],
    "scale": ["Commercial"],
    "capacity": "One of Europe's largest industrial fermentation complexes",
    "clients": ["Novo Nordisk (insulin)", "Multiple industrial customers"],
    "products": ["Enzymes", "Probiotics", "Industrial fermentation products"],
    "legacy": "Novozymes founded 2000 as spin-off from Novo Nordisk. Merged with Chr. Hansen to form Novonesis in 2024. Kalundborg site operational since the 1940s.",
    "certifications": ["ISO 9001", "ISO 14001"],
    "website": "https://www.novonesis.com",
    "imageUrl": "",
    "notes": "Part of the Kalundborg Symbiosis — the world's first industrial symbiosis ecosystem."
  },
  {
    "id": "dsm-firmenich-delft",
    "name": "dsm-firmenich Delft (Biotechnology Campus)",
    "owner": "dsm-firmenich AG",
    "location": { "city": "Delft", "country": "Netherlands", "region": "Europe", "lat": 51.989, "lng": 4.329 },
    "facilityType": "Captive",
    "modalities": ["Microbial fermentation", "Enzymes", "Probiotics & cultures"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Multiple fermentation suites at development and pilot scale",
    "clients": [],
    "products": ["Food cultures", "Probiotics", "Enzymes", "Nutritional ingredients"],
    "legacy": "Originated as Gist-Brocades (1869), became DSM in 1998 and merged with Firmenich in 2023. The Delft Biotechnology Campus is the global R&D and development heart of the company.",
    "certifications": ["ISO 9001", "FDA", "FSSC 22000"],
    "website": "https://www.dsm-firmenich.com",
    "imageUrl": "",
    "notes": "Birthplace of many fermentation biotechnology innovations; large strain and culture library."
  },
  {
    "id": "dsm-firmenich-sisseln",
    "name": "dsm-firmenich Sisseln",
    "owner": "dsm-firmenich AG",
    "location": { "city": "Sisseln", "country": "Switzerland", "region": "Europe", "lat": 47.624, "lng": 8.016 },
    "facilityType": "Captive",
    "modalities": ["Microbial fermentation", "Fermentation (industrial)"],
    "scale": ["Commercial"],
    "capacity": "Large-scale commercial fermentation for vitamins and nutritional ingredients",
    "clients": [],
    "products": ["Vitamins (B2, B12)", "Carotenoids", "Nutritional ingredients"],
    "legacy": "Site established by Hoffmann-La Roche in the 1940s for vitamin production; acquired by DSM in 2003.",
    "certifications": ["FDA", "EMA GMP", "ISO 9001"],
    "website": "https://www.dsm-firmenich.com",
    "imageUrl": "",
    "notes": "One of the world's largest fermentation-based vitamin production sites."
  },
  {
    "id": "cj-cheiljedang-incheon",
    "name": "CJ CheilJedang BIO Incheon",
    "owner": "CJ CheilJedang Corporation",
    "location": { "city": "Incheon", "country": "South Korea", "region": "Asia-Pacific", "lat": 37.478, "lng": 126.618 },
    "facilityType": "Captive",
    "modalities": ["Microbial fermentation", "Fermentation (industrial)"],
    "scale": ["Commercial"],
    "capacity": "Large-scale commercial fermentation for amino acids and food ingredients",
    "clients": [],
    "products": ["Amino acids (lysine, threonine, tryptophan)", "Nucleotides (IMP, GMP)", "Food flavor ingredients"],
    "legacy": "CJ CheilJedang (founded 1953) is one of the world's top producers of fermentation-derived amino acids and food ingredients. The BIO division was established in the 1980s.",
    "certifications": ["FDA", "FSSC 22000", "ISO 9001"],
    "website": "https://www.cj.net",
    "imageUrl": "",
    "notes": "Global leader in fermentation-derived savory and amino acid ingredients for food and feed."
  },
  {
    "id": "evonik-hanau",
    "name": "Evonik Health Care Hanau",
    "owner": "Evonik Industries AG",
    "location": { "city": "Hanau", "country": "Germany", "region": "Europe", "lat": 50.134, "lng": 8.921 },
    "facilityType": "CDMO",
    "modalities": ["Microbial fermentation", "Lipid nanoparticle"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Commercial fermentation for amino acids and pharma excipients",
    "clients": [],
    "products": ["Amino acids (pharma grade)", "Lipid excipients", "LNP formulations"],
    "legacy": "Evonik's pharma ingredients heritage traces to Degussa (founded 1843). The health care business unit was formalized in 2010.",
    "certifications": ["EMA GMP", "FDA"],
    "website": "https://health-care.evonik.com",
    "imageUrl": "",
    "notes": "Key supplier of lipid excipients used in mRNA-LNP vaccines (including COVID-19)."
  },
  {
    "id": "cerbios-lugano",
    "name": "CERBIOS-PHARMA Barbengo",
    "owner": "CERBIOS-PHARMA SA",
    "location": { "city": "Barbengo", "country": "Switzerland", "region": "Europe", "lat": 45.987, "lng": 8.929 },
    "facilityType": "CDMO",
    "modalities": ["Microbial fermentation", "ADC"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Up to 25,000 L fermenters; dedicated HPAPI containment",
    "clients": [],
    "products": ["APIs", "HPAPIs", "Fermentation-derived pharmaceuticals", "ADC payloads"],
    "legacy": "Founded 1986 as a specialty pharma manufacturer in the Ticino region of Switzerland. HPAPI and ADC capabilities added in the 2010s.",
    "certifications": ["Swissmedic", "EMA GMP", "FDA"],
    "website": "https://www.cerbios.ch",
    "imageUrl": "",
    "notes": "Specialist in cytotoxic and high-potency compounds alongside fermentation."
  },
  {
    "id": "lonza-portsmouth",
    "name": "Lonza Portsmouth (Microbial)",
    "owner": "Lonza Group AG",
    "location": { "city": "Portsmouth", "country": "United States", "region": "North America", "lat": 43.071, "lng": -70.762 },
    "facilityType": "CDMO",
    "modalities": ["Microbial fermentation"],
    "scale": ["Development", "Pilot", "Commercial"],
    "capacity": "Up to 75,000 L fermentation capacity",
    "clients": [],
    "products": ["Recombinant proteins (microbial)", "Enzymes", "Insulin precursors"],
    "legacy": "Originally part of Wyeth Biopharma. Acquired by Lonza in 2012 to strengthen microbial fermentation capabilities.",
    "certifications": ["FDA", "EMA GMP"],
    "website": "https://www.lonza.com",
    "imageUrl": "",
    "notes": "Lonza's primary microbial fermentation site in North America."
  },
  {
    "id": "fermion-oulu",
    "name": "Fermion Oulu",
    "owner": "Fermion Oy (Orion Group)",
    "location": { "city": "Oulu", "country": "Finland", "region": "Europe", "lat": 65.012, "lng": 25.472 },
    "facilityType": "CDMO",
    "modalities": ["Microbial fermentation"],
    "scale": ["Pilot", "Commercial"],
    "capacity": "Up to 63,000 L fermenters",
    "clients": [],
    "products": ["APIs", "Fermentation-derived pharmaceuticals", "Semi-synthetic antibiotics"],
    "legacy": "Fermion established 1970 as part of Orion Corporation. One of the Nordic region's leading API fermentation CDMOs.",
    "certifications": ["EMA GMP", "FDA"],
    "website": "https://www.fermion.fi",
    "imageUrl": "",
    "notes": "Nordic specialist in fermentation-derived API manufacturing."
  },
  {
    "id": "recipharm-strängnäs",
    "name": "Recipharm Strängnäs",
    "owner": "Recipharm AB",
    "location": { "city": "Strängnäs", "country": "Sweden", "region": "Europe", "lat": 59.379, "lng": 17.031 },
    "facilityType": "CDMO",
    "modalities": ["Microbial fermentation"],
    "scale": ["Pilot", "Commercial"],
    "capacity": "Fermentation suites up to 10,000 L",
    "clients": [],
    "products": ["APIs", "Fermentation-derived pharmaceuticals"],
    "legacy": "Recipharm founded 1995 in Sweden; grown to one of Europe's top CDMOs through acquisitions. The Strängnäs site specialises in fermentation-based APIs.",
    "certifications": ["EMA GMP", "FDA"],
    "website": "https://www.recipharm.com",
    "imageUrl": "",
    "notes": "Swedish CDMO with broad fermentation API heritage."
  },
  {
    "id": "bbi-biotech-berlin",
    "name": "BBI Biotech Berlin",
    "owner": "BBI Biotech GmbH",
    "location": { "city": "Berlin", "country": "Germany", "region": "Europe", "lat": 52.521, "lng": 13.405 },
    "facilityType": "CMO",
    "modalities": ["Microbial fermentation", "Mammalian cell culture"],
    "scale": ["Development", "Pilot"],
    "capacity": "Pilot fermentation and bioreactor systems up to 1,500 L",
    "clients": [],
    "products": ["Instrumentation", "Contract fermentation services"],
    "legacy": "Founded 1987 as a bioreactor instrumentation company. Expanded into contract fermentation development services.",
    "certifications": ["ISO 9001"],
    "website": "https://www.bbi-biotech.com",
    "imageUrl": "",
    "notes": "Also a leading bioreactor hardware manufacturer."
  }
]
```

- [ ] **Step 3: Verify JSON parses correctly**

```bash
node -e "const d = require('./data/facilities.json'); console.log('Records:', d.length, '| First:', d[0].name)"
```
Expected: `Records: 20 | First: Lonza Visp`

- [ ] **Step 4: Commit**

```bash
git add src/types/facility.ts data/facilities.json
git commit -m "feat: add Facility type and 20-record seed dataset"
```

---

## Task 3: Data Utilities + Filter State Hook

**Files:**
- Create: `src/lib/facilities.ts`
- Create: `src/hooks/useFacilityFilters.ts`

**Interfaces:**
- Produces: `loadFacilities(): Facility[]`
- Produces: `getFilterOptions(facilities: Facility[]): FilterOptions`
- Produces: `useFacilityFilters()` → `{ facilities, filtered, globalSearch, setGlobalSearch, modality, setModality, region, setRegion, facilityType, setFacilityType, selectedId, setSelectedId }`

- [ ] **Step 1: Write `src/lib/facilities.ts`**

```typescript
// src/lib/facilities.ts
import rawData from '../../data/facilities.json'
import type { Facility, Modality, FacilityType } from '@/types/facility'

export function loadFacilities(): Facility[] {
  return rawData as Facility[]
}

export interface FilterOptions {
  modalities: Modality[]
  regions: string[]
  facilityTypes: FacilityType[]
}

export function getFilterOptions(facilities: Facility[]): FilterOptions {
  return {
    modalities: [...new Set(facilities.flatMap((f) => f.modalities))].sort() as Modality[],
    regions: [...new Set(facilities.map((f) => f.location.region))].sort(),
    facilityTypes: [...new Set(facilities.map((f) => f.facilityType))].sort() as FacilityType[],
  }
}
```

- [ ] **Step 2: Write `src/hooks/useFacilityFilters.ts`**

```typescript
// src/hooks/useFacilityFilters.ts
'use client'
import { useState, useMemo } from 'react'
import { loadFacilities } from '@/lib/facilities'
import type { Facility, Modality, FacilityType } from '@/types/facility'

export function useFacilityFilters() {
  const facilities = useMemo(() => loadFacilities(), [])
  const [globalSearch, setGlobalSearch] = useState('')
  const [modality, setModality] = useState<Modality | ''>('')
  const [region, setRegion] = useState<string>('')
  const [facilityType, setFacilityType] = useState<FacilityType | ''>('')
  const [selectedId, setSelectedId] = useState<string | null>(null)

  const filtered = useMemo(() => {
    const q = globalSearch.toLowerCase()
    return facilities.filter((f) => {
      const matchesSearch =
        !q ||
        f.name.toLowerCase().includes(q) ||
        f.owner.toLowerCase().includes(q) ||
        f.location.city.toLowerCase().includes(q) ||
        f.location.country.toLowerCase().includes(q) ||
        f.products.some((p) => p.toLowerCase().includes(q)) ||
        f.modalities.some((m) => m.toLowerCase().includes(q))
      const matchesModality = !modality || f.modalities.includes(modality)
      const matchesRegion = !region || f.location.region === region
      const matchesType = !facilityType || f.facilityType === facilityType
      return matchesSearch && matchesModality && matchesRegion && matchesType
    })
  }, [facilities, globalSearch, modality, region, facilityType])

  return {
    facilities,
    filtered,
    globalSearch, setGlobalSearch,
    modality, setModality,
    region, setRegion,
    facilityType, setFacilityType,
    selectedId, setSelectedId,
  }
}
```

- [ ] **Step 3: Verify no TypeScript errors**

```bash
npx tsc --noEmit
```
Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add src/lib/facilities.ts src/hooks/useFacilityFilters.ts
git commit -m "feat: add data loader, filter options, and shared filter state hook"
```

---

## Task 4: FilterBar Component

**Files:**
- Create: `src/components/FilterBar.tsx`

**Interfaces:**
- Consumes: `useFacilityFilters()` return value (passed as props)
- Consumes: `getFilterOptions(facilities)` for dropdown options
- Produces: `<FilterBar />` — renders global search input + three dropdowns

- [ ] **Step 1: Write `src/components/FilterBar.tsx`**

```tsx
// src/components/FilterBar.tsx
'use client'
import { getFilterOptions } from '@/lib/facilities'
import type { Facility, Modality, FacilityType } from '@/types/facility'

interface FilterBarProps {
  facilities: Facility[]
  globalSearch: string
  setGlobalSearch: (v: string) => void
  modality: Modality | ''
  setModality: (v: Modality | '') => void
  region: string
  setRegion: (v: string) => void
  facilityType: FacilityType | ''
  setFacilityType: (v: FacilityType | '') => void
  resultCount: number
}

export default function FilterBar({
  facilities, globalSearch, setGlobalSearch,
  modality, setModality, region, setRegion,
  facilityType, setFacilityType, resultCount,
}: FilterBarProps) {
  const opts = getFilterOptions(facilities)

  return (
    <div className="flex flex-wrap gap-3 items-center p-4 bg-white border-b border-gray-200">
      <input
        type="text"
        placeholder="Search facilities, owners, products…"
        value={globalSearch}
        onChange={(e) => setGlobalSearch(e.target.value)}
        className="flex-1 min-w-[220px] px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
      />
      <select
        value={modality}
        onChange={(e) => setModality(e.target.value as Modality | '')}
        className="px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
      >
        <option value="">All modalities</option>
        {opts.modalities.map((m) => <option key={m} value={m}>{m}</option>)}
      </select>
      <select
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        className="px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
      >
        <option value="">All regions</option>
        {opts.regions.map((r) => <option key={r} value={r}>{r}</option>)}
      </select>
      <select
        value={facilityType}
        onChange={(e) => setFacilityType(e.target.value as FacilityType | '')}
        className="px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
      >
        <option value="">All types</option>
        {opts.facilityTypes.map((t) => <option key={t} value={t}>{t}</option>)}
      </select>
      <span className="text-sm text-gray-500 ml-auto whitespace-nowrap">
        {resultCount} {resultCount === 1 ? 'facility' : 'facilities'}
      </span>
    </div>
  )
}
```

- [ ] **Step 2: TypeScript check**

```bash
npx tsc --noEmit
```
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add src/components/FilterBar.tsx
git commit -m "feat: add FilterBar with global search and dropdown filters"
```

---

## Task 5: Facility Table

**Files:**
- Create: `src/components/FacilityTable/columns.tsx`
- Create: `src/components/FacilityTable/FacilityDetail.tsx`
- Create: `src/components/FacilityTable/FacilityTable.tsx`

**Interfaces:**
- Consumes: `Facility` type, `filtered: Facility[]`, `selectedId: string | null`, `setSelectedId: (id: string | null) => void`
- Produces: `<FacilityTable filtered={…} selectedId={…} setSelectedId={…} />`

- [ ] **Step 1: Write `src/components/FacilityTable/columns.tsx`**

```tsx
// src/components/FacilityTable/columns.tsx
import { createColumnHelper } from '@tanstack/react-table'
import type { Facility } from '@/types/facility'

const helper = createColumnHelper<Facility>()

export const columns = [
  helper.accessor('name', {
    header: 'Facility',
    cell: (info) => <span className="font-medium text-gray-900">{info.getValue()}</span>,
  }),
  helper.accessor('owner', {
    header: 'Owner',
    cell: (info) => <span className="text-gray-700">{info.getValue()}</span>,
  }),
  helper.accessor((row) => row.location.city + ', ' + row.location.country, {
    id: 'location',
    header: 'Location',
    cell: (info) => <span className="text-gray-600">{info.getValue()}</span>,
  }),
  helper.accessor('facilityType', {
    header: 'Type',
    cell: (info) => (
      <span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800">
        {info.getValue()}
      </span>
    ),
  }),
  helper.accessor((row) => row.modalities.join(', '), {
    id: 'modalities',
    header: 'Modalities',
    cell: (info) => <span className="text-sm text-gray-600">{info.getValue()}</span>,
  }),
  helper.accessor((row) => row.location.region, {
    id: 'region',
    header: 'Region',
    cell: (info) => <span className="text-gray-600">{info.getValue()}</span>,
  }),
]
```

- [ ] **Step 2: Write `src/components/FacilityTable/FacilityDetail.tsx`**

```tsx
// src/components/FacilityTable/FacilityDetail.tsx
import type { Facility } from '@/types/facility'

export default function FacilityDetail({ facility }: { facility: Facility }) {
  return (
    <div className="p-4 bg-emerald-50 border-t border-emerald-100">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <p className="font-semibold text-gray-800 mb-1">Capacity</p>
          <p className="text-gray-600">{facility.capacity || '—'}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Scale</p>
          <p className="text-gray-600">{facility.scale.join(' · ')}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Products</p>
          <p className="text-gray-600">{facility.products.join(', ') || '—'}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Known clients</p>
          <p className="text-gray-600">{facility.clients.length ? facility.clients.join(', ') : 'Confidential'}</p>
        </div>
        <div className="md:col-span-2">
          <p className="font-semibold text-gray-800 mb-1">Legacy</p>
          <p className="text-gray-600">{facility.legacy}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Certifications</p>
          <p className="text-gray-600">{facility.certifications.join(' · ') || '—'}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Notes</p>
          <p className="text-gray-600">{facility.notes || '—'}</p>
        </div>
        {facility.website && (
          <div>
            <a href={facility.website} target="_blank" rel="noopener noreferrer"
              className="text-emerald-700 hover:underline text-sm">
              Visit website →
            </a>
          </div>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Write `src/components/FacilityTable/FacilityTable.tsx`**

```tsx
// src/components/FacilityTable/FacilityTable.tsx
'use client'
import {
  useReactTable, getCoreRowModel, getSortedRowModel,
  flexRender, type SortingState,
} from '@tanstack/react-table'
import { useState } from 'react'
import { columns } from './columns'
import FacilityDetail from './FacilityDetail'
import type { Facility } from '@/types/facility'

interface FacilityTableProps {
  filtered: Facility[]
  selectedId: string | null
  setSelectedId: (id: string | null) => void
}

export default function FacilityTable({ filtered, selectedId, setSelectedId }: FacilityTableProps) {
  const [sorting, setSorting] = useState<SortingState>([])

  const table = useReactTable({
    data: filtered,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getRowId: (row) => row.id,
  })

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead className="bg-gray-100 sticky top-0 z-10">
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wide cursor-pointer select-none hover:bg-gray-200"
                  onClick={header.column.getToggleSortingHandler()}
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                  {header.column.getIsSorted() === 'asc' ? ' ↑' : header.column.getIsSorted() === 'desc' ? ' ↓' : ''}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => {
            const isSelected = row.id === selectedId
            const facility = row.original
            return (
              <>
                <tr
                  key={row.id}
                  onClick={() => setSelectedId(isSelected ? null : row.id)}
                  className={`border-b border-gray-100 cursor-pointer transition-colors
                    ${isSelected ? 'bg-emerald-50' : 'hover:bg-gray-50'}`}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-4 py-3">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
                {isSelected && (
                  <tr key={`${row.id}-detail`}>
                    <td colSpan={columns.length}>
                      <FacilityDetail facility={facility} />
                    </td>
                  </tr>
                )}
              </>
            )
          })}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="px-4 py-8 text-center text-gray-400">
                No facilities match the current filters.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
```

- [ ] **Step 4: TypeScript check**

```bash
npx tsc --noEmit
```
Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add src/components/FacilityTable/
git commit -m "feat: add sortable FacilityTable with expandable detail rows"
```

---

## Task 6: Facility Map

**Files:**
- Create: `src/components/FacilityMap/Map.tsx`
- Create: `src/components/FacilityMap/index.tsx`

**Interfaces:**
- Consumes: `filtered: Facility[]`, `selectedId: string | null`, `setSelectedId: (id: string | null) => void`
- Produces: `<FacilityMap filtered={…} selectedId={…} setSelectedId={…} />` — dynamic-imported, no SSR

- [ ] **Step 1: Write `src/components/FacilityMap/Map.tsx`**

```tsx
// src/components/FacilityMap/Map.tsx
'use client'
import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet.markercluster'
import type { Facility } from '@/types/facility'

interface MapProps {
  filtered: Facility[]
  selectedId: string | null
  setSelectedId: (id: string | null) => void
}

function makeIcon(selected: boolean) {
  return L.divIcon({
    className: '',
    html: `<div style="
      width:14px;height:14px;border-radius:50%;
      background:${selected ? '#059669' : '#10b981'};
      border:2px solid ${selected ? '#065f46' : '#fff'};
      box-shadow:0 1px 4px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  })
}

export default function Map({ filtered, selectedId, setSelectedId }: MapProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const clusterRef = useRef<L.MarkerClusterGroup | null>(null)
  const markersRef = useRef<Map<string, L.Marker>>(new Map())

  // Initialise map once
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return
    const map = L.map(containerRef.current, { center: [30, 10], zoom: 2 })
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map)
    const cluster = (L as any).markerClusterGroup({ maxClusterRadius: 40 })
    map.addLayer(cluster)
    mapRef.current = map
    clusterRef.current = cluster
    return () => { map.remove(); mapRef.current = null }
  }, [])

  // Rebuild markers when filtered list changes
  useEffect(() => {
    const cluster = clusterRef.current
    if (!cluster) return
    cluster.clearLayers()
    markersRef.current.clear()
    filtered.forEach((f) => {
      const marker = L.marker([f.location.lat, f.location.lng], {
        icon: makeIcon(f.id === selectedId),
      })
      marker.bindPopup(`
        <div style="min-width:160px">
          <strong style="font-size:13px">${f.name}</strong><br/>
          <span style="color:#555;font-size:12px">${f.owner}</span><br/>
          <span style="color:#888;font-size:11px">${f.location.city}, ${f.location.country}</span><br/>
          <span style="font-size:11px;color:#059669">${f.facilityType} · ${f.modalities[0]}</span>
        </div>
      `)
      marker.on('click', () => setSelectedId(f.id === selectedId ? null : f.id))
      cluster.addLayer(marker)
      markersRef.current.set(f.id, marker)
    })
  }, [filtered, selectedId, setSelectedId])

  // Update icon when selectedId changes without rebuilding
  useEffect(() => {
    markersRef.current.forEach((marker, id) => {
      marker.setIcon(makeIcon(id === selectedId))
    })
  }, [selectedId])

  return <div ref={containerRef} className="w-full h-full" />
}
```

- [ ] **Step 2: Write `src/components/FacilityMap/index.tsx`**

```tsx
// src/components/FacilityMap/index.tsx
import dynamic from 'next/dynamic'
import type { Facility } from '@/types/facility'

interface FacilityMapProps {
  filtered: Facility[]
  selectedId: string | null
  setSelectedId: (id: string | null) => void
}

const FacilityMap = dynamic<FacilityMapProps>(
  () => import('./Map'),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full flex items-center justify-center bg-gray-100">
        <span className="text-gray-400 text-sm">Loading map…</span>
      </div>
    ),
  }
)

export default FacilityMap
```

- [ ] **Step 3: TypeScript check**

```bash
npx tsc --noEmit
```
Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add src/components/FacilityMap/
git commit -m "feat: add Leaflet map with marker clustering and facility popups"
```

---

## Task 7: Main Page — Wire Everything Together

**Files:**
- Modify: `src/app/page.tsx`
- Modify: `src/app/globals.css` (ensure Leaflet map height works)

**Interfaces:**
- Consumes: `useFacilityFilters`, `FilterBar`, `FacilityTable`, `FacilityMap`
- Produces: full working page at `http://localhost:3000`

- [ ] **Step 1: Rewrite `src/app/page.tsx`**

```tsx
// src/app/page.tsx
'use client'
import { useFacilityFilters } from '@/hooks/useFacilityFilters'
import FilterBar from '@/components/FilterBar'
import FacilityTable from '@/components/FacilityTable/FacilityTable'
import FacilityMap from '@/components/FacilityMap'

export default function Home() {
  const filters = useFacilityFilters()

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-4 shrink-0">
        <div>
          <h1 className="text-lg font-bold text-gray-900">Biomanufacturing Facility Map</h1>
          <p className="text-xs text-gray-500">Global CMO &amp; CDMO intelligence platform</p>
        </div>
      </header>

      {/* Filter bar */}
      <FilterBar
        facilities={filters.facilities}
        globalSearch={filters.globalSearch}
        setGlobalSearch={filters.setGlobalSearch}
        modality={filters.modality}
        setModality={filters.setModality}
        region={filters.region}
        setRegion={filters.setRegion}
        facilityType={filters.facilityType}
        setFacilityType={filters.setFacilityType}
        resultCount={filters.filtered.length}
      />

      {/* Split view: map top, table bottom */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Map */}
        <div className="h-[40vh] shrink-0 border-b border-gray-200">
          <FacilityMap
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
          />
        </div>

        {/* Table */}
        <div className="flex-1 overflow-auto">
          <FacilityTable
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
          />
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Verify the full app in browser**

```bash
npm run dev
```

Open `http://localhost:3000`. Verify:
- Header renders
- FilterBar shows search input + 3 dropdowns + "20 facilities"
- Map renders with markers on correct locations
- Table shows 20 rows with correct data
- Clicking a table row expands the detail panel
- Clicking the same row collapses it
- Clicking a map marker highlights that row in the table (scroll to it if needed)
- Typing in the search box filters both table rows and map markers simultaneously
- Changing a dropdown filter updates both table and map

- [ ] **Step 3: Commit**

```bash
git add src/app/page.tsx src/app/globals.css
git commit -m "feat: wire FilterBar + FacilityTable + FacilityMap into main page with shared filter state"
```

---

## Task 8: Deploy to Vercel

**Files:**
- Create: `.env.local.example` (placeholder, no secrets needed for MVP)
- Create: `vercel.json` (optional — defaults work for Next.js)

**Interfaces:**
- Produces: public URL at `*.vercel.app`

- [ ] **Step 1: Push to GitHub**

```bash
gh repo create biomanufacturing-platform --public --source=. --push
```
Or manually: create repo on GitHub, then `git remote add origin <url> && git push -u origin main`.

- [ ] **Step 2: Deploy via Vercel CLI**

```bash
npx vercel --yes
```
Follow prompts: link to your account, accept auto-detected Next.js settings. No environment variables needed.

- [ ] **Step 3: Verify production deployment**

Open the Vercel URL. Confirm:
- Map loads on production (OpenStreetMap tiles load over HTTPS)
- Filtering works
- No console errors

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "chore: add deployment config and env example"
git push
```
