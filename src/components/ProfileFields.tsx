'use client'
import { useState } from 'react'

export interface ProfileData {
  firstName: string
  lastName: string
  jobTitle: string
  company: string
  orgType: string
  country: string
  phone: string
  mailingList: boolean
}

const ORG_TYPES = [
  'Cluster',
  'Incubator',
  'Investor',
  'Large Company',
  'Pilot facility',
  'Public authority',
  'Research organization',
  'Service Provider',
  'SME',
  'Start-up',
  'To-be-start-up',
  'Other',
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
const label = 'block text-sm font-medium text-gray-700 mb-1'

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
            <label className={label}>First name <span className="text-red-500">*</span></label>
            <input name="firstName" type="text" required defaultValue={defaults.firstName} className={field} />
          </div>
          <div>
            <label className={label}>Last name <span className="text-red-500">*</span></label>
            <input name="lastName" type="text" required defaultValue={defaults.lastName} className={field} />
          </div>
        </div>
        <div className="mt-3">
          <label className={label}>Job title <span className="text-red-500">*</span></label>
          <input name="jobTitle" type="text" required defaultValue={defaults.jobTitle} className={field} />
        </div>
      </div>

      {/* Organisation */}
      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Organisation</p>
        <div>
          <label className={label}>Company / organisation name <span className="text-red-500">*</span></label>
          <input name="company" type="text" required defaultValue={defaults.company} className={field} />
        </div>
        <div className="mt-3">
          <label className={label}>Organisation type <span className="text-red-500">*</span></label>
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
            <label className={label}>Please specify <span className="text-red-500">*</span></label>
            <input name="orgTypeOther" type="text" required className={field} />
          </div>
        )}
      </div>

      {/* Location & contact */}
      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Location &amp; contact</p>
        <div>
          <label className={label}>Country <span className="text-red-500">*</span></label>
          <select name="country" required defaultValue={defaults.country ?? ''} className={field}>
            <option value="">Select country…</option>
            {COUNTRIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div className="mt-3">
          <label className={label}>Phone number</label>
          <input name="phone" type="tel" defaultValue={defaults.phone} className={field} placeholder="+31 6 …" />
        </div>
      </div>

      {/* Preferences */}
      <div className="flex items-start gap-3 pt-1">
        <input
          id="mailingList"
          name="mailingList"
          type="checkbox"
          defaultChecked={defaults.mailingList}
          className="mt-0.5 h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
        />
        <label htmlFor="mailingList" className="text-sm text-gray-600">
          Subscribe to our newsletter for updates on new pilot facilities and platform features
        </label>
      </div>
    </div>
  )
}
