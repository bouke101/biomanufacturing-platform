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

export interface FacilityFormData {
  id: string
  name: string
  owner: string
  city: string
  country: string
  region: string
  lat: number
  lng: number
  facilityType: string
  modalities: string[]
  scale: string[]
  capacity: string
  clients: string[]
  products: string[]
  legacy: string
  certifications: string[]
  website: string
  imageUrl: string
  notes: string
  visible: boolean
}

export async function upsertFacility(data: FacilityFormData) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const row = {
    id: data.id,
    name: data.name,
    owner: data.owner,
    city: data.city,
    country: data.country,
    region: data.region,
    lat: data.lat,
    lng: data.lng,
    facility_type: data.facilityType,
    modalities: data.modalities,
    scale: data.scale,
    capacity: data.capacity,
    clients: data.clients,
    products: data.products,
    legacy: data.legacy,
    certifications: data.certifications,
    website: data.website,
    image_url: data.imageUrl,
    notes: data.notes,
    visible: data.visible,
  }
  const { error } = await admin.from('facilities').upsert(row)
  if (error) throw new Error(error.message)
}

export async function deleteFacility(id: string) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin.from('facilities').delete().eq('id', id)
  if (error) throw new Error(error.message)
}

export async function toggleFacilityVisible(id: string, visible: boolean) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin
    .from('facilities')
    .update({ visible })
    .eq('id', id)
  if (error) throw new Error(error.message)
}
