# Auth & Admin Panel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Supabase-powered email/password auth (all routes protected), migrate facility data from JSON to Supabase PostgreSQL, and build an admin panel for managing users, column visibility, and facility records.

**Architecture:** Next.js middleware guards every route except `/login` and `/register`; Supabase PostgreSQL replaces `data/facilities.json` and stores `profiles` (users + roles) and `settings` (column visibility); the main `page.tsx` becomes a server component that fetches facilities + settings and passes them to a client wrapper; admin operations (CRUD, block user) use a service-role Supabase client inside server actions that bypass RLS.

**Tech Stack:** Next.js 14 App Router · Supabase (Auth + PostgreSQL) · `@supabase/ssr` · `@supabase/supabase-js` · TypeScript · Tailwind CSS

**Spec:** `docs/superpowers/specs/2026-10-05-auth-admin-design.md`

## Global Constraints

- Next.js 14 App Router (`src/app/`) — no Pages Router
- TypeScript strict mode — no `any` except where Leaflet requires it
- Tailwind CSS only — no inline `style=` except inside Leaflet div-icons
- Use `@supabase/ssr` (NOT deprecated `@supabase/auth-helpers-nextjs`) for Next.js 14 session handling
- Admin email: `b.w.dejong@hotmail.com` — set in `profiles.role = 'admin'` via seed SQL
- No password reset, no email verification for MVP
- Column visibility is global (admin-controlled, applies to all visitors)
- All 20 existing facilities seeded with `visible = true`
- Existing `FacilityTable`, `FacilityMap`, `FilterBar` component internals unchanged — only props added

---

## File Map

```
src/
  lib/
    supabase/
      client.ts              ← NEW — createBrowserClient wrapper
      server.ts              ← NEW — createServerClient wrapper (reads cookies)
      admin.ts               ← NEW — service-role client (bypasses RLS)
    facilities.ts            ← MODIFY — add fetchFacilities(), fetchColumnVisibility()
  middleware.ts              ← NEW — auth guard, blocked check, admin route guard
  actions/
    auth.ts                  ← NEW — signIn, signUp, signOut server actions
    admin.ts                 ← NEW — blockUser, updateColumnVisibility, upsertFacility, deleteFacility
  app/
    layout.tsx               ← MODIFY — add <Header />
    page.tsx                 ← MODIFY — server component; fetches data, renders <FacilityPageClient />
    login/
      page.tsx               ← NEW
    register/
      page.tsx               ← NEW
    admin/
      page.tsx               ← NEW — server component; role guard; fetches users + settings + facilities
      AdminClient.tsx        ← NEW — 'use client'; three-tab shell
  components/
    Header.tsx               ← NEW — logo + sign-out button + admin link
    FacilityPageClient.tsx   ← NEW — 'use client'; holds filter state; renders FilterBar+Table+Map
    FacilityTable/
      FacilityTable.tsx      ← MODIFY — accept columnVisibility prop; filter columns
      columns.tsx            ← MODIFY — add explicit id to every column definition
    admin/
      UsersTab.tsx           ← NEW
      ColumnVisibilityTab.tsx ← NEW
      FacilitiesTab.tsx      ← NEW
      FacilityForm.tsx       ← NEW
  hooks/
    useFacilityFilters.ts    ← MODIFY — accept initialFacilities param; remove loadFacilities() call
.env.local.example           ← NEW
scripts/
  seed-facilities.ts         ← NEW — reads data/facilities.json; upserts to Supabase
```

---

## Task 1: Supabase project setup + client files + middleware + env template

**Files:**
- Create: `src/lib/supabase/client.ts`
- Create: `src/lib/supabase/server.ts`
- Create: `src/lib/supabase/admin.ts`
- Create: `src/middleware.ts`
- Create: `.env.local.example`

**Interfaces:**
- Produces: `createSupabaseBrowserClient()` → Supabase browser client
- Produces: `createSupabaseServerClient()` → Supabase server client (reads/writes session cookies)
- Produces: `createSupabaseAdminClient()` → Supabase admin client (service role, bypasses RLS)
- Produces: middleware that redirects unauthenticated users to `/login`, blocked users to `/login?suspended=1`, and non-admins away from `/admin`

- [ ] **Step 1: Create a Supabase project**

Go to https://supabase.com → New project. Note the project URL and anon key from **Settings → API**. Also copy the **service role key** (keep this secret — never expose it client-side).

- [ ] **Step 2: Install packages**

```bash
cd /Users/bouke/Library/CloudStorage/OneDrive-Personal/claude/projects/biomanufacturing
npm install @supabase/supabase-js @supabase/ssr
```

- [ ] **Step 3: Create `.env.local.example`**

```bash
# .env.local.example
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

Copy to `.env.local` and fill in the real values from the Supabase dashboard.

- [ ] **Step 4: Create `src/lib/supabase/client.ts`**

```typescript
// src/lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createSupabaseBrowserClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

- [ ] **Step 5: Create `src/lib/supabase/server.ts`**

```typescript
// src/lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createSupabaseServerClient() {
  const cookieStore = cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // setAll called from a Server Component; cookies can only be set from Server Actions or Route Handlers
          }
        },
      },
    }
  )
}
```

- [ ] **Step 6: Create `src/lib/supabase/admin.ts`**

```typescript
// src/lib/supabase/admin.ts
import { createClient } from '@supabase/supabase-js'

export function createSupabaseAdminClient() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    }
  )
}
```

