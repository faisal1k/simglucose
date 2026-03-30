export function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="soft-card p-4">
      <p className="text-xs uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-white">{value}</p>
    </div>
  )
}
