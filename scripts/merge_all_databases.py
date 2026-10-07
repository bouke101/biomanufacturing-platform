"""
Merge four source files into one consolidated Excel database:
  1. Pilots4U_database_1.xlsx   — 139 European pilot facilities
  2. NorthAmerica_biomanufacturing_database.xlsx — 76 North American facilities
  3. facilities.json            — 20 manual global CDMOs (non-Pilots4U)
  4. NorthAmerica_database_1.xlsx — agent-generated NA list (unique entries only)

Output: data/Global_biomanufacturing_database.xlsx
"""
import json
import re
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

# ── Helpers ──────────────────────────────────────────────────────────────────

def normalize(name: str) -> str:
    """Lowercase, strip closed/acquired suffixes, collapse whitespace."""
    s = str(name).lower()
    for pat in [r"\s*[–—-]+\s*closed(/acquired)?", r"\s*\(closed(/acquired)?\)"]:
        s = re.sub(pat, "", s, flags=re.I)
    # Remove trailing punctuation and whitespace
    s = re.sub(r"[,./]+$", "", s).strip()
    return re.sub(r"\s+", " ", s)


def row_score(row: dict) -> int:
    """Higher score = more fields filled."""
    return sum(1 for v in row.values() if v not in (None, "", 0))


def read_excel_rows(path: Path) -> list[dict]:
    """Read an Excel Facilities sheet into list-of-dicts using COLUMNS keys."""
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Facilities"]
    header = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    rows = []
    for excel_row in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(header, excel_row))
        # Normalise to canonical COLUMNS keys (handles any extra/missing cols)
        row = {col: d.get(col, "") or "" for col in COLUMNS}
        # Ensure numeric n_technologies
        try:
            row["No. of technologies"] = int(row["No. of technologies"]) if row["No. of technologies"] else ""
        except (ValueError, TypeError):
            row["No. of technologies"] = ""
        rows.append(row)
    return rows


def json_manual_to_rows(json_path: Path) -> list[dict]:
    """Map facilities.json manual (non-Pilots4U) entries to COLUMNS dicts."""
    with open(json_path) as f:
        facs = json.load(f)
    rows = []
    counter = 9001  # ID range for JSON-sourced entries
    for fac in facs:
        if fac.get("source") == "pilots4u":
            continue  # already in Pilots4U Excel
        ft = fac.get("facilityType", "")
        if ft in ("CMO", "CDMO"):
            tier = "Open CMO"
        elif ft == "Captive":
            tier = "Captive"
        else:
            tier = ft

        mods = fac.get("modalities", [])
        certs = fac.get("certifications", [])
        if isinstance(certs, list):
            cert_str = "\n".join(certs)
        else:
            cert_str = str(certs)

        about_parts = [p for p in [fac.get("notes", ""), fac.get("legacy", "")] if p]
        about = " ".join(about_parts)

        loc = fac.get("location", {})
        extra = f"Owner: {fac['owner']}" if fac.get("owner") else ""
        if fac.get("capacity"):
            extra = (extra + f". Capacity: {fac['capacity']}").lstrip(". ")

        rows.append({
            "ID": counter,
            "Facility": fac.get("name", ""),
            "Membership tier": tier,
            "City": loc.get("city", ""),
            "Country": loc.get("country", ""),
            "Address": "",
            "Contact person": "",
            "Website": fac.get("website", ""),
            "Social links": "",
            "About": about,
            "Technology areas": "\n".join(mods),
            "Technologies": "",
            "No. of technologies": len(mods) if mods else "",
            "Certifications": cert_str,
            "Non-technical services": "",
            "Open 24/7": "",
            "Extra information": extra,
            "Downloads": "",
            "Videos": "",
            "Logo": "",
            "Pilots4U page": "",
        })
        counter += 1
    return rows


# ── Load sources in priority order ───────────────────────────────────────────

print("Loading Pilots4U …")
p4u_rows = read_excel_rows(DATA_DIR / "Pilots4U_database_1.xlsx")
print(f"  {len(p4u_rows)} rows")

print("Loading NA biomanufacturing database …")
na_rows = read_excel_rows(DATA_DIR / "NorthAmerica_biomanufacturing_database.xlsx")
print(f"  {len(na_rows)} rows")

print("Loading facilities.json manual entries …")
json_rows = json_manual_to_rows(DATA_DIR / "facilities.json")
print(f"  {len(json_rows)} manual entries from JSON")

