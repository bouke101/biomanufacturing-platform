# Intelligent Search Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a natural-language "Ask" panel that synthesises facility + curated news data into a written answer and filters the facility table to matched results.

**Architecture:** Keyword expansion via a static synonym map pre-filters facilities (JS in-memory) and news (Supabase query). A single Claude API call (haiku model) synthesises a 2–4 paragraph answer. The `AskPanel` client component drives a `/api/ask` POST route and passes matched facility IDs back to `FacilityPageClient` to narrow the table/map.

**Tech Stack:** Next.js 14 App Router, Supabase (PostgreSQL), `@anthropic-ai/sdk`, React, Tailwind CSS.

**Spec:** `docs/superpowers/specs/2026-10-14-intelligent-search-design.md`

## Global Constraints

- Framework: Next.js 14 App Router — server components, server actions, and API routes only; no Pages Router patterns.
- Styling: Tailwind CSS utility classes only — no new CSS files or inline `style` attributes.
- Database: Supabase (PostgreSQL). All schema changes via migration SQL files in `supabase/migrations/`.
- LLM: Claude API using model ID `claude-haiku-4-5-20251001`. API key from env var `ANTHROPIC_API_KEY`.
- The `Ask` feature is **separate** from the existing filter/search bar — it does not replace it.
- No external search APIs — only the Supabase database.
- TypeScript strict mode throughout. No `any` types.
- Existing behaviour of table, map, and admin panel must be unchanged when Ask is idle.

---

## File Map

| File | Status | Purpose |
|---|---|---|
| `supabase/migrations/20261014000000_add_news_table.sql` | CREATE | `news` table DDL + RLS policies |
| `src/lib/synonyms.ts` | CREATE | `SYNONYMS` map + `expandTerms(query)` |
| `src/lib/news.ts` | CREATE | `NewsItem` type + `fetchAllNews()` |
| `src/app/api/ask/route.ts` | CREATE | POST handler: expand → query → synthesise |
| `src/components/AskPanel.tsx` | CREATE | Client component: idle / loading / answer states |
| `src/actions/news.ts` | CREATE | `createNewsItem` + `deleteNewsItem` server actions |
| `src/components/admin/NewsTab.tsx` | CREATE | Admin form + list for news CRUD |
| `src/components/FacilityPageClient.tsx` | MODIFY | Add `askFilterIds` state + render `AskPanel` |
| `src/app/admin/AdminClient.tsx` | MODIFY | Add "News" tab |
| `src/app/admin/page.tsx` | MODIFY | Fetch initial news + pass to `AdminClient` |

---

## Task 1: Database migration — `news` table

**Files:**
- Create: `supabase/migrations/20261014000000_add_news_table.sql`

**Interfaces:**
- Produces: `news` table in Supabase with columns `id`, `date`, `headline`, `body`, `product_tags`, `company_tags`, `event_type`, `source_url`, `created_at`. Used by Tasks 2, 3, 6.

- [ ] **Step 1: Create the migration file**

```sql
-- supabase/migrations/20261014000000_add_news_table.sql
CREATE TABLE IF NOT EXISTS news (
  id           uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  date         date        NOT NULL,
  headline     text        NOT NULL,
  body         text        NOT NULL,
  product_tags text[]      NOT NULL DEFAULT '{}',
  company_tags text[]      NOT NULL DEFAULT '{}',
  event_type   text        NOT NULL DEFAULT 'other',
  source_url   text        NOT NULL DEFAULT '',
  created_at   timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE news ENABLE ROW LEVEL SECURITY;

CREATE POLICY "news_read_authenticated"
  ON news FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "news_write_admin"
  ON news FOR ALL TO authenticated
  USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
  )
  WITH CHECK (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
  );
```

- [ ] **Step 2: Apply migration to Supabase**

Option A — Supabase CLI (if linked):
```bash
npx supabase db push
```

Option B — Supabase Dashboard:
Copy the SQL above and run it in the Supabase Dashboard → SQL Editor.

- [ ] **Step 3: Verify the table exists**

In the Supabase Dashboard → Table Editor, confirm `news` appears with the correct columns and RLS enabled. Or run in SQL Editor:
```sql
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'news' ORDER BY ordinal_position;
```
Expected: 9 rows (id, date, headline, body, product_tags, company_tags, event_type, source_url, created_at).

- [ ] **Step 4: Commit**

```bash
git add supabase/migrations/20261014000000_add_news_table.sql
git commit -m "feat: add news table migration with RLS"
```

---

## Task 2: Synonym map + `expandTerms` + `NewsItem` type

