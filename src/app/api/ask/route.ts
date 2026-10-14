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
