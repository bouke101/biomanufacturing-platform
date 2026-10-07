// src/app/admin/AdminClient.tsx
'use client'
import { useState } from 'react'
import UsersTab from '@/components/admin/UsersTab'
import ColumnVisibilityTab from '@/components/admin/ColumnVisibilityTab'
import FacilitiesTab from '@/components/admin/FacilitiesTab'
import type { AllFilterValues } from '@/components/admin/ContentFiltersTab'
import type { ColumnFilters } from '@/lib/facilities'

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
  columnVisibility: Record<string, boolean>
  columnFilters: ColumnFilters
  allFilterValues: AllFilterValues
  valueCounts: Record<string, Record<string, number>>
  totalFacilities: number
  facilities: import('@/types/facility').Facility[]
}

export default function AdminClient({
  users,
  columnVisibility,
  columnFilters,
  allFilterValues,
  valueCounts,
  totalFacilities,
  facilities,
}: AdminClientProps) {
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
          Columns
        </button>
        <button className={tabClass('facilities')} onClick={() => setActiveTab('facilities')}>
          Facilities
        </button>
      </div>

      {activeTab === 'users' && <UsersTab users={users} />}
      {activeTab === 'columns' && (
        <ColumnVisibilityTab
          columnVisibility={columnVisibility}
          columnFilters={columnFilters}
          allFilterValues={allFilterValues}
          valueCounts={valueCounts}
          totalFacilities={totalFacilities}
        />
      )}
      {activeTab === 'facilities' && <FacilitiesTab facilities={facilities} />}
    </div>
  )
}
