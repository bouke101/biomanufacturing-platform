// src/components/FacilityTable/columns.tsx
import { createColumnHelper, tableFeatures, rowSortingFeature, createSortedRowModel } from '@tanstack/react-table'
import type { Facility } from '@/types/facility'

export const features = tableFeatures({
  rowSortingFeature,
  sortedRowModel: createSortedRowModel(),
})

const helper = createColumnHelper<typeof features, Facility>()

export const allColumns = helper.columns([
  helper.accessor('name', {
    id: 'name',
    header: 'Facility',
    cell: (info) => <span className="font-medium text-gray-900">{info.getValue()}</span>,
  }),
  helper.accessor('owner', {
    id: 'owner',
    header: 'Owner',
    cell: (info) => <span className="text-gray-700">{info.getValue()}</span>,
  }),
  helper.accessor((row) => row.location.city + ', ' + row.location.country, {
    id: 'location',
    header: 'Location',
    cell: (info) => <span className="text-gray-600">{info.getValue()}</span>,
  }),
  helper.accessor('facilityType', {
    id: 'facilityType',
    header: 'Type',
    cell: (info) => (
      <span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800">
        {info.getValue()}
      </span>
    ),
  }),
  helper.accessor((row) => row.modalities.join(', '), {
    id: 'modalities',
    header: 'Modalities',
    cell: (info) => <span className="text-sm text-gray-600">{info.getValue()}</span>,
  }),
  helper.accessor((row) => row.location.region, {
    id: 'region',
    header: 'Region',
    cell: (info) => <span className="text-gray-600">{info.getValue()}</span>,
  }),
])
