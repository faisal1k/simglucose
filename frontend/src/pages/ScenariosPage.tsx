import { FormEvent, useState } from 'react'
import { Api } from '../lib/api'
import { useAppStore } from '../lib/store'
import type { Scenario } from '../types'
import { BolusEditor, MealEditor } from '../components/EventEditor'

const emptyScenario: Omit<Scenario, 'id'> = {
  name: 'Custom Scenario',
  duration_min: 480,
  time_step_min: 5,
  starting_glucose_mgdl: 110,
  target_glucose_mgdl: 110,
  meals: [{ time_min: 60, carbs_g: 45 }],
  boluses: [{ time_min: 45, units: 4 }],
  correction_threshold_mgdl: 180,
  exercise: [],
  disturbance_std: 1,
  model_name: 'physiological-v2',
  controller_enabled: true,
  controller_kp: 0.015,
  controller_ki: 0.00008,
  controller_kd: 0.08,
  activity_effect_scale: 1
}

export function ScenariosPage() {
  const { scenarios, setScenarios, setSelectedScenarioId, selectedScenarioId } = useAppStore()
  const [form, setForm] = useState(emptyScenario)

  const save = async (e: FormEvent) => {
    e.preventDefault()
    const created = await Api.createScenario(form)
    setScenarios([...scenarios, created])
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_400px]">
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Scenario Builder</h2>
        {scenarios.map((s) => (
          <div key={s.id} className="soft-card flex items-center justify-between p-4">
            <div>
              <p className="font-medium">{s.name}</p>
              <p className="text-sm text-slate-400">{s.model_name} • Duration: {s.duration_min}m | Meals: {s.meals.length} | Boluses: {s.boluses.length}</p>
            </div>
            <button className="rounded bg-cyan-500/20 px-3 py-1" onClick={() => setSelectedScenarioId(s.id)}>{selectedScenarioId === s.id ? 'Selected' : 'Select'}</button>
          </div>
        ))}
      </section>

      <form onSubmit={save} className="soft-card space-y-3 p-4">
        <h3 className="font-semibold">Create Scenario</h3>
        <label className="block text-sm">Name<input className="mt-1 w-full rounded bg-slate-800 p-2" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>
        <label className="block text-sm">Model
          <select className="mt-1 w-full rounded bg-slate-800 p-2" value={form.model_name} onChange={(e) => setForm({ ...form, model_name: e.target.value })}>
            <option value="physiological-v2">Physiological v2</option>
            <option value="simplified-v1">Simplified v1</option>
          </select>
        </label>
        <label className="block text-sm">Duration min<input type="number" className="mt-1 w-full rounded bg-slate-800 p-2" value={form.duration_min} onChange={(e) => setForm({ ...form, duration_min: +e.target.value })} /></label>
        <label className="block text-sm">Starting glucose<input type="number" className="mt-1 w-full rounded bg-slate-800 p-2" value={form.starting_glucose_mgdl} onChange={(e) => setForm({ ...form, starting_glucose_mgdl: +e.target.value })} /></label>
        <label className="block text-sm">PID enabled
          <input type="checkbox" className="ml-2" checked={form.controller_enabled} onChange={(e) => setForm({ ...form, controller_enabled: e.target.checked })} />
        </label>
        <div className="grid grid-cols-3 gap-2">
          <label className="text-xs">Kp<input type="number" step="0.001" className="mt-1 w-full rounded bg-slate-800 p-2" value={form.controller_kp} onChange={(e) => setForm({ ...form, controller_kp: +e.target.value })} /></label>
          <label className="text-xs">Ki<input type="number" step="0.00001" className="mt-1 w-full rounded bg-slate-800 p-2" value={form.controller_ki} onChange={(e) => setForm({ ...form, controller_ki: +e.target.value })} /></label>
          <label className="text-xs">Kd<input type="number" step="0.001" className="mt-1 w-full rounded bg-slate-800 p-2" value={form.controller_kd} onChange={(e) => setForm({ ...form, controller_kd: +e.target.value })} /></label>
        </div>
        <div>
          <p className="mb-1 text-sm">Meal timeline (time_min, carbs_g)</p>
          <MealEditor meals={form.meals} onChange={(meals) => setForm({ ...form, meals })} />
        </div>
        <div>
          <p className="mb-1 text-sm">Insulin bolus timeline (time_min, units)</p>
          <BolusEditor boluses={form.boluses} onChange={(boluses) => setForm({ ...form, boluses })} />
        </div>
        <button className="w-full rounded bg-cyan-500 py-2 font-medium text-slate-950">Save scenario</button>
      </form>
    </div>
  )
}
