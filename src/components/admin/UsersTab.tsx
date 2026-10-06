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
