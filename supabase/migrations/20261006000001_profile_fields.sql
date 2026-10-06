alter table public.profiles
  add column first_name text not null default '',
  add column last_name  text not null default '',
  add column job_title  text not null default '',
  add column company    text not null default '',
  add column org_type   text not null default '',
  add column country    text not null default '',
  add column phone      text not null default '',
  add column mailing_list boolean not null default false;

-- Allow users to update their own profile
create policy "Users update own profile"
  on public.profiles for update
  using (auth.uid() = id);
