import { useState } from 'react'
import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Api } from '../lib/api'
import { useAppStore } from '../lib/store'
import { StatCard } from '../components/StatCard'

export function RunnerPage() {
  const {
    patients,
    scenarios,
    selectedPatientId,
    selectedScenarioId,
    setSelectedPatientId,
    setSelectedScenarioId,
    latestResult,
    comparisonResult,
    setLatestResult,
    setComparisonResult
  } = useAppStore()

  const [running, setRunning] = useState(false)

  const runSimulation = async (compare = false) => {
    if (!selectedPatientId || !selectedScenarioId) return
    setRunning(true)
    const result = await Api.simulate(selectedPatientId, selectedScenarioId)
    compare ? setComparisonResult(result) : setLatestResult(result)
    setRunning(false)
  }

  const data = latestResult?.points ?? []
  const comparison = comparisonResult?.points ?? []

  return (
    <div className="space-y-6">
      <div className="soft-card grid gap-3 p-4 md:grid-cols-4">
        <select className="rounded bg-slate-800 p-2" value={selectedPatientId} onChange={(e) => setSelectedPatientId(e.target.value)}>
          <option value="">Select patient</option>
          {patients.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <select className="rounded bg-slate-800 p-2" value={selectedScenarioId} onChange={(e) => setSelectedScenarioId(e.target.value)}>
          <option value="">Select scenario</option>
          {scenarios.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
        <button className="rounded bg-cyan-500 py-2 font-medium text-slate-950" onClick={() => runSimulation(false)} disabled={running}>{running ? 'Running...' : 'Run simulation'}</button>
        <button className="rounded bg-violet-500 py-2 font-medium text-white" onClick={() => runSimulation(true)} disabled={running}>Run comparison</button>
      </div>

      {latestResult && (
        <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-6">
          <StatCard label="Average" value={latestResult.summary.average_glucose} />
          <StatCard label="Peak" value={latestResult.summary.peak_glucose} />
          <StatCard label="Minimum" value={latestResult.summary.minimum_glucose} />
          <StatCard label="Time in Range" value={`${latestResult.summary.time_in_range_percent}%`} />
          <StatCard label="Hypo events" value={latestResult.summary.hypo_events} />
          <StatCard label="Hyper events" value={latestResult.summary.hyper_events} />
        </div>
      )}

      <div className="soft-card h-[420px] p-4">
        <h3 className="mb-3 font-semibold">Glucose Trajectory</h3>
        <ResponsiveContainer>
          <LineChart data={data}>
            <XAxis dataKey="t_min" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" domain={[40, 260]} />
            <Tooltip />
            <ReferenceLine y={70} stroke="#f59e0b" strokeDasharray="4 4" />
            <ReferenceLine y={180} stroke="#ef4444" strokeDasharray="4 4" />
            <Line type="monotone" dataKey="glucose_mgdl" stroke="#22d3ee" strokeWidth={2} dot={false} />
            {comparison.length > 0 && <Line type="monotone" data={comparison} dataKey="glucose_mgdl" stroke="#c084fc" strokeWidth={2} dot={false} />}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
