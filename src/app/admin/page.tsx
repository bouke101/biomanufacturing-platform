// src/app/admin/page.tsx
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import Header from '@/components/Header'
import AdminClient from './AdminClient'
import { fetchColumnVisibility, fetchColumnFilters, fetchFacilities } from '@/lib/facilities'

export default async function AdminPage() {
  const supabase = createSupabaseServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()
  if (profile?.role !== 'admin') redirect('/')

  const admin = createSupabaseAdminClient()
  const [{ data: users }, columnVisibility, columnFilters, facilities] = await Promise.all([
    admin.from('profiles').select('id, email, role, blocked, created_at').order('created_at', { ascending: false }),
    fetchColumnVisibility(admin),
    fetchColumnFilters(admin),
    fetchFacilities(admin),
  ])

  const allFilterValues = {
    regions:       [...new Set(facilities.map((f) => f.location.region).filter(Boolean))].sort() as string[],
    facilityTypes: [...new Set(facilities.map((f) => f.facilityType).filter(Boolean))].sort() as string[],
    countries:     [...new Set(facilities.map((f) => f.location.country).filter(Boolean))].sort() as string[],
    sources:       [...new Set(facilities.map((f) => f.source ?? '').filter(Boolean))].sort() as string[],
    modalities:    [...new Set(facilities.flatMap((f) => f.modalities).filter(Boolean))].sort() as string[],
  }

  const valueCounts: Record<string, Record<string, number>> = {
    region: {}, facilityType: {}, country: {}, source: {}, modality: {},
  }
  for (const f of facilities) {
    if (f.location.region)  valueCounts.region[f.location.region]       = (valueCounts.region[f.location.region]       ?? 0) + 1
    if (f.facilityType)     valueCounts.facilityType[f.facilityType]     = (valueCounts.facilityType[f.facilityType]     ?? 0) + 1
    if (f.location.country) valueCounts.country[f.location.country]      = (valueCounts.country[f.location.country]      ?? 0) + 1
    if (f.source)           valueCounts.source[f.source]                 = (valueCounts.source[f.source]                 ?? 0) + 1
    for (const m of f.modalities) valueCounts.modality[m]               = (valueCounts.modality[m]                      ?? 0) + 1
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />
      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Admin Panel</h2>
        <AdminClient
          users={users ?? []}
          columnVisibility={columnVisibility}
          columnFilters={columnFilters}
          allFilterValues={allFilterValues}
          valueCounts={valueCounts}
          totalFacilities={facilities.length}
          facilities={facilities}
        />
      </main>
    </div>
  )
}