**Files:**
- Create: `src/lib/synonyms.ts`
- Create: `src/lib/news.ts`

**Interfaces:**
- Produces:
  - `expandTerms(query: string): string[]` — exported from `src/lib/synonyms.ts`
  - `NewsItem` interface — exported from `src/lib/news.ts`
  - `fetchAllNews(supabase: SupabaseClient): Promise<NewsItem[]>` — exported from `src/lib/news.ts`

- [ ] **Step 1: Create `src/lib/synonyms.ts`**

```typescript
// src/lib/synonyms.ts

export const SYNONYMS: Record<string, string[]> = {
  "vitamin a":   ["retinyl acetate", "retinyl palmitate", "retinol", "vitamin a"],
  "vitamin e":   ["tocopherol", "tocopheryl acetate", "alpha-tocopherol", "vitamin e"],
  "vitamin b2":  ["riboflavin", "vitamin b2"],
  "riboflavin":  ["riboflavin", "vitamin b2"],
  "omega-3":     ["epa", "dha", "omega-3", "fish oil", "omacor", "pronova"],
  "lysine":      ["l-lysine", "lysine"],
  "citric acid": ["citric acid", "citrate"],
  "lactic acid": ["lactic acid", "lactate", "pla", "polylactic acid"],
  "pbat":        ["pbat", "ecoflex", "polybutylene adipate"],
  "phytase":     ["phytase", "natuphos"],
  "astaxanthin": ["astaxanthin", "haematococcus"],
  "beta-carotene": ["beta-carotene", "carotene", "lucaropen"],
  "msg":         ["monosodium glutamate", "msg", "glutamate"],
  "threonine":   ["l-threonine", "threonine"],
  "tryptophan":  ["l-tryptophan", "tryptophan"],
  "methionine":  ["dl-methionine", "methionine"],
  "basf":        ["basf"],
  "dsm-firmenich": ["dsm-firmenich", "dsm firmenich", "dsm", "firmenich"],
  "novonesis":   ["novonesis", "novozymes"],
  "iff":         ["iff", "international flavors"],
  "evonik":      ["evonik"],
  "adm":         ["adm", "archer daniels midland"],
  "cargill":     ["cargill"],
  "corbion":     ["corbion"],
}

const STOP_WORDS = new Set([
  "the","a","an","and","or","but","in","on","at","to","for","of","with",
  "by","from","is","are","was","were","be","been","have","has","do","does",
  "did","will","would","could","should","may","might","can","me","my","we",
  "our","you","your","they","their","what","where","when","how","who","which",
  "show","tell","find","list","give","each","produced","producing","makes",
  "made","manufacture","manufactured","produces","market","share","company",
  "companies","facility","facilities","plant","plants","site","sites",
])

export function expandTerms(query: string): string[] {
  const lower = query.toLowerCase()
  const terms = new Set<string>()

  // Add individual non-stop-word tokens from the query
  lower.split(/[\s,;.?!]+/).forEach((token) => {
    const clean = token.replace(/[^a-z0-9-]/g, "")
    if (clean.length > 1 && !STOP_WORDS.has(clean)) {
      terms.add(clean)
    }
  })

  // Expand known multi-word keys and their aliases
  for (const [key, aliases] of Object.entries(SYNONYMS)) {
    if (lower.includes(key)) {
      aliases.forEach((a) => terms.add(a))
    }
  }

  return [...terms]
}
```

- [ ] **Step 2: Create `src/lib/news.ts`**

```typescript
// src/lib/news.ts
import type { SupabaseClient } from "@supabase/supabase-js"

export interface NewsItem {
  id: string
  date: string          // ISO date string e.g. "2026-03-15"
  headline: string
  body: string
  product_tags: string[]
  company_tags: string[]
  event_type: string
  source_url: string
  created_at: string
}

export async function fetchAllNews(supabase: SupabaseClient): Promise<NewsItem[]> {
  const { data, error } = await supabase
    .from("news")
    .select("*")
    .order("date", { ascending: false })
  if (error) throw new Error(error.message)
  return (data ?? []) as NewsItem[]
}
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
npx tsc --noEmit
```
Expected: zero errors related to the new files.

- [ ] **Step 4: Commit**

```bash
git add src/lib/synonyms.ts src/lib/news.ts
git commit -m "feat: add synonym map, expandTerms, and NewsItem type"
```

---

## Task 3: Install Anthropic SDK + `/api/ask` route

**Files:**
- Modify: `package.json` (via npm install)
- Create: `src/app/api/ask/route.ts`

