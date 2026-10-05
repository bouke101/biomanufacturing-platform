// src/components/FacilityTable/FacilityDetail.tsx
import type { Facility } from '@/types/facility'

export default function FacilityDetail({ facility }: { facility: Facility }) {
  return (
    <div className="p-4 bg-emerald-50 border-t border-emerald-100">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <p className="font-semibold text-gray-800 mb-1">Capacity</p>
          <p className="text-gray-600">{facility.capacity || '—'}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Scale</p>
          <p className="text-gray-600">{facility.scale.join(' · ')}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Products</p>
          <p className="text-gray-600">{facility.products.join(', ') || '—'}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Known clients</p>
          <p className="text-gray-600">{facility.clients.length ? facility.clients.join(', ') : 'Confidential'}</p>
        </div>
        <div className="md:col-span-2">
          <p className="font-semibold text-gray-800 mb-1">Legacy</p>
          <p className="text-gray-600">{facility.legacy}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Certifications</p>
          <p className="text-gray-600">{facility.certifications.join(' · ') || '—'}</p>
        </div>
        <div>
          <p className="font-semibold text-gray-800 mb-1">Notes</p>
          <p className="text-gray-600">{facility.notes || '—'}</p>
        </div>
        {facility.website && (
          <div>
            <a href={facility.website} target="_blank" rel="noopener noreferrer"
              className="text-emerald-700 hover:underline text-sm">
              Visit website →
            </a>
          </div>
        )}
      </div>
    </div>
  )
}
