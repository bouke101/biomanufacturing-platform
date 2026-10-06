import { createClient } from '@supabase/supabase-js'
import facilityData from '../data/facilities.json'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

async function seed() {
  const rows = (facilityData as any[]).map((f) => ({
    id: f.id,
    name: f.name,
    owner: f.owner,
    city: f.location.city,
    country: f.location.country,
    region: f.location.region,
    lat: f.location.lat,
    lng: f.location.lng,
    facility_type: f.facilityType,
    modalities: f.modalities,
    scale: f.scale,
    capacity: f.capacity,
    clients: f.clients,
    products: f.products,
    legacy: f.legacy,
    certifications: f.certifications,
    website: f.website,
    image_url: f.imageUrl,
    notes: f.notes,
    visible: f.visible ?? true,
    source: f.source ?? 'manual',
    pilots4u_page: f.pilots4uPage ?? '',
  }))

  const { error } = await supabase.from('facilities').upsert(rows)
  if (error) {
    console.error('Seed failed:', error.message)
    process.exit(1)
  }
  console.log(`Seeded ${rows.length} facilities.`)
}

seed()
