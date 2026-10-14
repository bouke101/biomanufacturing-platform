// src/components/admin/NewsTab.tsx
"use client"
import { useState, useTransition } from "react"
import { createNewsItem, deleteNewsItem } from "@/actions/news"
import type { NewsItem } from "@/lib/news"
import type { NewsItemFormData } from "@/actions/news"

const EVENT_TYPES = [
  "expansion", "closure", "acquisition", "incident", "partnership", "other",
] as const

const EMPTY_FORM: NewsItemFormData = {
  date: "",
  headline: "",
  body: "",
  product_tags: "",
  company_tags: "",
  event_type: "other",
  source_url: "",
}

export default function NewsTab({ initialNews }: { initialNews: NewsItem[] }) {
  const [items, setItems] = useState(initialNews)
  const [form, setForm] = useState<NewsItemFormData>(EMPTY_FORM)
  const [pending, startTransition] = useTransition()

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  function handleAdd(e: React.FormEvent) {
    e.preventDefault()
    startTransition(async () => {
      await createNewsItem(form)
      setForm(EMPTY_FORM)
      window.location.reload()
    })
  }

  function handleDelete(id: string) {
    if (!confirm("Delete this news item?")) return
    startTransition(async () => {
      await deleteNewsItem(id)
      setItems((prev) => prev.filter((n) => n.id !== id))
    })
  }

  return (
    <div>
      {/* Add form */}
      <form onSubmit={handleAdd} className="bg-white rounded-xl border border-gray-200 p-5 mb-6 space-y-4">
        <h3 className="text-sm font-semibold text-gray-800">Add news item</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Date</label>
            <input
              type="date"
              name="date"
              required
              value={form.date}
              onChange={handleChange}
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Event type</label>
            <select
              name="event_type"
              value={form.event_type}
              onChange={handleChange}
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
            >
              {EVENT_TYPES.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Headline</label>
          <input
            type="text"
            name="headline"
            required
            value={form.headline}
            onChange={handleChange}
            placeholder="BASF Ludwigshafen vitamin synthesis plant expands capacity"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Body</label>
          <textarea
            name="body"
            required
            rows={4}
            value={form.body}
            onChange={handleChange}
            placeholder="1–3 paragraph summary of the event…"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 resize-y"
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Product tags <span className="font-normal text-gray-400">(comma-separated, lowercase)</span>
            </label>
            <input
              type="text"
              name="product_tags"
              value={form.product_tags}
              onChange={handleChange}
              placeholder="vitamin a, retinol"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Company tags <span className="font-normal text-gray-400">(comma-separated, lowercase)</span>
            </label>
            <input
              type="text"
              name="company_tags"
              value={form.company_tags}
              onChange={handleChange}
              placeholder="basf, dsm-firmenich"
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Source URL <span className="font-normal text-gray-400">(optional)</span>
          </label>
          <input
            type="url"
            name="source_url"
            value={form.source_url}
            onChange={handleChange}
            placeholder="https://…"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={pending}
            className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 transition-colors disabled:opacity-50"
          >
            {pending ? "Saving…" : "Add item"}
          </button>
        </div>
      </form>

      {/* News list */}
      <p className="text-sm text-gray-500 mb-3">{items.length} news items</p>
      {items.length === 0 ? (
        <p className="text-sm text-gray-400 italic">No news items yet. Add one above.</p>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Date</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Headline</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Type</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Tags</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} className="border-t border-gray-100">
                  <td className="px-4 py-3 text-gray-500 whitespace-nowrap">{item.date}</td>
                  <td className="px-4 py-3 text-gray-800 max-w-xs truncate">{item.headline}</td>
                  <td className="px-4 py-3">
                    <span className="inline-block px-2 py-0.5 text-xs rounded-full bg-blue-100 text-blue-700 font-medium">
                      {item.event_type}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 text-xs">
                    {[...item.product_tags, ...item.company_tags].join(", ") || "—"}
                  </td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleDelete(item.id)}
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
      )}
    </div>
  )
}