- [ ] **Step 7: Create `src/middleware.ts`**

```typescript
// src/middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  const {
    data: { user },
  } = await supabase.auth.getUser()

  const pathname = request.nextUrl.pathname
  const isPublicRoute = pathname === '/login' || pathname === '/register'

  if (!user && !isPublicRoute) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  if (user) {
    const { data: profile } = await supabase
      .from('profiles')
      .select('role, blocked')
      .eq('id', user.id)
      .single()

    if (profile?.blocked) {
      const response = NextResponse.redirect(
        new URL('/login?suspended=1', request.url)
      )
      // Expire the session cookie so the user is fully signed out
      response.cookies.set('sb-access-token', '', { maxAge: 0 })
      response.cookies.set('sb-refresh-token', '', { maxAge: 0 })
      return response
    }

    if (pathname.startsWith('/admin') && profile?.role !== 'admin') {
      return NextResponse.redirect(new URL('/', request.url))
    }
  }

  return supabaseResponse
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

- [ ] **Step 8: TypeScript check**

```bash
npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 9: Commit**

```bash
git add src/lib/supabase/ src/middleware.ts .env.local.example package.json package-lock.json
git commit -m "feat: add Supabase client files, middleware auth guard, and env template"
```

---

## Task 2: Database schema + RLS + seed

**Files:**
- Create: `scripts/seed-facilities.ts`

**Interfaces:**
- Produces: `profiles`, `facilities`, `settings` tables in Supabase with RLS
- Produces: 20 facilities seeded into `facilities` table with `visible = true`
- Produces: `column_visibility` seed row in `settings` table
- Produces: admin profile for `b.w.dejong@hotmail.com`

- [ ] **Step 1: Run schema SQL in Supabase SQL editor**

Go to your Supabase dashboard → **SQL Editor** → New query. Paste and run the following:

```sql
-- profiles table
create table public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  email text not null,
  role text not null default 'user' check (role in ('admin', 'user')),
  blocked boolean not null default false,
  created_at timestamptz not null default now()
);

-- facilities table
create table public.facilities (
  id text primary key,
  name text not null,
  owner text not null,
  city text not null,
  country text not null,
  region text not null,
  lat float8 not null,
  lng float8 not null,
  facility_type text not null,
  modalities text[] not null default '{}',
  scale text[] not null default '{}',
  capacity text not null default '',
  clients text[] not null default '{}',
  products text[] not null default '{}',
  legacy text not null default '',
  certifications text[] not null default '{}',
  website text not null default '',
  image_url text not null default '',
  notes text not null default '',
  visible boolean not null default false,
  created_at timestamptz not null default now()
);

-- settings table
create table public.settings (
  key text primary key,
  value jsonb not null
);

-- Enable RLS
alter table public.profiles enable row level security;
alter table public.facilities enable row level security;
alter table public.settings enable row level security;

-- RLS: profiles — users see only their own row; admin client bypasses via service role
create policy "Users read own profile"
  on public.profiles for select
  using (auth.uid() = id);

-- RLS: facilities — authenticated users see visible=true; admin client bypasses via service role
create policy "Visitors see visible facilities"
  on public.facilities for select
  to authenticated
  using (visible = true);

-- RLS: settings — all authenticated users can read
create policy "Authenticated users read settings"
  on public.settings for select
  to authenticated
  using (true);

-- Trigger: auto-create profile on signup
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email, role, blocked)
  values (new.id, new.email, 'user', false)
  on conflict (id) do nothing;
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Seed: default column visibility (all visible)
insert into public.settings (key, value) values (
  'column_visibility',
  '{"name": true, "owner": true, "location": true, "facilityType": true, "modalities": true, "region": true}'::jsonb
);
```

- [ ] **Step 2: Create `scripts/seed-facilities.ts`**

```typescript
// scripts/seed-facilities.ts
import { createClient } from '@supabase/supabase-js'
import facilityData from '../data/facilities.json'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

async function seed() {
  const rows = (facilityData as any[]).map((f) => ({
    id: f.id,
    name: f.name,
    owner: f.owner,
    city: f.location.city,
    country: f.location.country,
    region: f.location.region,
    lat: f.location.lat,
    lng: f.location.lng,
    facility_type: f.facilityType,
    modalities: f.modalities,
    scale: f.scale,
    capacity: f.capacity,
    clients: f.clients,
    products: f.products,
    legacy: f.legacy,
    certifications: f.certifications,
    website: f.website,
    image_url: f.imageUrl,
    notes: f.notes,
    visible: true,
  }))

  const { error } = await supabase.from('facilities').upsert(rows)
  if (error) {
    console.error('Seed failed:', error.message)
    process.exit(1)
  }
  console.log(`Seeded ${rows.length} facilities.`)
}

seed()
```

- [ ] **Step 3: Run the seed script**

```bash
npx tsx scripts/seed-facilities.ts
```

Expected: `Seeded 20 facilities.`

If `tsx` is not installed: `npm install -D tsx` first.

- [ ] **Step 4: Set admin role for your account**

After registering at `/register` with `b.w.dejong@hotmail.com` (do this after Task 3), run in Supabase SQL editor:

```sql
update public.profiles
set role = 'admin'
where email = 'b.w.dejong@hotmail.com';
```

(This step is documented here but runs after Task 3 creates the account.)

- [ ] **Step 5: Verify in Supabase table editor**

