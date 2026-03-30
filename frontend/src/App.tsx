import { Route, Routes } from 'react-router-dom'
import { useEffect } from 'react'
import { Layout } from './components/Layout'
import { DashboardPage } from './pages/DashboardPage'
import { PatientsPage } from './pages/PatientsPage'
import { ScenariosPage } from './pages/ScenariosPage'
import { RunnerPage } from './pages/RunnerPage'
import { Api } from './lib/api'
import { useAppStore } from './lib/store'

export default function App() {
  const { setPatients, setScenarios } = useAppStore()

  useEffect(() => {
    Api.getPatients().then(setPatients)
    Api.getScenarios().then(setScenarios)
  }, [setPatients, setScenarios])

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/patients" element={<PatientsPage />} />
        <Route path="/scenarios" element={<ScenariosPage />} />
        <Route path="/runner" element={<RunnerPage />} />
      </Routes>
    </Layout>
  )
}
