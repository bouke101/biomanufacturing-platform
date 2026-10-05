// src/components/FacilityMap/index.tsx
import dynamic from 'next/dynamic'
import type { Facility } from '@/types/facility'

interface FacilityMapProps {
  filtered: Facility[]
  selectedId: string | null
  setSelectedId: (id: string | null) => void
}

const FacilityMap = dynamic<FacilityMapProps>(
  () => import('./Map'),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full flex items-center justify-center bg-gray-100">
        <span className="text-gray-400 text-sm">Loading map…</span>
      </div>
    ),
  }
)

export default FacilityMap