Open **Table Editor → facilities**. Confirm 20 rows with `visible = true`. Open **settings** — confirm `column_visibility` row.

- [ ] **Step 6: Commit**

```bash
git add scripts/seed-facilities.ts
git commit -m "feat: add database schema SQL and facility seed script"
```

---

## Task 3: Auth server actions + login/register pages + Header

**Files:**
- Create: `src/actions/auth.ts`
- Create: `src/app/login/page.tsx`
- Create: `src/app/register/page.tsx`
- Create: `src/components/Header.tsx`
- Modify: `src/app/layout.tsx`

**Interfaces:**
- Produces: `signIn(formData)`, `signUp(formData)`, `signOut()` server actions
- Produces: `/login` and `/register` pages using those actions
- Produces: `<Header />` component with sign-out + conditional admin link
- Consumes: `createSupabaseServerClient()` from `@/lib/supabase/server`

- [ ] **Step 1: Create `src/actions/auth.ts`**

```typescript
// src/actions/auth.ts
'use server'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function signIn(formData: FormData) {
  const email = formData.get('email') as string
  const password = formData.get('password') as string
  const supabase = createSupabaseServerClient()

  const { error } = await supabase.auth.signInWithPassword({ email, password })
  if (error) {
    redirect('/login?error=' + encodeURIComponent(error.message))
  }
  redirect('/')
}

export async function signUp(formData: FormData) {
  const email = formData.get('email') as string
  const password = formData.get('password') as string
  const supabase = createSupabaseServerClient()

  const { error } = await supabase.auth.signUp({ email, password })
  if (error) {
    redirect('/register?error=' + encodeURIComponent(error.message))
  }
  redirect('/')
}

export async function signOut() {
  const supabase = createSupabaseServerClient()
  await supabase.auth.signOut()
  redirect('/login')
}
```

- [ ] **Step 2: Create `src/app/login/page.tsx`**

```tsx
// src/app/login/page.tsx
import { signIn } from '@/actions/auth'

export default function LoginPage({
  searchParams,
}: {
  searchParams: { error?: string; suspended?: string }
}) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <h1 className="text-xl font-bold text-gray-900 mb-1">Sign in</h1>
        <p className="text-sm text-gray-500 mb-6">Biomanufacturing Facility Map</p>

        {searchParams.suspended && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
            Your account has been suspended. Contact the administrator.
          </div>
        )}
        {searchParams.error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
            {decodeURIComponent(searchParams.error)}
          </div>
        )}

        <form action={signIn} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              name="email"
              type="email"
              required
              autoComplete="email"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              name="password"
              type="password"
              required
              autoComplete="current-password"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 transition-colors"
          >
            Sign in
          </button>
        </form>

        <p className="mt-4 text-sm text-center text-gray-500">
          No account?{' '}
          <a href="/register" className="text-emerald-700 hover:underline font-medium">
            Register
          </a>
        </p>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Create `src/app/register/page.tsx`**

```tsx
// src/app/register/page.tsx
import { signUp } from '@/actions/auth'

export default function RegisterPage({
  searchParams,
}: {
  searchParams: { error?: string }
}) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <h1 className="text-xl font-bold text-gray-900 mb-1">Create account</h1>
        <p className="text-sm text-gray-500 mb-6">Biomanufacturing Facility Map</p>

        {searchParams.error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
            {decodeURIComponent(searchParams.error)}
          </div>
        )}

        <form action={signUp} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              name="email"
              type="email"
              required
              autoComplete="email"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              name="password"
              type="password"
              required
              minLength={6}
              autoComplete="new-password"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 transition-colors"
          >
            Create account
          </button>
        </form>

        <p className="mt-4 text-sm text-center text-gray-500">
          Already have an account?{' '}
          <a href="/login" className="text-emerald-700 hover:underline font-medium">
            Sign in
          </a>
        </p>
      </div>
    </div>
  )
}
```

- [ ] **Step 4: Create `src/components/Header.tsx`**

```tsx
// src/components/Header.tsx
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
```

- [ ] **Step 5: Modify `src/app/layout.tsx`**

Replace the entire file:

```tsx
// src/app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Biomanufacturing Facility Map',
  description: 'Global overview of biomanufacturing and CMO/CDMO facilities',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

Note: `<Header />` is NOT added to `layout.tsx` — it is rendered inside each page that needs it (`page.tsx` and `/admin/page.tsx`). This keeps login/register pages header-free.

- [ ] **Step 6: Build check**

```bash
npm run build
```

Expected: build succeeds. Warnings about Supabase cookie setting from server components are acceptable.

- [ ] **Step 7: Manual smoke test**

```bash
npm run dev
```