**Interfaces:**
- Consumes:
  - `expandTerms(query: string): string[]` from `src/lib/synonyms.ts`
  - `fetchAllNews(supabase: SupabaseClient): Promise<NewsItem[]>` from `src/lib/news.ts`
  - `Facility` type from `src/types/facility.ts`
- Produces: `POST /api/ask` → `{ answer: string; facilityIds: string[] }` or `{ error: string }`

- [ ] **Step 1: Install the Anthropic SDK**

```bash
npm install @anthropic-ai/sdk
```

- [ ] **Step 2: Add `ANTHROPIC_API_KEY` to `.env.local`**

Open `.env.local` and add:
```
ANTHROPIC_API_KEY=sk-ant-...
```
(Use your actual key from console.anthropic.com.)

- [ ] **Step 3: Create `src/app/api/ask/route.ts`**

```typescript
// src/app/api/ask/route.ts
import { NextRequest, NextResponse } from "next/server"
import Anthropic from "@anthropic-ai/sdk"
import { createSupabaseAdminClient } from "@/lib/supabase/admin"
import { expandTerms } from "@/lib/synonyms"
import { fetchAllNews } from "@/lib/news"
import type { NewsItem } from "@/lib/news"

const SYSTEM_PROMPT = `You are an analyst for a biomanufacturing intelligence platform.
Answer the user's question in 2–4 concise paragraphs using only the
facility and news context provided. Do not invent facts not present in
the context. Structure: first paragraph covers which companies/facilities
are involved and estimated market shares derived from the capacity figures;
remaining paragraphs cover recent market developments from the news items.
If capacity data is insufficient for market share, say so explicitly.
If no relevant news items are provided, omit the developments section.`

function buildContext(
  facilities: { name: string; owner: string; products: string[]; capacity: string }[],
  news: NewsItem[]
): string {
  const facilityBlock = facilities
    .map(
      (f) =>
        `Name: ${f.name}\nOwner: ${f.owner}\nProducts: ${f.products.join(", ")}\nAnnual capacity: ${f.capacity || "unknown"}`
    )
    .join("\n\n")

  const newsBlock = news
    .map((n) => `Date: ${n.date}\nHeadline: ${n.headline}\nBody: ${n.body}`)
    .join("\n\n")

  return (
    `=== FACILITIES (${facilities.length} matched) ===\n\n${facilityBlock}` +
    (news.length > 0
      ? `\n\n=== NEWS ITEMS (${news.length} recent) ===\n\n${newsBlock}`
      : "")
  )
}

export async function POST(req: NextRequest) {
  let query: string
  try {
    const body = (await req.json()) as { query?: unknown }
    query = typeof body.query === "string" ? body.query.trim() : ""
  } catch {
    return NextResponse.json({ error: "Invalid request body." }, { status: 400 })
  }

  if (!query || query.length > 500) {
    return NextResponse.json(
      { error: "Query must be 1–500 characters." },
      { status: 400 }
    )
  }

  const terms = expandTerms(query)
  const supabase = createSupabaseAdminClient()

  // Fetch facilities (lightweight columns only) and all news in parallel
  const [facilitiesResult, allNews] = await Promise.all([
    supabase
      .from("facilities")
      .select("id, name, owner, products, capacity"),
    fetchAllNews(supabase),
  ])

  if (facilitiesResult.error) {
    return NextResponse.json({ error: "Failed to query facilities." }, { status: 500 })
  }

  type FacilityRow = {
    id: string
    name: string
    owner: string
    products: string[]
    capacity: string
  }

  const allFacilities = (facilitiesResult.data ?? []) as FacilityRow[]

  // Filter facilities: match on products, name, or owner
  const matchedFacilities = allFacilities.filter((f) =>
    f.products.some((p) =>
      terms.some((t) => p.toLowerCase().includes(t))
    ) ||
    terms.some((t) => f.name.toLowerCase().includes(t)) ||
    terms.some((t) => f.owner.toLowerCase().includes(t))
  )

  // Filter news: match on product_tags or company_tags
  const matchedNews = allNews
    .filter((n) =>
      n.product_tags.some((tag) => terms.some((t) => tag.includes(t) || t.includes(tag))) ||
      n.company_tags.some((tag) => terms.some((t) => tag.includes(t) || t.includes(tag)))
    )
    .slice(0, 20)

  // No matches — skip Claude call
  if (matchedFacilities.length === 0 && matchedNews.length === 0) {
    return NextResponse.json({
      answer: "No facilities or news matching that query were found in the database.",
      facilityIds: [],
    })
  }

  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

  try {
    const message = await client.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 800,
      system: SYSTEM_PROMPT,
      messages: [
        {
          role: "user",
          content: `${query}\n\n${buildContext(matchedFacilities, matchedNews)}`,
        },
      ],
    })

    const block = message.content[0]
    const answer = block.type === "text" ? block.text : ""

    return NextResponse.json({
      answer,
      facilityIds: matchedFacilities.map((f) => f.id),
    })
  } catch {
    return NextResponse.json(
      { error: "Failed to generate answer." },
      { status: 500 }
    )
  }
}
```

