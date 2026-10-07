'use client'
import { useState, useTransition } from 'react'
import { updateColumnFilters } from '@/actions/admin'
import type { ColumnFilters } from '@/lib/facilities'

export interface AllFilterValues {
  regions: string[]
  facilityTypes: string[]
  countries: string[]
  sources: string[]
  modalities: string[]
}

interface Props {
  filters: ColumnFilters
  allValues: AllFilterValues
}

const SECTIONS: Array<{
  key: string
  label: string
  valuesKey: keyof AllFilterValues
}> = [
  { key: 'region',       label: 'Region',        valuesKey: 'regions' },
  { key: 'facilityType', label: 'Facility Type',  valuesKey: 'facilityTypes' },
  { key: 'modality',     label: 'Modality',       valuesKey: 'modalities' },
  { key: 'source',       label: 'Source',         valuesKey: 'sources' },
  { key: 'country',      label: 'Country',        valuesKey: 'countries' },
]

// normalise: missing key or empty array → all values are active (nothing filtered)
function activeSet(filters: ColumnFilters, key: string, allVals: string[]): Set<string> {
  const saved = filters[key]
  return saved && saved.length > 0 ? new Set(saved) : new Set(allVals)
}

export default function ContentFiltersTab({ filters, allValues }: Props) {
  // local state: key → Set of currently-checked values
  const [checked, setChecked] = useState<Record<string, Set<string>>>(() =>
    Object.fromEntries(
      SECTIONS.map(({ key, valuesKey }) => [
        key,
        activeSet(filters, key, allValues[valuesKey]),
      ])
    )
  )
  const [countrySearch, setCountrySearch] = useState('')
  const [saved, setSaved] = useState(false)
  const [pending, startTransition] = useTransition()

  function toggle(sectionKey: string, value: string) {
    setChecked((prev) => {
      const next = new Set(prev[sectionKey])
      if (next.has(value)) next.delete(value)
      else next.add(value)
      return { ...prev, [sectionKey]: next }
    })
    setSaved(false)
  }

  function selectAll(sectionKey: string, vals: string[]) {
    setChecked((prev) => ({ ...prev, [sectionKey]: new Set(vals) }))
    setSaved(false)
  }

  function selectNone(sectionKey: string) {
    setChecked((prev) => ({ ...prev, [sectionKey]: new Set() }))
    setSaved(false)
  }

  function save() {
    // Build the payload: empty array means "all allowed" (no restriction)
    const payload: ColumnFilters = {}
    for (const { key, valuesKey } of SECTIONS) {
      const all = allValues[valuesKey]
      const current = checked[key]
      // If every value is checked → store empty array (= no filter)
      payload[key] = current.size === all.length ? [] : [...current].sort()
    }
    startTransition(async () => {
      await updateColumnFilters(payload)
      setSaved(true)
    })
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <p className="text-sm text-gray-500">
        Select which values are visible to visitors for each column.
        Unchecked values hide all matching facilities from the map and table.
      </p>

      {SECTIONS.map(({ key, label, valuesKey }) => {
        const vals = allValues[valuesKey]
        const cur  = checked[key]
        const isCountry = key === 'country'
        const displayed = isCountry
          ? vals.filter((v) => v.toLowerCase().includes(countrySearch.toLowerCase()))
          : vals

        return (
          <div key={key} className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-800">{label}</h3>
              <div className="flex gap-2">
                <button
                  onClick={() => selectAll(key, vals)}
                  className="text-xs text-emerald-700 hover:underline"
                >
                  All
                </button>
                <span className="text-gray-300">|</span>
                <button
                  onClick={() => selectNone(key)}
                  className="text-xs text-gray-500 hover:underline"
                >
                  None
                </button>
              </div>
            </div>

            {isCountry && (
              <input
                type="text"
                placeholder="Search countries…"
                value={countrySearch}
                onChange={(e) => setCountrySearch(e.target.value)}
                className="w-full mb-3 px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            )}

            <div className={`grid gap-y-2 gap-x-4 ${isCountry ? 'grid-cols-2 sm:grid-cols-3 max-h-52 overflow-y-auto pr-1' : 'grid-cols-2 sm:grid-cols-3'}`}>
              {displayed.map((v) => (
                <label key={v} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={cur.has(v)}
                    onChange={() => toggle(key, v)}
                    className="w-4 h-4 accent-emerald-600 shrink-0"
                  />
                  <span className="text-sm text-gray-700 truncate">{v || '(empty)'}</span>
                </label>
              ))}
            </div>

            <p className="mt-2 text-xs text-gray-400">
              {cur.size} / {vals.length} selected
            </p>
          </div>
        )
      })}

      <div className="flex items-center gap-3 pt-2">
        <button
          onClick={save}
          disabled={pending}
          className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 disabled:opacity-50 transition-colors"
        >
          {pending ? 'Saving…' : 'Save filters'}
        </button>
        {saved && <span className="text-sm text-emerald-700">Saved!</span>}
      </div>
    </div>
  )
}
