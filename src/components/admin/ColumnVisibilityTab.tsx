'use client'
import { useState, useTransition } from 'react'
import { updateColumnVisibility } from '@/actions/admin'

const COLUMN_LABELS: Record<string, string> = {
  name: 'Facility Name',
  owner: 'Owner',
  location: 'Location',
  facilityType: 'Type',
  modalities: 'Modalities',
  region: 'Region',
}

interface ColumnVisibilityTabProps {
  columnVisibility: Record<string, boolean>
}

export default function ColumnVisibilityTab({ columnVisibility }: ColumnVisibilityTabProps) {
  const [visibility, setVisibility] = useState(columnVisibility)
  const [saved, setSaved] = useState(false)
  const [pending, startTransition] = useTransition()

  function toggle(key: string) {
    setVisibility((prev) => ({ ...prev, [key]: !prev[key] }))
    setSaved(false)
  }

  function save() {
    startTransition(async () => {
      await updateColumnVisibility(visibility)
      setSaved(true)
    })
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 max-w-md">
      <p className="text-sm text-gray-500 mb-4">
        Toggle which columns are visible to all visitors on the facility table.
      </p>
      <div className="space-y-3">
        {Object.entries(COLUMN_LABELS).map(([key, label]) => (
          <label key={key} className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={visibility[key] !== false}
              onChange={() => toggle(key)}
              className="w-4 h-4 accent-emerald-600"
            />
            <span className="text-sm text-gray-800">{label}</span>
          </label>
        ))}
      </div>
      <div className="mt-6 flex items-center gap-3">
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
