'use server'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { redirect } from 'next/navigation'

export async function signIn(formData: FormData) {
  const email    = formData.get('email') as string
  const password = formData.get('password') as string
  const supabase = createSupabaseServerClient()
  const { error } = await supabase.auth.signInWithPassword({ email, password })
  if (error) redirect('/login?error=' + encodeURIComponent(error.message))
  redirect('/')
}

export async function signUp(formData: FormData) {
  const email    = formData.get('email') as string
  const password = formData.get('password') as string
  const confirm  = formData.get('confirmPassword') as string

  if (password !== confirm) {
    redirect('/register?error=' + encodeURIComponent('Passwords do not match'))
  }

  const supabase = createSupabaseServerClient()
  const { data, error } = await supabase.auth.signUp({ email, password })
  if (error) redirect('/register?error=' + encodeURIComponent(error.message))

  const userId = data.user?.id
  if (userId) {
    const orgType      = formData.get('orgType') as string
    const orgTypeOther = formData.get('orgTypeOther') as string
    const firstName    = formData.get('firstName') as string
    const username     = (formData.get('username') as string).trim() || firstName

    await createSupabaseAdminClient().from('profiles').update({
      first_name:   firstName,
      last_name:    formData.get('lastName') as string,
      username,
      job_title:    formData.get('jobTitle') as string,
      company:      formData.get('company') as string,
      org_type:     orgType === 'Other' ? (orgTypeOther || 'Other') : orgType,
      country:      formData.get('country') as string,
      phone:        formData.get('phone') as string,
      mailing_list: false,
    }).eq('id', userId)
  }

  redirect('/')
}

export async function updateProfile(formData: FormData) {
  const supabase = createSupabaseServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const orgType      = formData.get('orgType') as string
  const orgTypeOther = formData.get('orgTypeOther') as string
  const firstName    = formData.get('firstName') as string
  const username     = (formData.get('username') as string).trim() || firstName
  const newEmail     = (formData.get('email') as string).trim()

  // Update profile fields
  const { error: profileError } = await supabase.from('profiles').update({
    first_name:   firstName,
    last_name:    formData.get('lastName') as string,
    username,
    job_title:    formData.get('jobTitle') as string,
    company:      formData.get('company') as string,
    org_type:     orgType === 'Other' ? (orgTypeOther || 'Other') : orgType,
    country:      formData.get('country') as string,
    phone:        formData.get('phone') as string,
    mailing_list: false,
  }).eq('id', user.id)

  if (profileError) redirect('/profile?error=' + encodeURIComponent(profileError.message))

  // Update email if changed — use admin client to skip confirmation
  if (newEmail && newEmail !== user.email) {
    const admin = createSupabaseAdminClient()
    const { error: emailError } = await admin.auth.admin.updateUserById(user.id, { email: newEmail })
    if (emailError) redirect('/profile?error=' + encodeURIComponent('Email update: ' + emailError.message))
    await admin.from('profiles').update({ email: newEmail }).eq('id', user.id)
  }

  redirect('/profile?saved=1')
}

export async function signOut() {
  const supabase = createSupabaseServerClient()
  await supabase.auth.signOut()
  redirect('/login')
}
