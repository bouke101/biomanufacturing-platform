import { createSupabaseServerClient } from '@/lib/supabase/server'
import ProfileDropdown from '@/components/ProfileDropdown'

export default async function Header() {
  const supabase = createSupabaseServerClient()
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

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-4 shrink-0">
      <a href="/" className="flex-1 group">
        <h1 className="text-lg font-bold text-gray-900 group-hover:text-emerald-700 transition-colors">
          Biomanufacturing Facility Map
        </h1>
        <p className="text-xs text-gray-500">Global CMO &amp; CDMO intelligence platform</p>
      </a>

      {user && (
        <ProfileDropdown email={user.email ?? ''} isAdmin={isAdmin} />
      )}
    </header>
  )
}
