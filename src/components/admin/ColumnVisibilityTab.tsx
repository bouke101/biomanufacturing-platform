'use client'
import { useState, useTransition } from 'react'
import { updateColumnVisibility, updateColumnFilters } from '@/actions/admin'
import type { ColumnFilters } from '@/lib/facilities'
import type { AllFilterValues } from './ContentFiltersTab'

interface Props {
  columnVisibility: Record<string, boolean>
  columnFilters: ColumnFilters
  allFilterValues: AllFilterValues
  valueCounts: Record<string, Record<string, number>>
  totalFacilities: number
}

interface ColumnEntry {
  visKey: string | null   // null = no visibility toggle (filter-only row)
  label: string
  filterKey: string | null
  valuesKey: keyof AllFilterValues | null
  searchable?: boolean
}

const COLUMNS: ColumnEntry[] = [
  { visKey: 'name',         label: 'Facility Name', filterKey: null,           valuesKey: null },
  { visKey: 'owner',        label: 'Owner',          filterKey: null,           valuesKey: null },
  { visKey: 'location',     label: 'Location',       filterKey: 'country',      valuesKey: 'countries',    searchable: true },
  { visKey: 'facilityType', label: 'Facility Type',  filterKey: 'facilityType', valuesKey: 'facilityTypes' },
  { visKey: 'modalities',   label: 'Modalities',     filterKey: 'modality',     valuesKey: 'modalities' },
  { visKey: 'region',       label: 'Region',         filterKey: 'region',       valuesKey: 'regions' },
  { visKey: null,           label: 'Source',         filterKey: 'source',       valuesKey: 'sources' },
]

function initChecked(filters: ColumnFilters, allValues: AllFilterValues): Record<string, Set<string>> {
  const out: Record<string, Set<string>> = {}
  for (const col of COLUMNS) {
    if (!col.filterKey || !col.valuesKey) continue
    const all = allValues[col.valuesKey] as string[]
    const saved = filters[col.filterKey]
    out[col.filterKey] = saved?.length ? new Set(saved) : new Set(all)
  }
  return out
}