print("Loading agent NA database …")
agent_rows = read_excel_rows(DATA_DIR / "NorthAmerica_database_1.xlsx")
print(f"  {len(agent_rows)} rows")

# ── Deduplicate ───────────────────────────────────────────────────────────────
# Priority: Pilots4U > NA biomanufacturing > JSON manual > agent NA
# Use normalized facility name as dedup key; keep higher-scoring row on conflict.

seen: dict[str, int] = {}   # norm_name → index in `merged`
merged: list[dict] = []

COUNTRY_ALIASES = {
    "USA": "United States",
    "US": "United States",
    "U.S.": "United States",
    "U.S.A.": "United States",
    "UK": "United Kingdom",
    "Great Britain": "United Kingdom",
    "S. Korea": "South Korea",
}

# Agent file ID ranges → facility type
def tier_from_agent_id(orig_id_str: str) -> str:
    try:
        oid = int(orig_id_str)
    except (ValueError, TypeError):
        return ""
    if 1000 <= oid < 2000:
        return "Open CMO"
    if 2000 <= oid < 3000:
        return "Captive"
    if 3000 <= oid < 4000:
        return "Captive"  # Canadian sites and vaccine hubs
    if 4000 <= oid < 5000:
        return "Pilot facility"  # industrial biotech
    if 5000 <= oid < 6000:
        return "Pilot facility"  # academic
    if oid >= 6000:
        return "Closed"
    return ""


def add_rows(source_rows: list[dict], source_name: str, default_tier: str = ""):
    added = 0
    skipped = 0
    for row in source_rows:
        key = normalize(str(row.get("Facility", "")))
        if not key:
            continue

        # Normalise country
        country = str(row.get("Country", "") or "")
        row["Country"] = COUNTRY_ALIASES.get(country, country)

        # Fill blank tier
        tier = str(row.get("Membership tier", "") or "")
        if not tier:
            if default_tier:
                row["Membership tier"] = default_tier
            # For agent rows the orig ID is still in the row before renumbering
            elif source_name == "Agent NA":
                orig_id = str(row.get("ID", "") or "")
                inferred = tier_from_agent_id(orig_id)
                if inferred:
                    row["Membership tier"] = inferred

        if key in seen:
            existing_idx = seen[key]
            if row_score(row) > row_score(merged[existing_idx]):
                merged[existing_idx] = row
            skipped += 1
        else:
            seen[key] = len(merged)
            merged.append(row)
            added += 1
    print(f"  {source_name}: +{added} new, {skipped} deduplicated")

add_rows(p4u_rows,   "Pilots4U",          default_tier="Pilot facility")
add_rows(na_rows,    "NA biomanufacturing")
add_rows(json_rows,  "JSON manual")
add_rows(agent_rows, "Agent NA")

print(f"\nTotal unique facilities: {len(merged)}")

# ── Renumber IDs sequentially while keeping original in Extra information ────
for i, row in enumerate(merged, start=1):
    orig_id = row.get("ID", "")
    row["ID"] = i
    # Preserve original source ID in extra_info
    if orig_id and str(orig_id) != str(i):
        extra = str(row.get("Extra information", "") or "")
        tag = f"Source ID: {orig_id}"
        if tag not in extra:
            row["Extra information"] = (extra + f" | {tag}").lstrip(" |")

# ── Write Excel ───────────────────────────────────────────────────────────────

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "All Facilities"

header_fill  = PatternFill(start_color="1B4332", end_color="1B4332", fill_type="solid")
header_font  = Font(color="FFFFFF", bold=True)
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin_border  = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)
alt_fill = PatternFill(start_color="F0FAF5", end_color="F0FAF5", fill_type="solid")

# Tier → fill colour
TIER_FILLS = {
    "Basic member":    PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid"),
    "Advanced member": PatternFill(start_color="C8E6C9", end_color="C8E6C9", fill_type="solid"),
    "Premium member":  PatternFill(start_color="A5D6A7", end_color="A5D6A7", fill_type="solid"),
    "Open CMO":        PatternFill(start_color="E3F2FD", end_color="E3F2FD", fill_type="solid"),
    "Captive":         PatternFill(start_color="FFF8E1", end_color="FFF8E1", fill_type="solid"),
    "Pilot facility":  PatternFill(start_color="F3E5F5", end_color="F3E5F5", fill_type="solid"),
    "Closed":          PatternFill(start_color="FAFAFA", end_color="FAFAFA", fill_type="solid"),
}

