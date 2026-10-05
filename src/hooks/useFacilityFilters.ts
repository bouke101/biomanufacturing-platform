'use client'
import { useState, useMemo } from 'react'
import { loadFacilities } from '@/lib/facilities'
import type { Modality, FacilityType } from '@/types/facility'

export function useFacilityFilters() {
  const facilities = useMemo(() => loadFacilities(), [])
  const [globalSearch, setGlobalSearch] = useState('')
  const [modality, setModality] = useState<Modality | ''>('')
  const [region, setRegion] = useState<string>('')
  const [facilityType, setFacilityType] = useState<FacilityType | ''>('')
  const [selectedId, setSelectedId] = useState<string | null>(null)

  const filtered = useMemo(() => {
    const q = globalSearch.toLowerCase()
    return facilities.filter((f) => {
      const matchesSearch =
        !q ||
        f.name.toLowerCase().includes(q) ||
        f.owner.toLowerCase().includes(q) ||
        f.location.city.toLowerCase().includes(q) ||
        f.location.country.toLowerCase().includes(q) ||
        f.products.some((p) => p.toLowerCase().includes(q)) ||
        f.modalities.some((m) => m.toLowerCase().includes(q))
      const matchesModality = !modality || f.modalities.includes(modality)
      const matchesRegion = !region || f.location.region === region
      const matchesType = !facilityType || f.facilityType === facilityType
      return matchesSearch && matchesModality && matchesRegion && matchesType
    })
  }, [facilities, globalSearch, modality, region, facilityType])

  return {
    facilities,
    filtered,
    globalSearch, setGlobalSearch,
    modality, setModality,
    region, setRegion,
    facilityType, setFacilityType,
    selectedId, setSelectedId,
  }
}
