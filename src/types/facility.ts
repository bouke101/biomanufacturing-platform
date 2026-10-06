export type FacilityType = 'CMO' | 'CDMO' | 'Captive' | 'Toll' | 'Pilot'
export type Scale = 'Development' | 'Pilot' | 'Commercial'
export type Modality =
  | 'Mammalian cell culture'
  | 'Microbial fermentation'
  | 'Fermentation (industrial)'
  | 'Viral vector'
  | 'mRNA'
  | 'ADC'
  | 'Lipid nanoparticle'
  | 'Enzymes'
  | 'Probiotics & cultures'
  | 'Algae'
  | 'Enzymatic catalysis'
  | 'Separation'
  | 'Size reduction'
  | 'Sterilisation'
  | 'Chemical conversion'
  | 'Thermochemical'
  | 'Thermal processing'
  | 'Material technologies'
  | 'Pulping'

export interface FacilityLocation {
  city: string
  country: string
  region: 'Europe' | 'North America' | 'Asia-Pacific' | 'Other'
  lat: number
  lng: number
}

export interface Facility {
  id: string
  name: string
  owner: string
  location: FacilityLocation
  facilityType: FacilityType
  modalities: Modality[]
  scale: Scale[]
  capacity: string          // e.g. "80,000 L bioreactor volume" — empty string if unknown
  clients: string[]         // known clients; empty array if confidential
  products: string[]        // product/ingredient categories
  legacy: string            // founding year + key history (1–2 sentences)
  certifications: string[]  // e.g. ["FDA", "EMA GMP", "ISO 9001"]
  website: string
  imageUrl: string          // relative path under /images/facilities/ or logo URL for Pilots4U entries
  notes: string
  visible?: boolean
  source?: 'manual' | 'pilots4u'
  pilots4uPage?: string
}