- Visit `http://localhost:3000` → should redirect to `/login`
- Register with any email + password → should land on `/` (which currently still loads from JSON — that's fine)
- Sign out → should redirect to `/login`
- Sign in again → lands on `/`

- [ ] **Step 8: Commit**

```bash
git add src/actions/auth.ts src/app/login/ src/app/register/ src/components/Header.tsx src/app/layout.tsx
git commit -m "feat: add auth server actions, login/register pages, and Header with sign-out"
```

---

## Task 4: Switch main page to Supabase data source

**Files:**
- Modify: `src/lib/facilities.ts`
- Modify: `src/hooks/useFacilityFilters.ts`
- Modify: `src/components/FacilityTable/columns.tsx`
- Modify: `src/components/FacilityTable/FacilityTable.tsx`
- Create: `src/components/FacilityPageClient.tsx`
- Modify: `src/app/page.tsx`

**Interfaces:**
- Produces: `fetchFacilities(supabase): Promise<Facility[]>` — fetches from Supabase
- Produces: `fetchColumnVisibility(supabase): Promise<Record<string, boolean>>` — fetches from `settings`
- Consumes: `createSupabaseServerClient()` in `page.tsx`
- Produces: `<FacilityPageClient initialFacilities={…} columnVisibility={…} />` — client wrapper

- [ ] **Step 1: Add Supabase fetchers to `src/lib/facilities.ts`**

Replace the entire file:

```typescript
// src/lib/facilities.ts
import type { SupabaseClient } from '@supabase/supabase-js'
import type { Facility, Modality, FacilityType } from '@/types/facility'

export interface FilterOptions {
  modalities: Modality[]
  regions: string[]
  facilityTypes: FacilityType[]
}

export function getFilterOptions(facilities: Facility[]): FilterOptions {
  return {
    modalities: [...new Set(facilities.flatMap((f) => f.modalities))].sort() as Modality[],
    regions: [...new Set(facilities.map((f) => f.location.region))].sort(),
    facilityTypes: [...new Set(facilities.map((f) => f.facilityType))].sort() as FacilityType[],
  }
}

export async function fetchFacilities(supabase: SupabaseClient): Promise<Facility[]> {
  const { data, error } = await supabase
    .from('facilities')
    .select('*')
    .order('name')
  if (error) throw new Error(error.message)
  return (data ?? []).map((row) => ({
    id: row.id,
    name: row.name,
    owner: row.owner,
    location: {
      city: row.city,
      country: row.country,
      region: row.region as Facility['location']['region'],
      lat: row.lat,
      lng: row.lng,
    },
    facilityType: row.facility_type as Facility['facilityType'],
    modalities: row.modalities as Facility['modalities'],
    scale: row.scale as Facility['scale'],
    capacity: row.capacity,
    clients: row.clients,
    products: row.products,
    legacy: row.legacy,
    certifications: row.certifications,
    website: row.website,
    imageUrl: row.image_url,
    notes: row.notes,
    visible: row.visible,
  }))
}

export async function fetchColumnVisibility(
  supabase: SupabaseClient
): Promise<Record<string, boolean>> {
  const { data } = await supabase
    .from('settings')
    .select('value')
    .eq('key', 'column_visibility')
    .single()
  return (data?.value as Record<string, boolean>) ?? {
    name: true,
    owner: true,
    location: true,
    facilityType: true,
    modalities: true,
    region: true,
  }
}
```

- [ ] **Step 2: Modify `src/hooks/useFacilityFilters.ts`**

Replace the entire file:

```typescript
// src/hooks/useFacilityFilters.ts
'use client'
import { useState, useMemo } from 'react'
import type { Facility, Modality, FacilityType } from '@/types/facility'

export function useFacilityFilters(initialFacilities: Facility[]) {
  const [globalSearch, setGlobalSearch] = useState('')
  const [modality, setModality] = useState<Modality | ''>('')
  const [region, setRegion] = useState<string>('')
  const [facilityType, setFacilityType] = useState<FacilityType | ''>('')
  const [selectedId, setSelectedId] = useState<string | null>(null)

  const filtered = useMemo(() => {
    const q = globalSearch.toLowerCase()
    return initialFacilities.filter((f) => {
      const matchesSearch =
        !q ||
        f.name.toLowerCase().includes(q) ||
        f.owner.toLowerCase().includes(q) ||
        f.location.city.toLowerCase().includes(q) ||
        f.location.country.toLowerCase().includes(q) ||
        f.products.some((p) => p.toLowerCase().includes(q)) ||
        f.modalities.some((m) => m.toLowerCase().includes(q))
      const matchesModality = !modality || f.modalities.includes(modality)
      const matchesRegion = !region || f.location.region === region
      const matchesType = !facilityType || f.facilityType === facilityType
      return matchesSearch && matchesModality && matchesRegion && matchesType
    })
  }, [initialFacilities, globalSearch, modality, region, facilityType])

  return {
    facilities: initialFacilities,
    filtered,
    globalSearch, setGlobalSearch,
    modality, setModality,
    region, setRegion,
    facilityType, setFacilityType,
    selectedId, setSelectedId,
  }
}
```

- [ ] **Step 3: Modify `src/components/FacilityTable/columns.tsx`** — add explicit `id` to every column

Replace the entire file:

```tsx
// src/components/FacilityTable/columns.tsx
import { createColumnHelper, tableFeatures, rowSortingFeature, createSortedRowModel } from '@tanstack/react-table'
import type { Facility } from '@/types/facility'

export const features = tableFeatures({
  rowSortingFeature,
  sortedRowModel: createSortedRowModel(),
})

const helper = createColumnHelper<typeof features, Facility>()

export const allColumns = helper.columns([
  helper.accessor('name', {
    id: 'name',
    header: 'Facility',
    cell: (info) => <span className="font-medium text-gray-900">{info.getValue()}</span>,
  }),
  helper.accessor('owner', {
    id: 'owner',
    header: 'Owner',
    cell: (info) => <span className="text-gray-700">{info.getValue()}</span>,
  }),
  helper.accessor((row) => row.location.city + ', ' + row.location.country, {
    id: 'location',
    header: 'Location',
    cell: (info) => <span className="text-gray-600">{info.getValue()}</span>,
  }),
  helper.accessor('facilityType', {
    id: 'facilityType',
    header: 'Type',
    cell: (info) => (
      <span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800">
        {info.getValue()}
      </span>
    ),
  }),
  helper.accessor((row) => row.modalities.join(', '), {
    id: 'modalities',
    header: 'Modalities',
    cell: (info) => <span className="text-sm text-gray-600">{info.getValue()}</span>,
  }),
  helper.accessor((row) => row.location.region, {
    id: 'region',
    header: 'Region',
    cell: (info) => <span className="text-gray-600">{info.getValue()}</span>,
  }),
])
```

Note: renamed `columns` → `allColumns` to make filtering by visibility explicit.

- [ ] **Step 4: Modify `src/components/FacilityTable/FacilityTable.tsx`** — accept `columnVisibility` prop

Replace the entire file:

```tsx
// src/components/FacilityTable/FacilityTable.tsx
'use client'
import React, { useState } from 'react'
import {
  useTable,
  flexRender,
  type SortingState,
} from '@tanstack/react-table'
import { allColumns, features } from './columns'
import FacilityDetail from './FacilityDetail'
import type { Facility } from '@/types/facility'

interface FacilityTableProps {
  filtered: Facility[]
  selectedId: string | null
  setSelectedId: (id: string | null) => void
  columnVisibility: Record<string, boolean>
}

export default function FacilityTable({
  filtered,
  selectedId,
  setSelectedId,
  columnVisibility,
}: FacilityTableProps) {
  const [sorting, setSorting] = useState<SortingState>([])

  const columns = allColumns.filter(
    (col) => columnVisibility[(col as { id?: string }).id ?? ''] !== false
  )

  const table = useTable({
    features,
    data: filtered,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getRowId: (row) => row.id,
  })

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead className="bg-gray-100 sticky top-0 z-10">
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wide cursor-pointer select-none hover:bg-gray-200"
                  onClick={header.column.getToggleSortingHandler()}
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                  {header.column.getIsSorted() === 'asc' ? ' ↑' : header.column.getIsSorted() === 'desc' ? ' ↓' : ''}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => {
            const isSelected = row.id === selectedId
            const facility = row.original
            return (
              <React.Fragment key={row.id}>
                <tr
                  onClick={() => setSelectedId(isSelected ? null : row.id)}
                  className={`border-b border-gray-100 cursor-pointer transition-colors
                    ${isSelected ? 'bg-emerald-50' : 'hover:bg-gray-50'}`}
                >
                  {row.getAllCells().map((cell) => (
                    <td key={cell.id} className="px-4 py-3">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
                {isSelected && (
                  <tr>
                    <td colSpan={columns.length}>
                      <FacilityDetail facility={facility} />
                    </td>
                  </tr>
                )}
              </React.Fragment>
            )
          })}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="px-4 py-8 text-center text-gray-400">
                No facilities match the current filters.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
```

- [ ] **Step 5: Create `src/components/FacilityPageClient.tsx`**

```tsx
// src/components/FacilityPageClient.tsx
'use client'
import { useFacilityFilters } from '@/hooks/useFacilityFilters'
import { getFilterOptions } from '@/lib/facilities'
import FilterBar from '@/components/FilterBar'
import FacilityTable from '@/components/FacilityTable/FacilityTable'
import FacilityMap from '@/components/FacilityMap'
import type { Facility } from '@/types/facility'

interface FacilityPageClientProps {
  initialFacilities: Facility[]
  columnVisibility: Record<string, boolean>
}

export default function FacilityPageClient({
  initialFacilities,
  columnVisibility,
}: FacilityPageClientProps) {
  const filters = useFacilityFilters(initialFacilities)

  return (
    <>
      <FilterBar
        facilities={filters.facilities}
        globalSearch={filters.globalSearch}
        setGlobalSearch={filters.setGlobalSearch}
        modality={filters.modality}
        setModality={filters.setModality}
        region={filters.region}
        setRegion={filters.setRegion}
        facilityType={filters.facilityType}
        setFacilityType={filters.setFacilityType}
        resultCount={filters.filtered.length}
      />
      <div className="flex flex-col flex-1 overflow-hidden">
        <div className="h-[40vh] shrink-0 border-b border-gray-200">
          <FacilityMap
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
          />
        </div>
        <div className="flex-1 overflow-auto">
          <FacilityTable
            filtered={filters.filtered}
            selectedId={filters.selectedId}
            setSelectedId={filters.setSelectedId}
            columnVisibility={columnVisibility}
          />
        </div>
      </div>
    </>
  )
}
```

- [ ] **Step 6: Rewrite `src/app/page.tsx` as a server component**

Replace the entire file:

```tsx
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
```

- [ ] **Step 7: Build check**

```bash
npm run build
```

Expected: build succeeds. Verify in browser (`npm run dev`):
- Visit `http://localhost:3000` after signing in → facilities load from Supabase (same 20 facilities)
- Header shows "Admin" link if signed in as `b.w.dejong@hotmail.com` (after Task 2 Step 4)

- [ ] **Step 8: Commit**

```bash
git add src/lib/facilities.ts src/hooks/useFacilityFilters.ts src/components/FacilityTable/columns.tsx src/components/FacilityTable/FacilityTable.tsx src/components/FacilityPageClient.tsx src/app/page.tsx
git commit -m "feat: switch main page to Supabase data source with column visibility support"
```

---

## Task 5: Admin panel shell + Users tab

**Files:**
- Create: `src/app/admin/page.tsx`
- Create: `src/app/admin/AdminClient.tsx`
- Create: `src/components/admin/UsersTab.tsx`
- Modify: `src/actions/admin.ts` (create file with `blockUser`)

**Interfaces:**
- Produces: `/admin` route (server component) that fetches all users and passes to `AdminClient`
- Produces: `<AdminClient users={…} />` with tab state
- Produces: `<UsersTab users={…} />` with block/unblock toggle
- Produces: `blockUser(userId, blocked)` server action

- [ ] **Step 1: Create `src/actions/admin.ts`** (initial version — Users only)

```typescript
// src/actions/admin.ts
'use server'
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import type { Facility } from '@/types/facility'

async function requireAdmin() {
  const supabase = createSupabaseServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()
  if (profile?.role !== 'admin') redirect('/')
}

export async function blockUser(userId: string, blocked: boolean) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin
    .from('profiles')
    .update({ blocked })
    .eq('id', userId)
  if (error) throw new Error(error.message)
}
```

- [ ] **Step 2: Create `src/app/admin/page.tsx`**

```tsx
// src/app/admin/page.tsx
import { createSupabaseAdminClient } from '@/lib/supabase/admin'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import Header from '@/components/Header'
import AdminClient from './AdminClient'

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

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />
      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Admin Panel</h2>
        <AdminClient users={users ?? []} />
      </main>
    </div>
  )
}
```

- [ ] **Step 3: Create `src/app/admin/AdminClient.tsx`**

```tsx
// src/app/admin/AdminClient.tsx
'use client'
import { useState } from 'react'
import UsersTab from '@/components/admin/UsersTab'

type Tab = 'users' | 'columns' | 'facilities'

interface Profile {
  id: string
  email: string
  role: string
  blocked: boolean
  created_at: string
}

interface AdminClientProps {
  users: Profile[]
}

export default function AdminClient({ users }: AdminClientProps) {
  const [activeTab, setActiveTab] = useState<Tab>('users')

  const tabClass = (tab: Tab) =>
    `px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
      activeTab === tab
        ? 'border-emerald-600 text-emerald-700'
        : 'border-transparent text-gray-500 hover:text-gray-700'
    }`

  return (
    <div>
      <div className="flex border-b border-gray-200 mb-6">
        <button className={tabClass('users')} onClick={() => setActiveTab('users')}>
          Users
        </button>
        <button className={tabClass('columns')} onClick={() => setActiveTab('columns')}>
          Column Visibility
        </button>
        <button className={tabClass('facilities')} onClick={() => setActiveTab('facilities')}>
          Facilities
        </button>
      </div>

      {activeTab === 'users' && <UsersTab users={users} />}
      {activeTab === 'columns' && (
        <p className="text-gray-400 text-sm">Column visibility — coming in next task.</p>
      )}
      {activeTab === 'facilities' && (
        <p className="text-gray-400 text-sm">Facilities — coming in next task.</p>
      )}
    </div>
  )
}
```