# Header row
for col_idx, col_name in enumerate(COLUMNS, start=1):
    cell = ws.cell(row=1, column=col_idx, value=col_name)
    cell.fill      = header_fill
    cell.font      = header_font
    cell.alignment = header_align
    cell.border    = thin_border
ws.row_dimensions[1].height = 30

for row_idx, row_data in enumerate(merged, start=2):
    tier = str(row_data.get("Membership tier", "") or "")
    row_fill = TIER_FILLS.get(tier, (alt_fill if row_idx % 2 == 0 else PatternFill()))
    for col_idx, col_name in enumerate(COLUMNS, start=1):
        val = row_data.get(col_name, "")
        if val is None:
            val = ""
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.fill      = row_fill
        cell.border    = thin_border
        cell.alignment = Alignment(vertical="top", wrap_text=True, horizontal="left")

# Column widths
COL_WIDTHS = {
    "ID": 6, "Facility": 40, "Membership tier": 16,
    "City": 20, "Country": 14, "Address": 32,
    "Contact person": 20, "Website": 36, "Social links": 18,
    "About": 55, "Technology areas": 30, "Technologies": 40,
    "No. of technologies": 9, "Certifications": 26,
    "Non-technical services": 28, "Open 24/7": 9,
    "Extra information": 50, "Downloads": 10, "Videos": 10,
    "Logo": 28, "Pilots4U page": 18,
}
for col_idx, col_name in enumerate(COLUMNS, start=1):
    ws.column_dimensions[get_column_letter(col_idx)].width = COL_WIDTHS.get(col_name, 18)

ws.freeze_panes = "A2"

# ── Copy Technologies sheet from Pilots4U (has detailed fermentor data) ───────
src_wb = openpyxl.load_workbook(DATA_DIR / "Pilots4U_database_1.xlsx")
src_tech = src_wb["Technologies"]
ws_tech = wb.create_sheet("Technologies (Pilots4U)")
for row in src_tech.iter_rows(values_only=True):
    ws_tech.append(list(row))

# ── Summary / Notes sheet ─────────────────────────────────────────────────────
ws_notes = wb.create_sheet("Notes")
ws_notes["A1"] = "Global Biomanufacturing Facility Database"
ws_notes["A1"].font = Font(bold=True, size=14)
ws_notes["A3"] = f"Total unique facilities: {len(merged)}"

# Count by tier
from collections import Counter
tier_counts = Counter(r.get("Membership tier", "") or "Unknown" for r in merged)
row_n = 5
ws_notes.cell(row_n, 1, "Breakdown by type:").font = Font(bold=True)
row_n += 1
for tier, count in sorted(tier_counts.items()):
    ws_notes.cell(row_n, 1, f"  {tier}: {count}")
    row_n += 1

# Count by country (top 15)
country_counts = Counter(r.get("Country", "") or "Unknown" for r in merged)
row_n += 1
ws_notes.cell(row_n, 1, "Breakdown by country (top 15):").font = Font(bold=True)
row_n += 1
for country, count in country_counts.most_common(15):
    ws_notes.cell(row_n, 1, f"  {country}: {count}")
    row_n += 1

row_n += 1
ws_notes.cell(row_n, 1, "Sources:")
row_n += 1
sources = [
    f"  Pilots4U database — {len(p4u_rows)} European pilot facilities (biopilots4u.eu)",
    f"  North America biomanufacturing database — {len(na_rows)} manually compiled NA facilities",
    f"  facilities.json manual entries — {len(json_rows)} global CDMOs/captive sites",
    f"  Agent NA database — additional entries after deduplication",
]
for s in sources:
    ws_notes.cell(row_n, 1, s)
    row_n += 1

row_n += 1
ws_notes.cell(row_n, 1, "Row colour key:")
row_n += 1
colours = [
    ("Green shades (Basic/Advanced/Premium member)", "Pilots4U European pilot facilities"),
    ("Blue (Open CMO)", "Contract manufacturing organisations open to external clients"),
    ("Yellow (Captive)", "Company-owned internal manufacturing sites"),
    ("Purple (Pilot facility)", "Scale-up, R&D, and academic pilot manufacturing"),
    ("Grey (Closed)", "Decommissioned or legacy sites"),
]
for label, desc in colours:
    ws_notes.cell(row_n, 1, f"  {label}: {desc}")
    row_n += 1

ws_notes.column_dimensions["A"].width = 80
ws_notes["A1"].font = Font(bold=True, size=14)

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = DATA_DIR / "Global_biomanufacturing_database.xlsx"
wb.save(out_path)
print(f"\nSaved → {out_path}")
