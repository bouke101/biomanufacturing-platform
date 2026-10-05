// src/components/FacilityTable/FacilityTable.tsx
'use client'
import React, { useState } from 'react'
import {
  useTable,
  flexRender,
  type SortingState,
} from '@tanstack/react-table'
import { columns, features } from './columns'
import FacilityDetail from './FacilityDetail'
import type { Facility } from '@/types/facility'

interface FacilityTableProps {
  filtered: Facility[]
  selectedId: string | null
  setSelectedId: (id: string | null) => void
}

export default function FacilityTable({ filtered, selectedId, setSelectedId }: FacilityTableProps) {
  const [sorting, setSorting] = useState<SortingState>([])

  const table = useTable({
    features,
    data: filtered,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getRowId: (row) => row.id,
  })

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead className="bg-gray-100 sticky top-0 z-10">
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wide cursor-pointer select-none hover:bg-gray-200"
                  onClick={header.column.getToggleSortingHandler()}
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                  {header.column.getIsSorted() === 'asc' ? ' ↑' : header.column.getIsSorted() === 'desc' ? ' ↓' : ''}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => {
            const isSelected = row.id === selectedId
            const facility = row.original
            return (
              <React.Fragment key={row.id}>
                <tr
                  onClick={() => setSelectedId(isSelected ? null : row.id)}
                  className={`border-b border-gray-100 cursor-pointer transition-colors
                    ${isSelected ? 'bg-emerald-50' : 'hover:bg-gray-50'}`}
                >
                  {row.getAllCells().map((cell) => (
                    <td key={cell.id} className="px-4 py-3">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
                {isSelected && (
                  <tr>
                    <td colSpan={columns.length}>
                      <FacilityDetail facility={facility} />
                    </td>
                  </tr>
                )}
              </React.Fragment>
            )
          })}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="px-4 py-8 text-center text-gray-400">
                No facilities match the current filters.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
