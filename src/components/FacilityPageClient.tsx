// src/components/FacilityPageClient.tsx
'use client'
import { useFacilityFilters } from '@/hooks/useFacilityFilters'
import FilterBar from '@/components/FilterBar'
import FacilityTable from '@/components/FacilityTable/FacilityTable'
import FacilityMap from '@/components/FacilityMap'
import type { Facility } from '@/types/facility'

interface FacilityPageClientProps {
  initialFacilities: Facility[]
  columnVisibility: Record<string, boolean>
}

export default function FacilityPageClient({
  initialFacilities,
  columnVisibility,
}: FacilityPageClientProps) {
  const filters = useFacilityFilters(initialFacilities)

  return (
    <>
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
      <div className="flex flex-col flex-1 overflow-hidden">
        <div className="h-[40vh] shrink-0 border-b border-gray-200">
          <FacilityMap
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
          />
        </div>
        <div className="flex-1 overflow-auto min-w-0">
          <FacilityTable
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
            columnVisibility={columnVisibility}
          />
        </div>
      </div>
    </>
  )
}
