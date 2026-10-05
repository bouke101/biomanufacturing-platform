// src/components/FilterBar.tsx
'use client'
import { getFilterOptions } from '@/lib/facilities'
import type { Facility, Modality, FacilityType } from '@/types/facility'

interface FilterBarProps {
  facilities: Facility[]
  globalSearch: string
  setGlobalSearch: (v: string) => void
  modality: Modality | ''
  setModality: (v: Modality | '') => void
  region: string
  setRegion: (v: string) => void
  facilityType: FacilityType | ''
  setFacilityType: (v: FacilityType | '') => void
  resultCount: number
}

export default function FilterBar({
  facilities, globalSearch, setGlobalSearch,
  modality, setModality, region, setRegion,
  facilityType, setFacilityType, resultCount,
}: FilterBarProps) {
  const opts = getFilterOptions(facilities)

  return (
    <div className="flex flex-wrap gap-3 items-center p-4 bg-white border-b border-gray-200">
      <input
        type="text"
        placeholder="Search facilities, owners, products…"
        value={globalSearch}
        onChange={(e) => setGlobalSearch(e.target.value)}
        className="flex-1 min-w-[220px] px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
      />
      <select
        value={modality}
        onChange={(e) => setModality(e.target.value as Modality | '')}
        className="px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
      >
        <option value="">All modalities</option>
        {opts.modalities.map((m) => <option key={m} value={m}>{m}</option>)}
      </select>
      <select
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        className="px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
      >
        <option value="">All regions</option>
        {opts.regions.map((r) => <option key={r} value={r}>{r}</option>)}
      </select>
      <select
        value={facilityType}
        onChange={(e) => setFacilityType(e.target.value as FacilityType | '')}
        className="px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
      >
        <option value="">All types</option>
        {opts.facilityTypes.map((t) => <option key={t} value={t}>{t}</option>)}
      </select>
      <span className="text-sm text-gray-500 ml-auto whitespace-nowrap">
        {resultCount} {resultCount === 1 ? 'facility' : 'facilities'}
      </span>
    </div>
  )
}
