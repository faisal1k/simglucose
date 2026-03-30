import { useMemo } from 'react'
import { useAppStore } from '../lib/store'
import { StatCard } from '../components/StatCard'

export function DashboardPage() {
  const { patients, scenarios, latestResult } = useAppStore()

  const latest = useMemo(() => latestResult?.summary, [latestResult])

  return (
    <div className="space-y-6">
      <section className="soft-card p-6">
        <h1 className="text-3xl font-semibold text-white">Personal Simulation Platform</h1>
        <p className="mt-2 text-slate-300">Design custom virtual patients, run insulin-meal experiments, and compare response dynamics.</p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Patients" value={patients.length} />
        <StatCard label="Scenarios" value={scenarios.length} />
        <StatCard label="Avg Glucose (last run)" value={latest ? `${latest.average_glucose} mg/dL` : '—'} />
        <StatCard label="Time in Range" value={latest ? `${latest.time_in_range_percent}%` : '—'} />
      </section>
    </div>
  )
}
