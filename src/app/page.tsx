// src/app/page.tsx
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { fetchFacilities, fetchColumnVisibility } from '@/lib/facilities'
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

  // Admin sees all facilities; visitors see only visible=true (enforced by RLS)
  const facilityClient = isAdmin ? createSupabaseAdminClient() : supabase
  const [facilities, columnVisibility] = await Promise.all([
    fetchFacilities(facilityClient),
    fetchColumnVisibility(supabase),
  ])

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
