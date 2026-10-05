# Biomanufacturing & CMO Facility Overview

## Project Goal

Build a web-based intelligence platform that gives users a comprehensive, searchable, and visual overview of biomanufacturing and Contract Manufacturing Organisation (CMO) facilities worldwide.

## Core Features

### 1. Facility Library (Table View)
A large, searchable data table that serves as the central database of all facilities. Each facility record includes:

- **Name** — facility / site name
- **Owner / Operator** — company name (CMO, CDMO, captive manufacturer, etc.)
- **Location** — city, country, region
- **Coordinates** — latitude / longitude (for map integration)
- **Facility Type** — CMO, CDMO, captive, toll manufacturer, etc.
- **Modalities** — fermentation, mammalian cell culture, microbial, viral vector, mRNA, etc.
- **Scale** — development, pilot, commercial (with capacity figures where available)
- **Clients & Products** — known clients, product categories, therapeutic areas or food/industrial applications
- **Legacy / History** — founding year, previous owners, major milestones
- **Helicopter-view image** — aerial or overview photograph of the facility
- **Additional notes** — certifications (GMP, FDA, EMA), notable capabilities, recent investments

The table must be:
- **Filterable and searchable** on every column
- **Sortable** by any field
- **Expandable** — clicking a row opens a detail panel with full facility information, image, and links

### 2. Interactive Map View
A geographic map that visualises all facilities as markers:

- Markers plotted from facility coordinates
- **Interactively linked to the table** — filtering the table updates the map markers in real time, and clicking a map marker highlights / filters the table row
- Marker clustering for dense regions
- Popup on marker click showing facility name, owner, modality, and a thumbnail image
- Filter controls on the map (by modality, region, facility type) that sync with the table

### 3. Additional Information (Future Phases)
Planned extensions once the core library and map are live:

- Capacity benchmarking charts (bioreactor volume by region, modality, etc.)
- Market news feed per facility (expansions, acquisitions, new partnerships)
- Client–CMO relationship network graph
- Export to CSV / PDF
- User-contributed data submissions with moderation

## Tech Stack (Proposed)

- **Frontend**: Next.js (React) — component-based, easy to deploy on Vercel
- **Table**: TanStack Table (React Table v8) — headless, fully customisable filtering and sorting
- **Map**: Mapbox GL JS or Leaflet with OpenStreetMap — interactive, marker clustering, popup support
- **Data**: Initially a static JSON / CSV file checked into the repo; later migrated to Supabase (PostgreSQL) for dynamic querying
- **Styling**: Tailwind CSS
- **Hosting**: Vercel

## Data Strategy

- Start with a curated seed dataset of ~50–100 well-known biomanufacturing and CMO/CDMO facilities
- Enrich over time with public sources: company websites, regulatory databases, industry reports
- Each facility stored as a structured JSON record keyed by a unique facility ID

## Folder Structure (Planned)

```
biomanufacturing/
├── CLAUDE.md               — this file
├── data/
│   └── facilities.json     — master facility dataset
├── src/
│   ├── app/                — Next.js app router pages
│   ├── components/
│   │   ├── FacilityTable/  — searchable / sortable table
│   │   ├── FacilityMap/    — interactive map component
│   │   └── FacilityDetail/ — expanded facility panel
│   └── lib/                — data loaders, types, utilities
├── public/
│   └── images/facilities/  — helicopter-view images
└── README.md
```

## Design Principles

- **Data first** — the facility library is the core asset; UI serves the data
- **Speed** — table and map must feel instant even with hundreds of records
- **Linked views** — table and map are always in sync; no disconnected UI states
- **Extensible** — data schema and components designed to accommodate new fields and feature phases without rewrites
