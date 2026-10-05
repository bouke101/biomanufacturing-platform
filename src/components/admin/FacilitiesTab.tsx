// src/components/admin/FacilitiesTab.tsx
'use client'
import { useState, useTransition } from 'react'
import { deleteFacility, toggleFacilityVisible } from '@/actions/admin'
import FacilityForm from './FacilityForm'
import type { Facility } from '@/types/facility'

export default function FacilitiesTab({ facilities: initial }: { facilities: Facility[] }) {
  const [facilities, setFacilities] = useState(initial)
  const [editing, setEditing] = useState<Facility | null | 'new'>(null)
  const [pending, startTransition] = useTransition()

  function handleDelete(id: string) {
    if (!confirm('Delete this facility?')) return
    startTransition(async () => {
      await deleteFacility(id)
      setFacilities((prev) => prev.filter((f) => f.id !== id))
    })
  }

  function handleToggleVisible(id: string, current: boolean) {
    startTransition(async () => {
      await toggleFacilityVisible(id, !current)
      setFacilities((prev) =>
        prev.map((f) => (f.id === id ? { ...f, visible: !current } : f))
      )
    })
  }

  function handleSaved() {
    // Reload to get fresh data from DB
    window.location.reload()
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <p className="text-sm text-gray-500">{facilities.length} facilities</p>
        <button
          onClick={() => setEditing('new')}
          className="px-3 py-1.5 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 transition-colors"
        >
          + Add Facility
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Name</th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Owner</th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Location</th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Visible</th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody>
            {facilities.map((f) => (
              <tr key={f.id} className="border-t border-gray-100">
                <td className="px-4 py-3 font-medium text-gray-800">{f.name}</td>
                <td className="px-4 py-3 text-gray-600">{f.owner}</td>
                <td className="px-4 py-3 text-gray-500">{f.location.city}, {f.location.country}</td>
                <td className="px-4 py-3">
                  <button
                    onClick={() => handleToggleVisible(f.id, f.visible ?? false)}
                    disabled={pending}
                    className={`inline-block px-2 py-0.5 text-xs rounded-full font-medium cursor-pointer disabled:opacity-50 ${
                      f.visible
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    {f.visible ? 'Visible' : 'Hidden'}
                  </button>
                </td>
                <td className="px-4 py-3 flex gap-3">
                  <button
                    onClick={() => setEditing(f)}
                    className="text-sm text-emerald-700 hover:underline"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(f.id)}
                    disabled={pending}
                    className="text-sm text-red-600 hover:underline disabled:opacity-50"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {editing !== null && (
        <FacilityForm
          facility={editing === 'new' ? null : editing}
          onClose={() => setEditing(null)}
          onSaved={handleSaved}
        />
      )}
    </div>
  )
}
