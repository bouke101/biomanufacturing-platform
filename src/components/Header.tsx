import { createSupabaseServerClient } from '@/lib/supabase/server'
import { signOut } from '@/actions/auth'

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
      <div className="flex-1">
        <h1 className="text-lg font-bold text-gray-900">Biomanufacturing Facility Map</h1>
        <p className="text-xs text-gray-500">Global CMO &amp; CDMO intelligence platform</p>
      </div>
      <div className="flex items-center gap-3">
        {isAdmin && (
          <a
            href="/admin"
            className="text-sm text-emerald-700 hover:underline font-medium"
          >
            Admin
          </a>
        )}
        {user && (
          <form action={signOut}>
            <button
              type="submit"
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Sign out
            </button>
          </form>
        )}
      </div>
    </header>
  )
}
