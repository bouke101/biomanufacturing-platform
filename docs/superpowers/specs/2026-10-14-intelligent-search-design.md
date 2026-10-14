# Intelligent Search Design

**Goal:** Add a natural-language "Ask" panel to the biomanufacturing platform that synthesises facility database knowledge and curated news into a written answer, and filters the facility table to matching results.

**Architecture:** A new `AskPanel` component sends queries to a `/api/ask` Next.js route. The route extracts keywords server-side, queries Supabase in parallel for matching facilities and news, then calls the Claude API (single call) to synthesise a written answer. The response includes the answer text and a list of matched facility IDs used to filter the existing table.

**Tech Stack:** Next.js 14 App Router, Supabase (PostgreSQL), Claude API (`claude-haiku-4-5-20251001`), React, Tailwind CSS.

---

## Global Constraints

- Framework: Next.js 14 App Router — server components, server actions, and API routes only; no Pages Router patterns.
- Styling: Tailwind CSS utility classes only — no new CSS files or inline `style` attributes.
- Database: Supabase (PostgreSQL). All schema changes via migration SQL files in `supabase/migrations/`.
- LLM: Claude API using model ID `claude-haiku-4-5-20251001`. API key from env var `ANTHROPIC_API_KEY`.
- The `Ask` feature is **separate** from the existing filter/search bar — it does not replace it.
- The facility table and map continue to work normally when Ask is idle or cleared.
- No external search APIs (Tavily, Brave, etc.) — only the Supabase database.
- TypeScript strict mode throughout. No `any` types.
- Existing tests must continue to pass.

---

## Data Model

### `news` table

```sql
CREATE TABLE news (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  date        date        NOT NULL,
  headline    text        NOT NULL,
  body        text        NOT NULL,
  product_tags  text[]    NOT NULL DEFAULT '{}',
  company_tags  text[]    NOT NULL DEFAULT '{}',
  event_type  text        NOT NULL DEFAULT 'other',
  source_url  text        NOT NULL DEFAULT '',
  created_at  timestamptz NOT NULL DEFAULT now()
);

-- event_type values: 'expansion' | 'closure' | 'acquisition' | 'incident' | 'partnership' | 'other'
```

RLS: readable by all authenticated users; insert/update/delete restricted to admin role (same pattern as other admin-only tables).

### Synonym map

A static TypeScript file `src/lib/synonyms.ts` exports a `Record<string, string[]>` mapping canonical product/company names to aliases. Example:

```ts
export const SYNONYMS: Record<string, string[]> = {
  "vitamin a": ["retinyl acetate", "retinyl palmitate", "retinol", "vitamin a"],
  "vitamin e": ["tocopherol", "tocopheryl acetate", "vitamin e"],
  "riboflavin": ["riboflavin", "vitamin b2"],
  "omega-3": ["epa", "dha", "omega-3", "fish oil", "omacor"],
}
```

This file is edited manually over time as gaps are discovered.

---

## Backend — `/api/ask`

**File:** `src/app/api/ask/route.ts`

**Request:** `POST` with JSON body `{ query: string }`.

**Response:** `{ answer: string; facilityIds: string[] }` on success, `{ error: string }` on failure.

### Flow

1. **Parse query** — trim and validate (non-empty, max 500 chars).

2. **Extract terms** — split query into lowercase tokens; expand each against `SYNONYMS`; produce a deduplicated `string[]` of candidate search terms.

3. **Fetch facilities** — `supabase.from('facilities').select('id, name, owner, products, capacity')` (all rows, no filter — 508 rows, negligible). Filter in JS: keep facilities where `products.some(p => terms.some(t => p.toLowerCase().includes(t)))` OR `name.toLowerCase()` includes any term OR `owner.toLowerCase()` includes any term.

4. **Fetch news** — Supabase query: rows where `product_tags && terms` OR `company_tags && terms`, ordered by `date DESC`, limit 20. Use a single `or` filter.

