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
