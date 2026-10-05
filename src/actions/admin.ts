// src/actions/admin.ts
'use server'
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

async function requireAdmin() {
  const supabase = createSupabaseServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()
  if (profile?.role !== 'admin') redirect('/')
}

export async function blockUser(userId: string, blocked: boolean) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin
    .from('profiles')
    .update({ blocked })
    .eq('id', userId)
  if (error) throw new Error(error.message)
}

export async function updateColumnVisibility(visibility: Record<string, boolean>) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin
    .from('settings')
    .upsert({ key: 'column_visibility', value: visibility })
  if (error) throw new Error(error.message)
}