- [ ] **Step 4: Verify TypeScript compiles**

```bash
npx tsc --noEmit
```
Expected: zero new errors.

- [ ] **Step 5: Smoke-test with curl**

Start the dev server in a separate terminal: `npm run dev`

Then run:
```bash
curl -s -X POST http://localhost:3000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me where vitamin A is produced"}' | jq .
```
Expected: `{ "answer": "...", "facilityIds": ["...", ...] }` with non-empty arrays.

Test validation:
```bash
curl -s -X POST http://localhost:3000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query": ""}' | jq .
```
Expected: `{ "error": "Query must be 1–500 characters." }` with HTTP 400.

- [ ] **Step 6: Commit**

```bash
git add src/app/api/ask/route.ts package.json package-lock.json
git commit -m "feat: add /api/ask route with Claude synthesis"
```

---

## Task 4: `AskPanel` component

**Files:**
- Create: `src/components/AskPanel.tsx`

**Interfaces:**
- Consumes: `POST /api/ask` → `{ answer: string; facilityIds: string[] }` or `{ error: string }`
- Produces: exported default `AskPanel` component with props:
  ```typescript
  interface AskPanelProps {
    onResult: (facilityIds: string[]) => void
    onClear: () => void
  }
  ```

- [ ] **Step 1: Create `src/components/AskPanel.tsx`**

```typescript
// src/components/AskPanel.tsx
"use client"
import { useState, useRef } from "react"

interface AskPanelProps {
  onResult: (facilityIds: string[]) => void
  onClear: () => void
}

type PanelState = "idle" | "loading" | "answer"

interface AnswerData {
  text: string
  count: number
}

function renderParagraph(text: string): React.ReactNode[] {
  // Replace **bold** with <strong>
  const parts = text.split(/\*\*([^*]+)\*\*/g)
  return parts.map((part, i) =>
    i % 2 === 1 ? <strong key={i}>{part}</strong> : part
  )
}

export default function AskPanel({ onResult, onClear }: AskPanelProps) {
  const [state, setState] = useState<PanelState>("idle")
  const [query, setQuery] = useState("")
  const [answer, setAnswer] = useState<AnswerData | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  async function handleSubmit() {
    const trimmed = query.trim()
    if (!trimmed || state === "loading") return
    setState("loading")
    setErrorMsg(null)

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: trimmed }),
      })
      const data = (await res.json()) as
        | { answer: string; facilityIds: string[] }
        | { error: string }

      if ("error" in data) {
        setErrorMsg(data.error)
        setState("idle")
        return
      }

      setAnswer({ text: data.answer, count: data.facilityIds.length })
      onResult(data.facilityIds)
      setState("answer")
    } catch {
      setErrorMsg("Something went wrong. Please try again.")
      setState("idle")
    }
  }

  function handleClear() {
    setState("idle")
    setAnswer(null)
    setErrorMsg(null)
    setQuery("")
    onClear()
    inputRef.current?.focus()
  }

  const isLoading = state === "loading"
  const hasAnswer = state === "answer"

  return (
    <div className="bg-white border-b border-gray-200 px-4 py-4">
      {/* Input row */}
      <div className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") handleSubmit() }}
          disabled={isLoading}
          placeholder="Ask anything about the market…"
          className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:bg-gray-50 disabled:text-gray-400"
        />
        {hasAnswer ? (
          <button
            onClick={handleClear}
            className="px-4 py-2 text-sm font-medium bg-gray-100 text-gray-600 rounded-md hover:bg-gray-200 transition-colors whitespace-nowrap"
          >
            Clear ×
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={isLoading || !query.trim()}
            className="px-4 py-2 text-sm font-medium bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {isLoading ? "Thinking…" : "Ask →"}
          </button>
        )}
      </div>

      {/* Error */}
      {errorMsg && (
        <p className="mt-2 text-sm text-red-600">{errorMsg}</p>
      )}

      {/* Loading skeleton */}
      {isLoading && (
        <div className="mt-4 space-y-2 animate-pulse">
          <div className="h-3 bg-gray-200 rounded w-full" />
          <div className="h-3 bg-gray-200 rounded w-5/6" />
          <div className="h-3 bg-gray-200 rounded w-4/6" />
        </div>
      )}

      {/* Answer */}
      {hasAnswer && answer && (
        <div className="mt-4">
          <div className="prose-sm text-gray-700 space-y-3">
            {answer.text.split("\n\n").filter(Boolean).map((para, i) => (
              <p key={i}>{renderParagraph(para)}</p>
            ))}
          </div>
          <p className="mt-3 text-xs text-gray-400">
            {answer.count} {answer.count === 1 ? "facility" : "facilities"} matched — showing in table below
          </p>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Verify TypeScript compiles**

```bash
npx tsc --noEmit
```
Expected: zero new errors.

- [ ] **Step 3: Commit**

```bash
git add src/components/AskPanel.tsx
git commit -m "feat: add AskPanel component (idle/loading/answer states)"
```

---

## Task 5: Wire `AskPanel` into `FacilityPageClient`

**Files:**
- Modify: `src/components/FacilityPageClient.tsx`

**Interfaces:**
- Consumes:
  - `AskPanel` from `src/components/AskPanel.tsx` — props `onResult(ids: string[])` and `onClear()`
  - `useFacilityFilters` hook — `filters.filtered: Facility[]` already computed
- Produces: unchanged external interface (`FacilityPageClientProps`); internal `askFilterIds` state added.

- [ ] **Step 1: Replace `src/components/FacilityPageClient.tsx`**

Current file is 27 lines. Replace entirely with:

```typescript
// src/components/FacilityPageClient.tsx
"use client"
import { useState } from "react"
import { useFacilityFilters } from "@/hooks/useFacilityFilters"
import FilterBar from "@/components/FilterBar"
import FacilityTable from "@/components/FacilityTable/FacilityTable"
import FacilityMap from "@/components/FacilityMap"
import AskPanel from "@/components/AskPanel"
import type { Facility } from "@/types/facility"

