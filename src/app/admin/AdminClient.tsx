// src/app/admin/AdminClient.tsx
'use client'
import { useState } from 'react'
import UsersTab from '@/components/admin/UsersTab'
import ColumnVisibilityTab from '@/components/admin/ColumnVisibilityTab'

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
}

export default function AdminClient({ users, columnVisibility }: AdminClientProps) {
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
        <ColumnVisibilityTab columnVisibility={columnVisibility} />
      )}
      {activeTab === 'facilities' && (
        <p className="text-gray-400 text-sm">Facilities — coming in next task.</p>
      )}
    </div>
  )
}
