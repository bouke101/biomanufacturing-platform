import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import Header from '@/components/Header'
import { updateProfile } from '@/actions/auth'
import ProfileFields from '@/components/ProfileFields'

export default async function ProfilePage({
  searchParams,
}: {
  searchParams: { error?: string; saved?: string }
}) {
  const supabase = createSupabaseServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const { data: profile } = await supabase
    .from('profiles')
    .select('email, role, created_at, first_name, last_name, job_title, company, org_type, country, phone, mailing_list')
    .eq('id', user.id)
    .single()

  const initials = ((profile?.first_name?.[0] ?? '') + (profile?.last_name?.[0] ?? '')).toUpperCase()
    || ((profile?.email?.[0]) ?? '?').toUpperCase()

  const displayName = ([profile?.first_name, profile?.last_name].filter(Boolean).join(' '))
    || (profile?.email?.split('@')[0] ?? '')

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />
      <main className="flex-1 flex items-start justify-center px-4 py-10">
        <div className="w-full max-w-lg">

          {/* Avatar + name */}
          <div className="flex items-center gap-4 mb-8">
            <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-2xl font-bold shrink-0">
              {initials}
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">{displayName}</h1>
              <p className="text-sm text-gray-500">{profile?.email}</p>
              <span className="inline-block mt-1 text-xs font-medium px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 capitalize">
                {profile?.role}
              </span>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
            <h2 className="text-base font-semibold text-gray-900 mb-6">Edit profile</h2>

            {searchParams.saved && (
              <div className="mb-6 p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-sm text-emerald-700">
                Profile saved successfully.
              </div>
            )}
            {searchParams.error && (
              <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
                {decodeURIComponent(searchParams.error)}
              </div>
            )}

            <form action={updateProfile}>
              <ProfileFields
                defaults={{
                  firstName:   profile?.first_name ?? '',
                  lastName:    profile?.last_name ?? '',
                  jobTitle:    profile?.job_title ?? '',
                  company:     profile?.company ?? '',
                  orgType:     profile?.org_type ?? '',
                  country:     profile?.country ?? '',
                  phone:       profile?.phone ?? '',
                  mailingList: profile?.mailing_list ?? false,
                }}
              />

              <button
                type="submit"
                className="mt-8 w-full py-2.5 px-4 bg-emerald-600 text-white text-sm font-semibold rounded-lg hover:bg-emerald-700 transition-colors"
              >
                Save changes
              </button>
            </form>

            <div className="mt-6 pt-6 border-t border-gray-100">
              <p className="text-xs text-gray-400">
                Member since{' '}
                {profile?.created_at
                  ? new Date(profile.created_at).toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: 'numeric' })
                  : '—'}
              </p>
            </div>
          </div>

        </div>
      </main>
    </div>
  )
}