interface FacilityPageClientProps {
  initialFacilities: Facility[]
  columnVisibility: Record<string, boolean>
}

export default function FacilityPageClient({
  initialFacilities,
  columnVisibility,
}: FacilityPageClientProps) {
  const filters = useFacilityFilters(initialFacilities)
  const [askFilterIds, setAskFilterIds] = useState<string[] | null>(null)

  // When Ask is active, intersect its matched IDs with the current filter state
  const displayed =
    askFilterIds !== null
      ? filters.filtered.filter((f) => askFilterIds.includes(f.id))
      : filters.filtered

  return (
    <>
      <AskPanel
        onResult={(ids) => setAskFilterIds(ids)}
        onClear={() => setAskFilterIds(null)}
      />
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
        resultCount={displayed.length}
      />
      <div className="flex flex-col flex-1 overflow-hidden">
        <div className="h-[40vh] shrink-0 border-b border-gray-200">
          <FacilityMap
            filtered={displayed}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
          />
        </div>
        <div className="flex-1 overflow-auto min-w-0">
          <FacilityTable
            filtered={displayed}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
            columnVisibility={columnVisibility}
          />
        </div>
      </div>
    </>
  )
}
```

- [ ] **Step 2: Verify TypeScript compiles**

```bash
npx tsc --noEmit
```
Expected: zero errors.

- [ ] **Step 3: Manual browser test**

Run `npm run dev`. Open `http://localhost:3000`.

Verify:
1. The Ask panel renders above the filter bar — a text input with "Ask anything about the market…" placeholder and an "Ask →" button.
2. Typing "vitamin A" and pressing Ask → shows a loading skeleton, then an answer paragraph and a count of matched facilities.
3. The table below narrows to the matched facilities.
4. "Clear ×" button resets the table to the full list and clears the answer.
5. The existing filter dropdowns and text search still work when Ask is idle.

- [ ] **Step 4: Commit**

```bash
git add src/components/FacilityPageClient.tsx
git commit -m "feat: integrate AskPanel into FacilityPageClient with askFilterIds state"
```

---

## Task 6: Admin news management — actions, `NewsTab`, `AdminClient`, admin page

**Files:**
- Create: `src/actions/news.ts`
- Create: `src/components/admin/NewsTab.tsx`
- Modify: `src/app/admin/AdminClient.tsx`
- Modify: `src/app/admin/page.tsx`

