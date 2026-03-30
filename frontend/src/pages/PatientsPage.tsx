import { FormEvent, useState } from 'react'
import { Api } from '../lib/api'
import { useAppStore } from '../lib/store'
import type { Patient } from '../types'

const emptyPatient: Omit<Patient, 'id'> = {
  name: 'New Patient',
  body_weight_kg: 70,
  age_years: 30,
  baseline_glucose_mgdl: 110,
  insulin_sensitivity_factor: 40,
  carb_ratio: 10,
  basal_rate_u_per_hr: 1,
  insulin_action_duration_min: 240,
  carb_absorption_duration_min: 180,
  glucose_effectiveness: 0.2,
  variability_noise_std: 2,
  activity_sensitivity_modifier: 1
}

export function PatientsPage() {
  const { patients, setPatients, setSelectedPatientId, selectedPatientId } = useAppStore()
  const [form, setForm] = useState(emptyPatient)

  const save = async (e: FormEvent) => {
    e.preventDefault()
    const created = await Api.createPatient(form)
    setPatients([...patients, created])
  }

  const clone = async (p: Patient) => {
    const { id: _, ...payload } = p
    const created = await Api.createPatient({ ...payload, name: `${payload.name} (Clone)` })
    setPatients([...patients, created])
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_380px]">
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Patient Library</h2>
        {patients.map((p) => (
          <div key={p.id} className="soft-card flex items-center justify-between p-4">
            <div>
              <p className="font-medium">{p.name}</p>
              <p className="text-sm text-slate-400">ISF {p.insulin_sensitivity_factor} | CR {p.carb_ratio} | Basal {p.basal_rate_u_per_hr} U/hr</p>
            </div>
            <div className="flex gap-2">
              <button className="rounded bg-cyan-500/20 px-3 py-1" onClick={() => setSelectedPatientId(p.id)}>{selectedPatientId === p.id ? 'Selected' : 'Select'}</button>
              <button className="rounded bg-violet-500/20 px-3 py-1" onClick={() => clone(p)}>Clone</button>
            </div>
          </div>
        ))}
      </section>
      <form onSubmit={save} className="soft-card space-y-3 p-4">
        <h3 className="font-semibold">Create Patient</h3>
        {Object.entries(form).map(([k, v]) => (
          <label key={k} className="block text-sm">
            {k}
            <input
              className="mt-1 w-full rounded bg-slate-800 p-2"
              type={typeof v === 'number' ? 'number' : 'text'}
              value={v}
              onChange={(e) => setForm((s) => ({ ...s, [k]: typeof v === 'number' ? +e.target.value : e.target.value }))}
              required
            />
          </label>
        ))}
        <button className="w-full rounded bg-cyan-500 py-2 font-medium text-slate-950">Save patient</button>
      </form>
    </div>
  )
}
