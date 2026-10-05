# Auth & Admin Panel — Design Spec

**Project:** Biomanufacturing Facility Platform  
**Date:** 2026-10-05  
**Status:** Approved for implementation

---

## Goal

Add email/password authentication so only registered users can view the facility platform, and an admin panel (accessible only to the site owner) for managing users, column visibility, and facility data.

---

## Architecture Overview

Supabase replaces the static `data/facilities.json` and adds authentication. Three new layers are added to the existing Next.js 14 app:

1. **Supabase Auth** — email/password sign-up and sign-in, cookie-based sessions readable server-side
2. **Supabase PostgreSQL** — `facilities`, `profiles`, and `settings` tables; Row Level Security enforces visitor access rules
3. **Next.js middleware** (`src/middleware.ts`) — intercepts every request; unauthenticated users redirect to `/login`; non-admin users accessing `/admin` redirect to `/`

The existing facility table and map components are unchanged except their data source switches from the JSON file to Supabase.

---

## Public Routes

Only two routes are accessible without a session:

- `/login` — email + password sign-in form
- `/register` — self-registration form

All other routes require a valid Supabase session cookie. The middleware handles this transparently — no page renders before the auth check.

---

## Auth Flow

### Registration (`/register`)
1. Visitor enters email + password
2. Supabase creates the auth user
3. A `profiles` row is inserted: `role = 'user'`, `blocked = false`
4. Visitor is redirected to `/` (the facility map)

### Sign-in (`/login`)
1. User enters email + password
2. Supabase validates credentials and sets a session cookie
3. Middleware reads the cookie on every subsequent request
4. If `profiles.blocked = true`: user sees "Your account has been suspended" and cannot proceed
5. If `profiles.role = 'admin'`: user can access `/admin` in addition to all other routes
6. On success: redirect to `/`

### Sign-out
A "Sign out" button in the site header. Clears the Supabase session cookie and redirects to `/login`.

### Admin identity
The admin account is the owner's email (`b.w.dejong@hotmail.com`). During database setup, this user's `profiles.role` is set to `'admin'` via a seed script or Supabase dashboard. No other mechanism promotes users to admin.

---

## Middleware

`src/middleware.ts` runs on every request (configured via `matcher`):

1. Read the Supabase session from the request cookie
2. If no session → redirect to `/login`
3. If session exists and route is `/admin`:
   - Fetch the user's profile from `profiles`
   - If `role !== 'admin'` → redirect to `/`
4. If session exists and `profiles.blocked = true` → redirect to `/login` with a `?blocked=1` query param (shows the suspension message)
5. Otherwise → allow the request through

---

## Database Schema

### `profiles`
| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` | Primary key; foreign key → `auth.users.id` |
| `email` | `text` | Copied from auth for easy display in admin |
| `role` | `text` | `'user'` or `'admin'` |
| `blocked` | `bool` | Default `false` |
| `created_at` | `timestamptz` | Default `now()` |

### `facilities`
All fields from the existing `Facility` TypeScript interface, plus:

| Column | Type | Notes |
|---|---|---|
| `id` | `text` | Primary key (slug, e.g. `"lonza-visp"`) |
| `name` | `text` | |
| `owner` | `text` | |
| `city` | `text` | |
| `country` | `text` | |
| `region` | `text` | `'Europe'` \| `'North America'` \| `'Asia-Pacific'` \| `'Other'` |
| `lat` | `float8` | |
| `lng` | `float8` | |
| `facility_type` | `text` | `'CMO'` \| `'CDMO'` \| `'Captive'` \| `'Toll'` |
| `modalities` | `text[]` | Array of modality strings |
| `scale` | `text[]` | Array: `'Development'`, `'Pilot'`, `'Commercial'` |
| `capacity` | `text` | Empty string if unknown |
| `clients` | `text[]` | Empty array if confidential |
| `products` | `text[]` | |
| `legacy` | `text` | 1–2 sentence history |
| `certifications` | `text[]` | |
| `website` | `text` | |
| `image_url` | `text` | Relative path or empty string |
| `notes` | `text` | |
| `visible` | `bool` | Default `false`; `true` = published to visitors |
| `created_at` | `timestamptz` | Default `now()` |

### `settings`
| Column | Type | Notes |
|---|---|---|
| `key` | `text` | Primary key |
| `value` | `jsonb` | |

Seed row for column visibility:
```json
{
  "key": "column_visibility",
  "value": {
    "name": true,
    "owner": true,
    "location": true,
    "facilityType": true,
    "modalities": true,
    "region": true
  }
}
```

---

## Row Level Security (RLS)

### `facilities`
- **Visitors (authenticated, role = 'user'):** `SELECT` where `visible = true` only
- **Admin (role = 'admin'):** full `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- Unauthenticated requests: no access (all routes behind auth)

### `profiles`
- Users can read their own row (`id = auth.uid()`)
- Admin can read and update all rows

### `settings`
- All authenticated users can `SELECT`
- Only admin can `INSERT` / `UPDATE`

---

## New Pages & Components

### `/login` — `src/app/login/page.tsx`
- Email + password form
- "Sign in" button
- Link to `/register`
- Shows suspension message if `?blocked=1` is in the URL

### `/register` — `src/app/register/page.tsx`
- Email + password + confirm-password form
- "Create account" button
- Link to `/login`
- On success: redirect to `/`

### `/admin` — `src/app/admin/page.tsx`
Three-tab layout:

**Tab 1 — Users**
- Table: email · registration date · last sign-in · status badge (Active / Blocked)
- Per-row toggle: Block / Unblock (updates `profiles.blocked`)

**Tab 2 — Column Visibility**
- Six toggle rows, one per table column: Name · Owner · Location · Type · Modalities · Region
- "Save" button writes to `settings` table
- Change takes effect for all visitors immediately

**Tab 3 — Facilities**
- Table: name · owner · location · visible toggle
- "Add Facility" button → opens facility form (empty)
- Per-row "Edit" button → opens facility form (pre-filled)
- Per-row "Delete" button → confirmation dialog, then hard delete

### Facility form (used in Tab 3)
All fields from the `facilities` table. Multi-value fields (modalities, scale, certifications, clients, products) use a tag-style input (comma-separated values, displayed as chips). Coordinates are two number inputs (lat, lng). A "Visible" toggle controls whether the facility is published.

### Header changes — `src/app/layout.tsx` or `src/components/Header.tsx`
- Add "Sign out" button (right side)
- Add "Admin" link visible only when `role = 'admin'`

---

## Supabase Client Setup

Two clients needed in Next.js 14:

- `src/lib/supabase/client.ts` — browser client (`createBrowserClient`) for client components
- `src/lib/supabase/server.ts` — server client (`createServerClient`) for server components and middleware, reads/writes cookies via Next.js `cookies()`

Use `@supabase/ssr` package (the recommended approach for Next.js App Router).

---

## Data Migration

The 20 facilities from `data/facilities.json` are inserted into the `facilities` table via a seed script (`scripts/seed-facilities.ts`) that reads the JSON and calls `supabase.from('facilities').upsert(...)`. All 20 are seeded with `visible = true`.

---

## Constraints

- No changes to the facility table or map rendering logic — only the data source changes (Supabase query replaces `loadFacilities()`)
- Column visibility is global (admin-set); visitors cannot customize their own column view
- No per-user facility bookmarking or personalisation (future phase)
- No email verification on registration (MVP — add later if needed)
- No password reset flow (MVP — add later via Supabase's built-in email reset)
- Admin role is set manually (seed script or Supabase dashboard); no self-promotion mechanism