**Interfaces:**
- Consumes: `NewsItem` from `src/lib/news.ts`; `fetchAllNews` from `src/lib/news.ts`; `createSupabaseAdminClient` from `src/lib/supabase/admin`
- Produces:
  - `createNewsItem(data: NewsItemFormData): Promise<void>` server action
  - `deleteNewsItem(id: string): Promise<void>` server action
  - `NewsTab` component (props: `{ initialNews: NewsItem[] }`)
  - Updated `AdminClient` with a "News" tab (tab key `"news"`)
  - Updated admin page that fetches initial news and passes it to `AdminClient`

- [ ] **Step 1: Create `src/actions/news.ts`**

```typescript
// src/actions/news.ts
"use server"
import { createSupabaseAdminClient } from "@/lib/supabase/admin"
import { createSupabaseServerClient } from "@/lib/supabase/server"
import { redirect } from "next/navigation"

async function requireAdmin() {
  const supabase = createSupabaseServerClient()
  const {
    data: { user },
  } = await supabase.auth.getUser()
  if (!user) redirect("/login")
  const { data: profile } = await supabase
    .from("profiles")
    .select("role")
    .eq("id", user.id)
    .single()
  if (profile?.role !== "admin") redirect("/")
}

export interface NewsItemFormData {
  date: string        // "YYYY-MM-DD"
  headline: string
  body: string
  product_tags: string  // comma-separated; split server-side
  company_tags: string  // comma-separated; split server-side
  event_type: string
  source_url: string
}

function parseTags(raw: string): string[] {
  return raw
    .split(",")
    .map((t) => t.trim().toLowerCase())
    .filter((t) => t.length > 0)
}

export async function createNewsItem(data: NewsItemFormData): Promise<void> {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin.from("news").insert({
    date: data.date,
    headline: data.headline,
    body: data.body,
    product_tags: parseTags(data.product_tags),
    company_tags: parseTags(data.company_tags),
    event_type: data.event_type,
    source_url: data.source_url,
  })
  if (error) throw new Error(error.message)
}

export async function deleteNewsItem(id: string): Promise<void> {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin.from("news").delete().eq("id", id)
  if (error) throw new Error(error.message)
}
```

- [ ] **Step 2: Create `src/components/admin/NewsTab.tsx`**

```typescript
// src/components/admin/NewsTab.tsx
"use client"
import { useState, useTransition } from "react"
import { createNewsItem, deleteNewsItem } from "@/actions/news"
import type { NewsItem } from "@/lib/news"
import type { NewsItemFormData } from "@/actions/news"

const EVENT_TYPES = [
  "expansion", "closure", "acquisition", "incident", "partnership", "other",
] as const

const EMPTY_FORM: NewsItemFormData = {
  date: "",
  headline: "",
  body: "",
  product_tags: "",
  company_tags: "",
  event_type: "other",
  source_url: "",
}

export default function NewsTab({ initialNews }: { initialNews: NewsItem[] }) {
  const [items, setItems] = useState(initialNews)
  const [form, setForm] = useState<NewsItemFormData>(EMPTY_FORM)
  const [pending, startTransition] = useTransition()

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  function handleAdd(e: React.FormEvent) {
    e.preventDefault()
    startTransition(async () => {
      await createNewsItem(form)
      setForm(EMPTY_FORM)
      window.location.reload()
    })
  }

  function handleDelete(id: string) {
    if (!confirm("Delete this news item?")) return
    startTransition(async () => {
      await deleteNewsItem(id)
      setItems((prev) => prev.filter((n) => n.id !== id))
    })
  }

  return (
    <div>
      {/* Add form */}
      <form onSubmit={handleAdd} className="bg-white rounded-xl border border-gray-200 p-5 mb-6 space-y-4">
        <h3 className="text-sm font-semibold text-gray-800">Add news item</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Date</label>
            <input
              type="date"
              name="date"
              required
              value={form.date}
              onChange={handleChange}
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Event type</label>
            <select
              name="event_type"
              value={form.event_type}
              onChange={handleChange}
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
            >
              {EVENT_TYPES.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Headline</label>
          <input
            type="text"
            name="headline"
            required
            value={form.headline}
            onChange={handleChange}
            placeholder="BASF Ludwigshafen vitamin synthesis plant expands capacity"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Body</label>
          <textarea
            name="body"
            required
            rows={4}
            value={form.body}
            onChange={handleChange}
            placeholder="1–3 paragraph summary of the event…"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 resize-y"
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Product tags <span className="font-normal text-gray-400">(comma-separated, lowercase)</span>
            </label>
            <input
              type="text"
              name="product_tags"
              value={form.product_tags}
              onChange={handleChange}
              placeholder="vitamin a, retinol"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Company tags <span className="font-normal text-gray-400">(comma-separated, lowercase)</span>
            </label>
            <input
              type="text"
              name="company_tags"
              value={form.company_tags}
              onChange={handleChange}
              placeholder="basf, dsm-firmenich"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Source URL <span className="font-normal text-gray-400">(optional)</span>
          </label>
          <input
            type="url"
            name="source_url"
            value={form.source_url}
            onChange={handleChange}
            placeholder="https://…"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={pending}
            className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 transition-colors disabled:opacity-50"
          >
            {pending ? "Saving…" : "Add item"}
          </button>
        </div>
      </form>

      {/* News list */}
      <p className="text-sm text-gray-500 mb-3">{items.length} news items</p>
      {items.length === 0 ? (
        <p className="text-sm text-gray-400 italic">No news items yet. Add one above.</p>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Date</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Headline</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Type</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Tags</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} className="border-t border-gray-100">
                  <td className="px-4 py-3 text-gray-500 whitespace-nowrap">{item.date}</td>
                  <td className="px-4 py-3 text-gray-800 max-w-xs truncate">{item.headline}</td>
                  <td className="px-4 py-3">
                    <span className="inline-block px-2 py-0.5 text-xs rounded-full bg-blue-100 text-blue-700 font-medium">
                      {item.event_type}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 text-xs">
                    {[...item.product_tags, ...item.company_tags].join(", ") || "—"}
                  </td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleDelete(item.id)}
                      disabled={pending}
                      className="text-sm text-red-600 hover:underline disabled:opacity-50"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: Update `src/app/admin/AdminClient.tsx`**

Add the `"news"` tab. Change the `Tab` type union and add the button + render block. The diff is:

```typescript
// Change Tab type (line ~9):
type Tab = "users" | "columns" | "facilities" | "news"

