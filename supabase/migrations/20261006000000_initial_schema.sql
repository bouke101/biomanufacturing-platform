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
  source text not null default 'manual',
  pilots4u_page text not null default '',
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

-- RLS: profiles — users see only their own row
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

-- Seed: default column visibility
insert into public.settings (key, value) values (
  'column_visibility',
  '{"name": true, "owner": true, "location": true, "facilityType": true, "modalities": true, "region": true}'::jsonb
);
