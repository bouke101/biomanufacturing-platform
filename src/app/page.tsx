// src/app/page.tsx
'use client'
import { useFacilityFilters } from '@/hooks/useFacilityFilters'
import FilterBar from '@/components/FilterBar'
import FacilityTable from '@/components/FacilityTable/FacilityTable'
import FacilityMap from '@/components/FacilityMap'

export default function Home() {
  const filters = useFacilityFilters()

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-4 shrink-0">
        <div>
          <h1 className="text-lg font-bold text-gray-900">Biomanufacturing Facility Map</h1>
          <p className="text-xs text-gray-500">Global CMO &amp; CDMO intelligence platform</p>
        </div>
      </header>

      {/* Filter bar */}
      <FilterBar
        facilities={filters.facilities}
        globalSearch={filters.globalSearch}
        setGlobalSearch={filters.setGlobalSearch}
        modality={filters.modality}
        setModality={filters.setModality}
        region={filters.region}
        setRegion={filters.setRegion}
        facilityType={filters.facilityType}
        setFacilityType={filters.setFacilityType}
        resultCount={filters.filtered.length}
      />

      {/* Split view: map top, table bottom */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Map */}
        <div className="h-[40vh] shrink-0 border-b border-gray-200">
          <FacilityMap
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
          />
        </div>

        {/* Table */}
        <div className="flex-1 overflow-auto">
          <FacilityTable
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
          />
        </div>
      </div>
    </div>
  )
}
