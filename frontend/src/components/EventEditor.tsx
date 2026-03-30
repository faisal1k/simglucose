import type { InsulinEvent, MealEvent } from '../types'

export function MealEditor({ meals, onChange }: { meals: MealEvent[]; onChange: (meals: MealEvent[]) => void }) {
  const update = (idx: number, key: keyof MealEvent, value: number) => {
    const copy = [...meals]
    copy[idx] = { ...copy[idx], [key]: value }
    onChange(copy)
  }

  return (
    <div className="space-y-2">
      {meals.map((m, idx) => (
        <div key={idx} className="grid grid-cols-2 gap-2">
          <input className="rounded bg-slate-800 p-2" type="number" value={m.time_min} onChange={(e) => update(idx, 'time_min', +e.target.value)} />
          <input className="rounded bg-slate-800 p-2" type="number" value={m.carbs_g} onChange={(e) => update(idx, 'carbs_g', +e.target.value)} />
        </div>
      ))}
      <button className="rounded bg-cyan-500/20 px-3 py-2" onClick={() => onChange([...meals, { time_min: 0, carbs_g: 30 }])}>Add meal</button>
    </div>
  )
}

export function BolusEditor({ boluses, onChange }: { boluses: InsulinEvent[]; onChange: (boluses: InsulinEvent[]) => void }) {
  const update = (idx: number, key: keyof InsulinEvent, value: number) => {
    const copy = [...boluses]
    copy[idx] = { ...copy[idx], [key]: value }
    onChange(copy)
  }

  return (
    <div className="space-y-2">
      {boluses.map((b, idx) => (
        <div key={idx} className="grid grid-cols-2 gap-2">
          <input className="rounded bg-slate-800 p-2" type="number" value={b.time_min} onChange={(e) => update(idx, 'time_min', +e.target.value)} />
          <input className="rounded bg-slate-800 p-2" type="number" value={b.units} onChange={(e) => update(idx, 'units', +e.target.value)} />
        </div>
      ))}
      <button className="rounded bg-violet-500/20 px-3 py-2" onClick={() => onChange([...boluses, { time_min: 0, units: 1 }])}>Add bolus</button>
    </div>
  )
}
