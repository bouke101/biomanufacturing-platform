// src/components/admin/FacilityForm.tsx
'use client'
import { useState, useTransition } from 'react'
import { upsertFacility, type FacilityFormData } from '@/actions/admin'
import type { Facility } from '@/types/facility'

const MODALITY_OPTIONS = [
  'Mammalian cell culture',
  'Microbial fermentation',
  'Fermentation (industrial)',
  'Viral vector',
  'mRNA',
  'ADC',
  'Lipid nanoparticle',
  'Enzymes',
  'Probiotics & cultures',
]
const SCALE_OPTIONS = ['Development', 'Pilot', 'Commercial']
const REGION_OPTIONS = ['Europe', 'North America', 'Asia-Pacific', 'Other']
const TYPE_OPTIONS = ['CMO', 'CDMO', 'Captive', 'Toll']

function parseTagInput(value: string): string[] {
  return value.split(',').map((s) => s.trim()).filter(Boolean)
}

interface FacilityFormProps {
  facility: Facility | null
  onClose: () => void
  onSaved: () => void
}

export default function FacilityForm({ facility, onClose, onSaved }: FacilityFormProps) {
  const isNew = !facility
  const [error, setError] = useState('')
  const [pending, startTransition] = useTransition()

  const [form, setForm] = useState<FacilityFormData>({
    id: facility?.id ?? '',
    name: facility?.name ?? '',
    owner: facility?.owner ?? '',
    city: facility?.location.city ?? '',
    country: facility?.location.country ?? '',
    region: facility?.location.region ?? 'Europe',
    lat: facility?.location.lat ?? 0,
    lng: facility?.location.lng ?? 0,
    facilityType: facility?.facilityType ?? 'CDMO',
    modalities: facility?.modalities ?? [],
    scale: facility?.scale ?? [],
    capacity: facility?.capacity ?? '',
    clients: facility?.clients ?? [],
    products: facility?.products ?? [],
    legacy: facility?.legacy ?? '',
    certifications: facility?.certifications ?? [],
    website: facility?.website ?? '',
    imageUrl: facility?.imageUrl ?? '',
    notes: facility?.notes ?? '',
    visible: facility?.visible ?? false,
  })

  function set<K extends keyof FacilityFormData>(key: K, value: FacilityFormData[K]) {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  function handleSubmit() {
    if (!form.id.trim() || !form.name.trim()) {
      setError('ID and Name are required.')
      return
    }
    setError('')
    startTransition(async () => {
      try {
        await upsertFacility(form)
        onSaved()
        onClose()
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Save failed.')
      }
    })
  }

  const input = 'w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500'
  const label = 'block text-xs font-medium text-gray-600 mb-1'

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-lg font-bold text-gray-900">
            {isNew ? 'Add Facility' : 'Edit Facility'}
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-xl">×</button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={label}>ID (slug, e.g. lonza-visp) *</label>
            <input className={input} value={form.id} onChange={(e) => set('id', e.target.value)} disabled={!isNew} />
          </div>
          <div>
            <label className={label}>Name *</label>
            <input className={input} value={form.name} onChange={(e) => set('name', e.target.value)} />
          </div>
          <div className="col-span-2">
            <label className={label}>Owner</label>
            <input className={input} value={form.owner} onChange={(e) => set('owner', e.target.value)} />
          </div>
          <div>
            <label className={label}>City</label>
            <input className={input} value={form.city} onChange={(e) => set('city', e.target.value)} />
          </div>
          <div>
            <label className={label}>Country</label>
            <input className={input} value={form.country} onChange={(e) => set('country', e.target.value)} />
          </div>
          <div>
            <label className={label}>Latitude</label>
            <input className={input} type="number" step="0.001" value={form.lat} onChange={(e) => set('lat', parseFloat(e.target.value) || 0)} />
          </div>
          <div>
            <label className={label}>Longitude</label>
            <input className={input} type="number" step="0.001" value={form.lng} onChange={(e) => set('lng', parseFloat(e.target.value) || 0)} />
          </div>
          <div>
            <label className={label}>Region</label>
            <select className={input} value={form.region} onChange={(e) => set('region', e.target.value)}>
              {REGION_OPTIONS.map((r) => <option key={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label className={label}>Facility Type</label>
            <select className={input} value={form.facilityType} onChange={(e) => set('facilityType', e.target.value)}>
              {TYPE_OPTIONS.map((t) => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div className="col-span-2">
            <label className={label}>Modalities</label>
            <div className="flex flex-wrap gap-2">
              {MODALITY_OPTIONS.map((m) => (
                <label key={m} className="flex items-center gap-1 text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={form.modalities.includes(m)}
                    onChange={(e) =>
                      set('modalities', e.target.checked
                        ? [...form.modalities, m]
                        : form.modalities.filter((x) => x !== m))
                    }
                    className="accent-emerald-600"
                  />
                  {m}
                </label>
              ))}
            </div>
          </div>
          <div>
            <label className={label}>Scale</label>
            <div className="flex gap-4">
              {SCALE_OPTIONS.map((s) => (
                <label key={s} className="flex items-center gap-1 text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={form.scale.includes(s)}
                    onChange={(e) =>
                      set('scale', e.target.checked
                        ? [...form.scale, s]
                        : form.scale.filter((x) => x !== s))
                    }
                    className="accent-emerald-600"
                  />
                  {s}
                </label>
              ))}
            </div>
          </div>
          <div>
            <label className={label}>Capacity</label>
            <input className={input} value={form.capacity} onChange={(e) => set('capacity', e.target.value)} />
          </div>
          <div>
            <label className={label}>Products (comma-separated)</label>
            <input className={input} value={form.products.join(', ')} onChange={(e) => set('products', parseTagInput(e.target.value))} />
          </div>
          <div>
            <label className={label}>Clients (comma-separated)</label>
            <input className={input} value={form.clients.join(', ')} onChange={(e) => set('clients', parseTagInput(e.target.value))} />
          </div>
          <div className="col-span-2">
            <label className={label}>Legacy / History</label>
            <textarea className={input} rows={2} value={form.legacy} onChange={(e) => set('legacy', e.target.value)} />
          </div>
          <div>
            <label className={label}>Certifications (comma-separated)</label>
            <input className={input} value={form.certifications.join(', ')} onChange={(e) => set('certifications', parseTagInput(e.target.value))} />
          </div>
          <div>
            <label className={label}>Website</label>
            <input className={input} value={form.website} onChange={(e) => set('website', e.target.value)} />
          </div>
          <div className="col-span-2">
            <label className={label}>Notes</label>
            <textarea className={input} rows={2} value={form.notes} onChange={(e) => set('notes', e.target.value)} />
          </div>
          <div className="col-span-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={form.visible}
                onChange={(e) => set('visible', e.target.checked)}
                className="w-4 h-4 accent-emerald-600"
              />
              <span className="text-sm font-medium text-gray-700">Visible to visitors</span>
            </label>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={handleSubmit}
            disabled={pending}
            className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 disabled:opacity-50 transition-colors"
          >
            {pending ? 'Saving…' : 'Save'}
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}