// Add to AdminClientProps (after `facilities` prop):
initialNews: import("@/lib/news").NewsItem[]

// Add to AdminClient destructuring:
{ ..., initialNews }

// Add tab button after Facilities button:
<button className={tabClass("news")} onClick={() => setActiveTab("news")}>
  News
</button>

// Add render after facilities conditional:
{activeTab === "news" && <NewsTab initialNews={initialNews} />}

// Add import at top:
import NewsTab from "@/components/admin/NewsTab"
```

Full updated file:

```typescript
// src/app/admin/AdminClient.tsx
"use client"
import { useState } from "react"
import UsersTab from "@/components/admin/UsersTab"
import ColumnVisibilityTab from "@/components/admin/ColumnVisibilityTab"
import FacilitiesTab from "@/components/admin/FacilitiesTab"
import NewsTab from "@/components/admin/NewsTab"
import type { AllFilterValues } from "@/components/admin/ContentFiltersTab"
import type { ColumnFilters } from "@/lib/facilities"
import type { NewsItem } from "@/lib/news"

type Tab = "users" | "columns" | "facilities" | "news"

interface Profile {
  id: string
  email: string
  role: string
  blocked: boolean
  created_at: string
}

interface AdminClientProps {
  users: Profile[]
  columnVisibility: Record<string, boolean>
  columnFilters: ColumnFilters
  allFilterValues: AllFilterValues
  valueCounts: Record<string, Record<string, number>>
  totalFacilities: number
  facilities: import("@/types/facility").Facility[]
  initialNews: NewsItem[]
}

export default function AdminClient({
  users,
  columnVisibility,
  columnFilters,
  allFilterValues,
  valueCounts,
  totalFacilities,
  facilities,
  initialNews,
}: AdminClientProps) {
  const [activeTab, setActiveTab] = useState<Tab>("users")

  const tabClass = (tab: Tab) =>
    `px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
      activeTab === tab
        ? "border-emerald-600 text-emerald-700"
        : "border-transparent text-gray-500 hover:text-gray-700"
    }`

  return (
    <div>
      <div className="flex border-b border-gray-200 mb-6">
        <button className={tabClass("users")} onClick={() => setActiveTab("users")}>
          Users
        </button>
        <button className={tabClass("columns")} onClick={() => setActiveTab("columns")}>
          Columns
        </button>
        <button className={tabClass("facilities")} onClick={() => setActiveTab("facilities")}>
          Facilities
        </button>
        <button className={tabClass("news")} onClick={() => setActiveTab("news")}>
          News
        </button>
      </div>

      {activeTab === "users" && <UsersTab users={users} />}
      {activeTab === "columns" && (
        <ColumnVisibilityTab
          columnVisibility={columnVisibility}
          columnFilters={columnFilters}
          allFilterValues={allFilterValues}
          valueCounts={valueCounts}
          totalFacilities={totalFacilities}
        />
      )}
      {activeTab === "facilities" && <FacilitiesTab facilities={facilities} />}
      {activeTab === "news" && <NewsTab initialNews={initialNews} />}
    </div>
  )
}
```

- [ ] **Step 4: Update `src/app/admin/page.tsx`**

Add `fetchAllNews` import + fetch + pass to `AdminClient`. The only changes are one import line, one extra `Promise.all` entry, and one new prop on `<AdminClient>`.

Updated file:

```typescript
// src/app/admin/page.tsx
import { createSupabaseAdminClient } from "@/lib/supabase/admin"
import { createSupabaseServerClient } from "@/lib/supabase/server"
import { redirect } from "next/navigation"
import Header from "@/components/Header"
import AdminClient from "./AdminClient"
import { fetchColumnVisibility, fetchColumnFilters, fetchFacilities } from "@/lib/facilities"
import { fetchAllNews } from "@/lib/news"

