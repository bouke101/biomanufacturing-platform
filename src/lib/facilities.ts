// src/lib/facilities.ts
import type { SupabaseClient } from '@supabase/supabase-js'
import type { Facility, Modality, FacilityType } from '@/types/facility'

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

export async function fetchFacilities(supabase: SupabaseClient): Promise<Facility[]> {
  const { data, error } = await supabase
    .from('facilities')
    .select('*')
    .order('name')
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
