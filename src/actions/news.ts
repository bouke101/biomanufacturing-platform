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