export default async function AdminPage() {
  const supabase = createSupabaseServerClient()
  const {
    data: { user },
  } = await supabase.auth.getUser()
  if (!user) redirect("/login")

  const { data: profile } = await supabase
    .from("profiles")
    .select("role")
    .eq("id", user.id)
    .single()
  if (profile?.role !== "admin") redirect("/")

  const admin = createSupabaseAdminClient()
  const [{ data: users }, columnVisibility, columnFilters, facilities, initialNews] =
    await Promise.all([
      admin
        .from("profiles")
        .select("id, email, role, blocked, created_at")
        .order("created_at", { ascending: false }),
      fetchColumnVisibility(admin),
      fetchColumnFilters(admin),
      fetchFacilities(admin),
      fetchAllNews(admin),
    ])

  const allFilterValues = {
    regions: [...new Set(facilities.map((f) => f.location.region).filter(Boolean))].sort() as string[],
    facilityTypes: [...new Set(facilities.map((f) => f.facilityType).filter(Boolean))].sort() as string[],
    countries: [...new Set(facilities.map((f) => f.location.country).filter(Boolean))].sort() as string[],
    sources: [...new Set(facilities.map((f) => f.source ?? "").filter(Boolean))].sort() as string[],
    modalities: [...new Set(facilities.flatMap((f) => f.modalities).filter(Boolean))].sort() as string[],
  }

  const valueCounts: Record<string, Record<string, number>> = {
    region: {},
    facilityType: {},
    country: {},
    source: {},
    modality: {},
  }
  for (const f of facilities) {
    if (f.location.region)
      valueCounts.region[f.location.region] = (valueCounts.region[f.location.region] ?? 0) + 1
    if (f.facilityType)
      valueCounts.facilityType[f.facilityType] = (valueCounts.facilityType[f.facilityType] ?? 0) + 1
    if (f.location.country)
      valueCounts.country[f.location.country] = (valueCounts.country[f.location.country] ?? 0) + 1
    if (f.source)
      valueCounts.source[f.source] = (valueCounts.source[f.source] ?? 0) + 1
    for (const m of f.modalities)
      valueCounts.modality[m] = (valueCounts.modality[m] ?? 0) + 1
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />
      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Admin Panel</h2>
        <AdminClient
          users={users ?? []}
          columnVisibility={columnVisibility}
          columnFilters={columnFilters}
          allFilterValues={allFilterValues}
          valueCounts={valueCounts}
          totalFacilities={facilities.length}
          facilities={facilities}
          initialNews={initialNews}
        />
      </main>
    </div>
  )
}
```

- [ ] **Step 5: Verify TypeScript compiles and build passes**

```bash
npx tsc --noEmit && npm run build
```
Expected: zero TypeScript errors, successful build.

- [ ] **Step 6: Manual browser test of admin News tab**

Run `npm run dev`. Navigate to `http://localhost:3000/admin` (must be logged in as admin).

Verify:
1. A "News" tab appears in the admin panel alongside Users, Columns, Facilities.
2. Clicking "News" shows the add form and an empty items list.
3. Fill in the form (date, headline, body, product_tags: "vitamin a", company_tags: "basf", event_type: "expansion") and submit — page reloads and the item appears in the list.
4. Click "Delete" on the item — it disappears from the list.
5. Go back to the main page, type "vitamin A" in the Ask panel — the synthesised answer now includes the news item you just added in its developments section.

- [ ] **Step 7: Commit**

```bash
git add src/actions/news.ts src/components/admin/NewsTab.tsx src/app/admin/AdminClient.tsx src/app/admin/page.tsx
git commit -m "feat: add admin News tab for curated market intelligence"
git push
```