export default function ColumnVisibilityTab({ columnVisibility, columnFilters, allFilterValues, valueCounts, totalFacilities }: Props) {
  const [visibility, setVisibility] = useState(columnVisibility)
  const [checked, setChecked] = useState(() => initChecked(columnFilters, allFilterValues))
  const [expanded, setExpanded] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [saved, setSaved] = useState(false)
  const [pending, startTransition] = useTransition()

  function toggleVisibility(key: string) {
    setVisibility((prev) => ({ ...prev, [key]: !prev[key] }))
    setSaved(false)
  }

  function toggleFilter(filterKey: string, value: string) {
    setChecked((prev) => {
      const next = new Set(prev[filterKey])
      if (next.has(value)) next.delete(value)
      else next.add(value)
      return { ...prev, [filterKey]: next }
    })
    setSaved(false)
  }

  function selectAll(filterKey: string, vals: string[]) {
    setChecked((prev) => ({ ...prev, [filterKey]: new Set(vals) }))
    setSaved(false)
  }

  function selectNone(filterKey: string) {
    setChecked((prev) => ({ ...prev, [filterKey]: new Set() }))
    setSaved(false)
  }

  function handleExpand(filterKey: string) {
    setExpanded((prev) => (prev === filterKey ? null : filterKey))
    setSearch('')
  }

  function save() {
    const filtersPayload: ColumnFilters = {}
    for (const col of COLUMNS) {
      if (!col.filterKey || !col.valuesKey) continue
      const all = allFilterValues[col.valuesKey] as string[]
      const cur = checked[col.filterKey]
      filtersPayload[col.filterKey] = cur.size === all.length ? [] : [...cur].sort()
    }
    startTransition(async () => {
      await Promise.all([
        updateColumnVisibility(visibility),
        updateColumnFilters(filtersPayload),
      ])
      setSaved(true)
    })
  }

  return (
    <div className="max-w-lg space-y-2">
      <p className="text-sm text-gray-500 mb-4">
        Toggle column visibility and click a column to filter which values visitors can see.
      </p>

      {COLUMNS.map((col) => {
        const isOpen = col.filterKey ? expanded === col.filterKey : false
        const allVals = col.valuesKey ? (allFilterValues[col.valuesKey] as string[]) : []
        const cur = col.filterKey ? checked[col.filterKey] : new Set<string>()
        const allSelected = cur.size === allVals.length
        const displayed = col.searchable
          ? allVals.filter((v) => v.toLowerCase().includes(search.toLowerCase()))
          : allVals

        return (
          <div
            key={col.visKey ?? col.filterKey ?? col.label}
            className={`rounded-lg border transition-colors ${
              isOpen ? 'border-emerald-300 bg-emerald-50/40' : 'border-gray-200 bg-white'
            }`}
          >
            {/* Row header */}
            <div
              className={`flex items-center gap-3 px-4 py-3 ${col.filterKey ? 'cursor-pointer' : ''}`}
              onClick={() => col.filterKey && handleExpand(col.filterKey)}
            >
              {/* Visibility checkbox */}
              {col.visKey ? (
                <input
                  type="checkbox"
                  checked={visibility[col.visKey] !== false}
                  onChange={(e) => { e.stopPropagation(); toggleVisibility(col.visKey!) }}
                  onClick={(e) => e.stopPropagation()}
                  className="w-4 h-4 accent-emerald-600 shrink-0"
                />
              ) : (
                <span className="w-4 h-4 shrink-0" />
              )}

              <span className="flex-1 text-sm font-medium text-gray-800">{col.label}</span>

              {col.filterKey && (
                <span className={`text-xs px-2 py-0.5 rounded-full mr-1 ${
                  allSelected ? 'text-gray-400' : 'bg-amber-100 text-amber-700 font-medium'
                }`}>
                  {allSelected ? 'all' : `${cur.size}/${allVals.length}`}
                </span>
              )}

              {col.filterKey && (
                <svg
                  className={`w-4 h-4 text-gray-400 transition-transform shrink-0 ${isOpen ? 'rotate-180' : ''}`}
                  fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              )}
            </div>

            {/* Expanded filter section */}
            {isOpen && col.filterKey && (
              <div className="px-4 pb-4 border-t border-emerald-100">
                <div className="flex items-center justify-between mt-3 mb-2">
                  <span className="text-xs text-gray-500">Visible values</span>
                  <div className="flex gap-2">
                    <button onClick={() => selectAll(col.filterKey!, allVals)} className="text-xs text-emerald-700 hover:underline">All</button>
                    <span className="text-gray-300">|</span>
                    <button onClick={() => selectNone(col.filterKey!)} className="text-xs text-gray-500 hover:underline">None</button>
                  </div>
                </div>

                {col.searchable && (
                  <input
                    type="text"
                    placeholder={`Search ${col.label.toLowerCase()}…`}
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full mb-2 px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    onClick={(e) => e.stopPropagation()}
                  />
                )}

                <div className={`grid gap-y-1.5 gap-x-4 ${
                  col.searchable
                    ? 'grid-cols-2 sm:grid-cols-3 max-h-44 overflow-y-auto pr-1'
                    : allVals.length > 6 ? 'grid-cols-2 sm:grid-cols-3' : 'grid-cols-2'
                }`}>
                  {displayed.map((v) => {
                    const count = valueCounts[col.filterKey!]?.[v] ?? 0
                    return (
                      <label key={v} className="flex items-center gap-2 cursor-pointer" onClick={(e) => e.stopPropagation()}>
                        <input
                          type="checkbox"
                          checked={cur.has(v)}
                          onChange={() => toggleFilter(col.filterKey!, v)}
                          className="w-3.5 h-3.5 accent-emerald-600 shrink-0"
                        />
                        <span className="text-xs text-gray-700 truncate">{v || '(empty)'}</span>
                        <span className="text-xs text-gray-400 shrink-0 ml-auto">{count}/{totalFacilities}</span>
                      </label>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        )
      })}

      <div className="flex items-center gap-3 pt-3">
        <button
          onClick={save}
          disabled={pending}
          className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 disabled:opacity-50 transition-colors"
        >
          {pending ? 'Saving…' : 'Save'}
        </button>
        {saved && <span className="text-sm text-emerald-700">Saved!</span>}
      </div>
    </div>
  )
}
