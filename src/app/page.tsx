// src/app/page.tsx
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { fetchFacilities, fetchColumnVisibility, fetchColumnFilters } from '@/lib/facilities'
import Header from '@/components/Header'
import FacilityPageClient from '@/components/FacilityPageClient'

export default async function Home() {
  const supabase = createSupabaseServerClient()

  // Determine if the current user is admin
  const { data: { user } } = await supabase.auth.getUser()
  let isAdmin = false
  if (user) {
    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', user.id)
      .single()
    isAdmin = profile?.role === 'admin'
  }

  // Admin client used for settings reads (bypasses RLS so filters are always readable)
  const admin = createSupabaseAdminClient()

  // Content filters apply to everyone on the main page.
  // Admin bypass is only for the visible flag (hidden facilities still show for admins).
  const facilityClient = isAdmin ? admin : supabase
  const [columnFilters, columnVisibility] = await Promise.all([
    fetchColumnFilters(admin),
    fetchColumnVisibility(admin),
  ])
  const facilities = await fetchFacilities(facilityClient, columnFilters)

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header />
      <FacilityPageClient
        initialFacilities={facilities}
        columnVisibility={columnVisibility}
      />
    </div>
  )
}
