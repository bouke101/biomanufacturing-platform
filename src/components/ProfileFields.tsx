'use client'
import { useState } from 'react'

export interface ProfileData {
  username: string
  firstName: string
  lastName: string
  jobTitle: string
  company: string
  orgType: string
  country: string
  phone: string
}

const ORG_TYPES = [
  'Cluster', 'Incubator', 'Investor', 'Large Company', 'Pilot facility',
  'Public authority', 'Research organization', 'Service Provider',
  'SME', 'Start-up', 'To-be-start-up', 'Other',
]

const COUNTRIES = [
  'Austria','Belgium','Bulgaria','Croatia','Cyprus','Czechia','Denmark','Estonia',
  'Finland','France','Germany','Greece','Hungary','Iceland','Ireland','Italy',
  'Latvia','Liechtenstein','Lithuania','Luxembourg','Malta','Netherlands','Norway',
  'Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','Switzerland',
  'United Kingdom','Albania','Bosnia and Herzegovina','Kosovo','Montenegro',
  'North Macedonia','Serbia','Turkey','Ukraine','United States','Canada','Australia',
  'China','India','Japan','South Korea','Singapore','Brazil','South Africa','Other',
]

const field = 'w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white'
const lbl   = 'block text-sm font-medium text-gray-700 mb-1'
const req   = <span className="text-red-500">*</span>

interface Props {
  defaults?: Partial<ProfileData>
}

export default function ProfileFields({ defaults = {} }: Props) {
  const [orgType, setOrgType] = useState(defaults.orgType ?? '')

  return (
    <div className="space-y-5">

      {/* Personal */}
      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Personal information</p>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className={lbl}>First name {req}</label>
            <input name="firstName" type="text" required defaultValue={defaults.firstName} className={field} />
          </div>
          <div>
            <label className={lbl}>Last name {req}</label>
            <input name="lastName" type="text" required defaultValue={defaults.lastName} className={field} />
          </div>
        </div>
        <div className="mt-3">
          <label className={lbl}>
            Username
            <span className="ml-1 text-xs font-normal text-gray-400">(optional — defaults to first name)</span>
          </label>
          <input
            name="username"
            type="text"
            defaultValue={defaults.username}
            placeholder={defaults.firstName || 'e.g. jsmith'}
            className={field}
          />
        </div>
        <div className="mt-3">
          <label className={lbl}>Job title {req}</label>
          <input name="jobTitle" type="text" required defaultValue={defaults.jobTitle} className={field} />
        </div>
      </div>

      {/* Organisation */}
      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Organisation</p>
        <div>
          <label className={lbl}>Company / organisation name {req}</label>
          <input name="company" type="text" required defaultValue={defaults.company} className={field} />
        </div>
        <div className="mt-3">
          <label className={lbl}>Organisation type {req}</label>
          <select
            name="orgType"
            required
            value={orgType}
            onChange={(e) => setOrgType(e.target.value)}
            className={field}
          >
            <option value="">Select type…</option>
            {ORG_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        {orgType === 'Other' && (
          <div className="mt-3">
            <label className={lbl}>Please specify {req}</label>
            <input name="orgTypeOther" type="text" required className={field} />
          </div>
        )}
      </div>

      {/* Location & contact */}
      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Location &amp; contact</p>
        <div>
          <label className={lbl}>Country {req}</label>
          <select name="country" required defaultValue={defaults.country ?? ''} className={field}>
            <option value="">Select country…</option>
            {COUNTRIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div className="mt-3">
          <label className={lbl}>Phone number {req}</label>
          <input name="phone" type="tel" required defaultValue={defaults.phone} placeholder="+31 6 …" className={field} />
        </div>
      </div>

    </div>
  )
}
