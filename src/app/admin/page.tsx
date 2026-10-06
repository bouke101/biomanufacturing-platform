// src/app/admin/page.tsx
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import Header from '@/components/Header'
import AdminClient from './AdminClient'
import { fetchColumnVisibility, fetchFacilities } from '@/lib/facilities'

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
  const { data: users } = await admin
    .from('profiles')
    .select('id, email, role, blocked, created_at')
    .order('created_at', { ascending: false })

  const columnVisibility = await fetchColumnVisibility(admin)
  const facilities = await fetchFacilities(admin)

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />
      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Admin Panel</h2>
        <AdminClient users={users ?? []} columnVisibility={columnVisibility} facilities={facilities} />
      </main>
    </div>
  )
}