5. **Synthesise** — call Claude API with:
   - Model: `claude-haiku-4-5-20251001`
   - Max tokens: 800
   - System prompt (exact text):
     ```
     You are an analyst for a biomanufacturing intelligence platform.
     Answer the user's question in 2–4 concise paragraphs using only the
     facility and news context provided. Do not invent facts not present in
     the context. Structure: first paragraph covers which companies/facilities
     are involved and estimated market shares derived from the capacity figures;
     remaining paragraphs cover recent market developments from the news items.
     If capacity data is insufficient for market share, say so explicitly.
     If no relevant news items are provided, omit the developments section.
     ```
   - User message: the original query, followed by a serialised context block (see below).

6. **Return** `{ answer, facilityIds }` where `facilityIds` is the `id` array of matched facilities from step 3.

### Context serialisation

```
=== FACILITIES (${n} matched) ===
[For each facility:]
Name: {name}
Owner: {owner}
Products: {products.join(", ")}
Annual capacity: {capacity || "unknown"}

=== NEWS ITEMS (${m} recent) ===
[For each news item:]
Date: {date}
Headline: {headline}
Body: {body}
```

### Error handling

- Empty query or > 500 chars: return 400 `{ error: "Query must be 1–500 characters." }`.
- No facilities matched and no news matched: return 200 with `{ answer: "No facilities or news matching that query were found in the database.", facilityIds: [] }` — do not call Claude.
- Claude API error: return 500 `{ error: "Failed to generate answer." }`.

---

## Frontend

### `AskPanel` component

**File:** `src/components/AskPanel.tsx`

Client component. Three render states:

**Idle:**
```
[  Ask anything about the market…                    ] [Ask →]
```
A full-width text input (placeholder "Ask anything about the market…") and a submit button labelled "Ask →". Pressing Enter submits.

**Loading:**
Spinner or pulsing skeleton in place of the answer area. Input and button disabled.

**Answer:**
```
[  Show me where vitamin A is produced…              ] [Clear ×]

  [Answer text rendered as prose paragraphs]

  12 facilities matched  ↓ showing in table below
```
The answer text is plain text rendered in `<p>` tags, one per paragraph (split on `\n\n`). Bold (`**...**`) markdown is stripped and replaced with `<strong>`. No full markdown renderer — keep it simple.

A "Clear ×" button resets to idle and clears the table filter.

A small muted line below the answer: "{n} facilities matched — showing in table below."

### Integration with `FacilityPageClient`

**File:** `src/components/FacilityPageClient.tsx` — modify.

Add state: `const [askFilterIds, setAskFilterIds] = useState<string[] | null>(null)`.

Pass `setAskFilterIds` to `AskPanel`.

In the table/map filter logic: when `askFilterIds` is non-null, intersect it with the normal filter results (Ask narrows; it does not bypass other active filters). When null, behave exactly as today.

`AskPanel` sits between `Header` and `FilterBar` in the render tree.

### Placement in page layout

```
<Header />
<AskPanel onResult={(ids) => setAskFilterIds(ids)} onClear={() => setAskFilterIds(null)} />
<FilterBar … />
<FacilityTable … />   {/* filtered by askFilterIds when non-null */}
```

---

## Admin — News management

A new "News" tab in the existing admin panel (`src/app/admin/AdminClient.tsx`).

**File:** `src/components/admin/NewsTab.tsx`

Lists existing news items in a table: date, headline, event type, delete button.

A form above the list for adding new items:
- Date (date input)
- Headline (text input)
- Body (textarea)
- Product tags (comma-separated text input, split on save)
- Company tags (comma-separated text input, split on save)
- Event type (select: expansion / closure / acquisition / incident / partnership / other)
- Source URL (text input, optional)

On submit: `INSERT INTO news …`. On delete: `DELETE FROM news WHERE id = $id`. Both use the Supabase admin client (bypasses RLS).

No edit functionality for v1 — delete and re-add.

---

## Supabase migration

File: `supabase/migrations/20261014_add_news_table.sql`

Contents: the `CREATE TABLE news` DDL above plus RLS policies:
```sql
ALTER TABLE news ENABLE ROW LEVEL SECURITY;
CREATE POLICY "news_read_authenticated" ON news FOR SELECT TO authenticated USING (true);
CREATE POLICY "news_write_admin" ON news FOR ALL TO authenticated
  USING (EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'))
  WITH CHECK (EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'));
```

---

## Out of scope (v1)

- Live web search / external news APIs
- Vector/semantic search (pg_vector)
- Streaming the LLM response
- Saving query history
- Answer feedback / thumbs up-down
