// src/lib/facilities.ts
import type { SupabaseClient } from '@supabase/supabase-js'
import type { Facility, Modality, FacilityType } from '@/types/facility'

export type ColumnFilters = Record<string, string[]>

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

export async function fetchColumnFilters(
  supabase: SupabaseClient
): Promise<ColumnFilters> {
  const { data } = await supabase
    .from('settings')
    .select('value')
    .eq('key', 'column_filters')
    .single()
  return (data?.value as ColumnFilters) ?? {}
}

export async function fetchFacilities(
  supabase: SupabaseClient,
  columnFilters?: ColumnFilters
): Promise<Facility[]> {
  let query = supabase.from('facilities').select('*').order('name')

  if (columnFilters) {
    if (columnFilters.region?.length)       query = query.in('region', columnFilters.region)
    if (columnFilters.facilityType?.length) query = query.in('facility_type', columnFilters.facilityType)
    if (columnFilters.country?.length)      query = query.in('country', columnFilters.country)
    if (columnFilters.source?.length)       query = query.in('source', columnFilters.source)
    if (columnFilters.modality?.length)     query = query.containedBy('modalities', columnFilters.modality)
  }

  const { data, error } = await query
  if (error) throw new Error(error.message)
  return (data ?? []).map((row) => ({
    id: row.id,
    name: row.name,
    owner: row.owner,
    location: {
      city: row.city,
      country: row.country,
      region: row.region as Facility['location']['region'],
      lat: row.lat,
      lng: row.lng,
    },
    facilityType: row.facility_type as Facility['facilityType'],
    modalities: row.modalities as Facility['modalities'],
    scale: row.scale as Facility['scale'],
    capacity: row.capacity,
    clients: row.clients,
    products: row.products,
    legacy: row.legacy,
    certifications: row.certifications,
    website: row.website,
    imageUrl: row.image_url,
    notes: row.notes,
    visible: row.visible,
    source: row.source as Facility['source'],
    pilots4uPage: row.pilots4u_page,
  }))
}

export async function fetchColumnVisibility(
  supabase: SupabaseClient
): Promise<Record<string, boolean>> {
  const { data } = await supabase
    .from('settings')
    .select('value')
    .eq('key', 'column_visibility')
    .single()
  return (data?.value as Record<string, boolean>) ?? {
    name: true,
    owner: true,
    location: true,
    facilityType: true,
    modalities: true,
    region: true,
  }
}
