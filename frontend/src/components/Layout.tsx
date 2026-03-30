import { Link, NavLink } from 'react-router-dom'
import { Activity, FlaskConical, House, Users } from 'lucide-react'
import { ReactNode } from 'react'

const nav = [
  { to: '/', label: 'Dashboard', icon: House },
  { to: '/patients', label: 'Patients', icon: Users },
  { to: '/scenarios', label: 'Scenarios', icon: FlaskConical },
  { to: '/runner', label: 'Simulation', icon: Activity }
]

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[240px_1fr]">
      <aside className="border-r border-white/10 bg-slate-950/90 p-5 backdrop-blur-md lg:sticky lg:top-0 lg:h-screen">
        <Link to="/" className="mb-8 block text-xl font-semibold text-cyan-300">Virtual Glucose Lab</Link>
        <nav className="space-y-2">
          {nav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-2 rounded-xl px-3 py-2 ${isActive ? 'bg-cyan-400/20 text-cyan-200' : 'text-slate-300 hover:bg-white/10'}`
              }
            >
              <item.icon size={16} />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="p-4 md:p-8">{children}</main>
    </div>
  )
}
