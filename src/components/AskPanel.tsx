"use client"
import { useState, useRef } from "react"

interface AskPanelProps {
  onResult: (facilityIds: string[]) => void
  onClear: () => void
}

type PanelState = "idle" | "loading" | "answer"

interface AnswerData {
  text: string
  count: number
}

function renderParagraph(text: string): React.ReactNode[] {
  // Replace **bold** with <strong>
  const parts = text.split(/\*\*([^*]+)\*\*/g)
  return parts.map((part, i) =>
    i % 2 === 1 ? <strong key={i}>{part}</strong> : part
  )
}

export default function AskPanel({ onResult, onClear }: AskPanelProps) {
  const [state, setState] = useState<PanelState>("idle")
  const [query, setQuery] = useState("")
  const [answer, setAnswer] = useState<AnswerData | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  async function handleSubmit() {
    const trimmed = query.trim()
    if (!trimmed || state === "loading") return
    setState("loading")
    setErrorMsg(null)

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: trimmed }),
      })
      const data = (await res.json()) as
        | { answer: string; facilityIds: string[] }
        | { error: string }

      if ("error" in data) {
        setErrorMsg(data.error)
        setState("idle")
        return
      }

      setAnswer({ text: data.answer, count: data.facilityIds.length })
      onResult(data.facilityIds)
      setState("answer")
    } catch {
      setErrorMsg("Something went wrong. Please try again.")
      setState("idle")
    }
  }

  function handleClear() {
    setState("idle")
    setAnswer(null)
    setErrorMsg(null)
    setQuery("")
    onClear()
    inputRef.current?.focus()
  }

  const isLoading = state === "loading"
  const hasAnswer = state === "answer"

  return (
    <div className="bg-white border-b border-gray-200 px-4 py-4">
      {/* Input row */}
      <div className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") handleSubmit() }}
          disabled={isLoading}
          placeholder="Ask anything about the market…"
          className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:bg-gray-50 disabled:text-gray-400"
        />
        {hasAnswer ? (
          <button
            onClick={handleClear}
            className="px-4 py-2 text-sm font-medium bg-gray-100 text-gray-600 rounded-md hover:bg-gray-200 transition-colors whitespace-nowrap"
          >
            Clear ×
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={isLoading || !query.trim()}
            className="px-4 py-2 text-sm font-medium bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {isLoading ? "Thinking…" : "Ask →"}
          </button>
        )}
      </div>

      {/* Error */}
      {errorMsg && (
        <p className="mt-2 text-sm text-red-600">{errorMsg}</p>
      )}

      {/* Loading skeleton */}
      {isLoading && (
        <div className="mt-4 space-y-2 animate-pulse">
          <div className="h-3 bg-gray-200 rounded w-full" />
          <div className="h-3 bg-gray-200 rounded w-5/6" />
          <div className="h-3 bg-gray-200 rounded w-4/6" />
        </div>
      )}

      {/* Answer */}
      {hasAnswer && answer && (
        <div className="mt-4">
          <div className="prose-sm text-gray-700 space-y-3">
            {answer.text.split("\n\n").filter(Boolean).map((para, i) => (
              <p key={i}>{renderParagraph(para)}</p>
            ))}
          </div>
          <p className="mt-3 text-xs text-gray-400">
            {answer.count} {answer.count === 1 ? "facility" : "facilities"} matched — showing in table below
          </p>
        </div>
      )}
    </div>
  )
}