- [ ] **Step 4: Create `src/components/admin/UsersTab.tsx`**

```tsx
// src/components/admin/UsersTab.tsx
'use client'
import { useTransition } from 'react'
import { blockUser } from '@/actions/admin'

interface Profile {
  id: string
  email: string
  role: string
  blocked: boolean
  created_at: string
}

export default function UsersTab({ users }: { users: Profile[] }) {
  const [pending, startTransition] = useTransition()

  function toggle(userId: string, currentlyBlocked: boolean) {
    startTransition(async () => {
      await blockUser(userId, !currentlyBlocked)
      // Refresh the page to reflect the new state
      window.location.reload()
    })
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Email</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Role</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Registered</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Status</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id} className="border-t border-gray-100">
              <td className="px-4 py-3 text-gray-800">{u.email}</td>
              <td className="px-4 py-3">
                <span className={`inline-block px-2 py-0.5 text-xs rounded-full font-medium ${
                  u.role === 'admin'
                    ? 'bg-emerald-100 text-emerald-800'
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  {u.role}
                </span>
              </td>
              <td className="px-4 py-3 text-gray-500">
                {new Date(u.created_at).toLocaleDateString()}
              </td>
              <td className="px-4 py-3">
                <span className={`inline-block px-2 py-0.5 text-xs rounded-full font-medium ${
                  u.blocked
                    ? 'bg-red-100 text-red-700'
                    : 'bg-green-100 text-green-700'
                }`}>
                  {u.blocked ? 'Blocked' : 'Active'}
                </span>
              </td>
              <td className="px-4 py-3">
                {u.role !== 'admin' && (
                  <button
                    onClick={() => toggle(u.id, u.blocked)}
                    disabled={pending}
                    className={`text-sm font-medium ${
                      u.blocked
                        ? 'text-emerald-700 hover:underline'
                        : 'text-red-600 hover:underline'
                    } disabled:opacity-50`}
                  >
                    {u.blocked ? 'Unblock' : 'Block'}
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

- [ ] **Step 5: Build check**

```bash
npm run build
```

- [ ] **Step 6: Manual test**

Sign in as admin, navigate to `/admin`. Verify Users tab shows registered users with Block/Unblock buttons.

- [ ] **Step 7: Commit**

```bash
git add src/actions/admin.ts src/app/admin/ src/components/admin/UsersTab.tsx
git commit -m "feat: add admin panel shell and Users tab with block/unblock"
```

---

## Task 6: Admin Column Visibility tab

**Files:**
- Modify: `src/actions/admin.ts` — add `updateColumnVisibility`
- Create: `src/components/admin/ColumnVisibilityTab.tsx`
- Modify: `src/app/admin/page.tsx` — fetch column visibility; pass to `AdminClient`
- Modify: `src/app/admin/AdminClient.tsx` — wire `ColumnVisibilityTab`

**Interfaces:**
- Produces: `updateColumnVisibility(visibility: Record<string, boolean>)` server action
- Produces: `<ColumnVisibilityTab columnVisibility={…} />` — toggles + save button

- [ ] **Step 1: Add `updateColumnVisibility` to `src/actions/admin.ts`**

Append to the existing file (after the `blockUser` export):

```typescript
export async function updateColumnVisibility(visibility: Record<string, boolean>) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin
    .from('settings')
    .upsert({ key: 'column_visibility', value: visibility })
  if (error) throw new Error(error.message)
}
```

- [ ] **Step 2: Create `src/components/admin/ColumnVisibilityTab.tsx`**

```tsx
// src/components/admin/ColumnVisibilityTab.tsx
'use client'
import { useState, useTransition } from 'react'
import { updateColumnVisibility } from '@/actions/admin'

const COLUMN_LABELS: Record<string, string> = {
  name: 'Facility Name',
  owner: 'Owner',
  location: 'Location',
  facilityType: 'Type',
  modalities: 'Modalities',
  region: 'Region',
}

interface ColumnVisibilityTabProps {
  columnVisibility: Record<string, boolean>
}

export default function ColumnVisibilityTab({ columnVisibility }: ColumnVisibilityTabProps) {
  const [visibility, setVisibility] = useState(columnVisibility)
  const [saved, setSaved] = useState(false)
  const [pending, startTransition] = useTransition()

  function toggle(key: string) {
    setVisibility((prev) => ({ ...prev, [key]: !prev[key] }))
    setSaved(false)
  }

  function save() {
    startTransition(async () => {
      await updateColumnVisibility(visibility)
      setSaved(true)
    })
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 max-w-md">
      <p className="text-sm text-gray-500 mb-4">
        Toggle which columns are visible to all visitors on the facility table.
      </p>
      <div className="space-y-3">
        {Object.entries(COLUMN_LABELS).map(([key, label]) => (
          <label key={key} className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={visibility[key] !== false}
              onChange={() => toggle(key)}
              className="w-4 h-4 accent-emerald-600"
            />
            <span className="text-sm text-gray-800">{label}</span>
          </label>
        ))}
      </div>
      <div className="mt-6 flex items-center gap-3">
        <button
          onClick={save}
          disabled={pending}
          className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 disabled:opacity-50 transition-colors"
        >
          {pending ? 'Saving…' : 'Save'}
        </button>
        {saved && <span className="text-sm text-emerald-700">Saved!</span>}
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Modify `src/app/admin/page.tsx`** — fetch column visibility and pass to AdminClient

In `AdminPage`, add after the `users` fetch:

```typescript
const { fetchColumnVisibility } = await import('@/lib/facilities')
const columnVisibility = await fetchColumnVisibility(admin)
```

And update the `<AdminClient>` call:

```tsx
<AdminClient users={users ?? []} columnVisibility={columnVisibility} />
```

- [ ] **Step 4: Modify `src/app/admin/AdminClient.tsx`** — add `columnVisibility` prop and wire tab

Update `AdminClientProps`:
```typescript
interface AdminClientProps {
  users: Profile[]
  columnVisibility: Record<string, boolean>
}
```

Update function signature:
```typescript
export default function AdminClient({ users, columnVisibility }: AdminClientProps) {
```

Replace the column visibility placeholder:
```tsx
{activeTab === 'columns' && (
  <ColumnVisibilityTab columnVisibility={columnVisibility} />
)}
```

Add import at top of file:
```typescript
import ColumnVisibilityTab from '@/components/admin/ColumnVisibilityTab'
```

- [ ] **Step 5: Build check + manual test**

```bash
npm run build
```

Sign in as admin → `/admin` → Column Visibility tab → toggle a column off → Save → visit `/` as a non-admin user → confirm the column is hidden.

- [ ] **Step 6: Commit**

```bash
git add src/actions/admin.ts src/components/admin/ColumnVisibilityTab.tsx src/app/admin/page.tsx src/app/admin/AdminClient.tsx
git commit -m "feat: add Column Visibility tab to admin panel"
```

---

## Task 7: Admin Facilities tab + facility form

**Files:**
- Modify: `src/actions/admin.ts` — add `upsertFacility`, `deleteFacility`, `toggleFacilityVisible`
- Create: `src/components/admin/FacilitiesTab.tsx`
- Create: `src/components/admin/FacilityForm.tsx`
- Modify: `src/app/admin/page.tsx` — fetch all facilities (admin client); pass to `AdminClient`
- Modify: `src/app/admin/AdminClient.tsx` — wire `FacilitiesTab`

**Interfaces:**
- Produces: `upsertFacility(data: FacilityFormData)`, `deleteFacility(id: string)`, `toggleFacilityVisible(id: string, visible: boolean)` server actions
- Produces: `<FacilitiesTab facilities={…} />` with Add/Edit/Delete/Visible toggle
- Produces: `<FacilityForm facility={…} | null onClose={…} />` — full form for all fields

- [ ] **Step 1: Add facility actions to `src/actions/admin.ts`**

Append to the existing file:

```typescript
export interface FacilityFormData {
  id: string
  name: string
  owner: string
  city: string
  country: string
  region: string
  lat: number
  lng: number
  facilityType: string
  modalities: string[]
  scale: string[]
  capacity: string
  clients: string[]
  products: string[]
  legacy: string
  certifications: string[]
  website: string
  imageUrl: string
  notes: string
  visible: boolean
}

export async function upsertFacility(data: FacilityFormData) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const row = {
    id: data.id,
    name: data.name,
    owner: data.owner,
    city: data.city,
    country: data.country,
    region: data.region,
    lat: data.lat,
    lng: data.lng,
    facility_type: data.facilityType,
    modalities: data.modalities,
    scale: data.scale,
    capacity: data.capacity,
    clients: data.clients,
    products: data.products,
    legacy: data.legacy,
    certifications: data.certifications,
    website: data.website,
    image_url: data.imageUrl,
    notes: data.notes,
    visible: data.visible,
  }
  const { error } = await admin.from('facilities').upsert(row)
  if (error) throw new Error(error.message)
}

export async function deleteFacility(id: string) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin.from('facilities').delete().eq('id', id)
  if (error) throw new Error(error.message)
}

export async function toggleFacilityVisible(id: string, visible: boolean) {
  await requireAdmin()
  const admin = createSupabaseAdminClient()
  const { error } = await admin
    .from('facilities')
    .update({ visible })
    .eq('id', id)
  if (error) throw new Error(error.message)
}
```

- [ ] **Step 2: Create `src/components/admin/FacilityForm.tsx`**

```tsx
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
```

- [ ] **Step 3: Create `src/components/admin/FacilitiesTab.tsx`**

```tsx
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
```

- [ ] **Step 4: Update `src/app/admin/page.tsx`** — fetch facilities and pass to AdminClient

After the `users` fetch, add:

```typescript
const { data: facilitiesRaw } = await admin
  .from('facilities')
  .select('*')
  .order('name')

const { fetchFacilities } = await import('@/lib/facilities')
// Re-map raw rows to Facility type using admin client
const facilities = await fetchFacilities(admin)
```

Update `<AdminClient>`:
```tsx
<AdminClient users={users ?? []} columnVisibility={columnVisibility} facilities={facilities} />
```

- [ ] **Step 5: Update `src/app/admin/AdminClient.tsx`** — add `facilities` prop and wire tab

Add to imports: `import FacilitiesTab from '@/components/admin/FacilitiesTab'`

Update `AdminClientProps`:
```typescript
interface AdminClientProps {
  users: Profile[]
  columnVisibility: Record<string, boolean>
  facilities: import('@/types/facility').Facility[]
}
```

Update function signature: `export default function AdminClient({ users, columnVisibility, facilities }: AdminClientProps)`

Replace the facilities placeholder:
```tsx
{activeTab === 'facilities' && <FacilitiesTab facilities={facilities} />}
```

- [ ] **Step 6: Build check**

```bash
npm run build
```

- [ ] **Step 7: Manual test**

Sign in as admin → `/admin` → Facilities tab:
- Verify all 20 facilities listed
- Toggle a facility's Visible toggle → confirm change persists on reload
- Click Edit → form opens pre-filled → save
- Click Add Facility → form opens empty → fill and save → new row appears
- Click Delete → confirmation → row removed

- [ ] **Step 8: Commit**

```bash
git add src/actions/admin.ts src/components/admin/FacilitiesTab.tsx src/components/admin/FacilityForm.tsx src/app/admin/page.tsx src/app/admin/AdminClient.tsx
git commit -m "feat: add Facilities tab with add/edit/delete and visible toggle"
```

---

## Task 8: Deploy to Vercel + configure environment variables

**Files:**
- No code changes — deployment and configuration only

**Interfaces:**
- Produces: live production app at `biomanufacturing.vercel.app` with Supabase auth working

- [ ] **Step 1: Push all commits to GitHub**

```bash
git push origin main
```

- [ ] **Step 2: Set environment variables in Vercel**

Go to https://vercel.com → your `biomanufacturing` project → **Settings → Environment Variables**. Add all three:

| Name | Value |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | from Supabase Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | from Supabase Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | from Supabase Settings → API → Service Role |

Set all three for **Production**, **Preview**, and **Development** environments.

- [ ] **Step 3: Trigger a redeployment**

In Vercel dashboard → **Deployments** → click **Redeploy** on the latest deployment. Or push a trivial commit to trigger CI.

- [ ] **Step 4: Verify production**

Open `https://biomanufacturing.vercel.app`:
- Redirects to `/login` — auth works
- Register with `b.w.dejong@hotmail.com` if not done yet
- Run `UPDATE profiles SET role = 'admin' WHERE email = 'b.w.dejong@hotmail.com'` in Supabase SQL editor
- Sign in → map and table load → Header shows "Admin" link
- Navigate to `/admin` → all three tabs functional

- [ ] **Step 5: Final commit**

```bash
git add .
git commit -m "chore: deployment verified on Vercel with Supabase env vars"
git push
```
