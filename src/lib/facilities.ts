import rawData from '../../data/facilities.json'
import type { Facility, Modality, FacilityType } from '@/types/facility'

export function loadFacilities(): Facility[] {
  return rawData as Facility[]
}

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
