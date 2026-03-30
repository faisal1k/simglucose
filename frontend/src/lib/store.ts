import { create } from 'zustand'
import type { Patient, Scenario, SimulationResult } from '../types'

interface AppState {
  patients: Patient[]
  scenarios: Scenario[]
  selectedPatientId?: string
  selectedScenarioId?: string
  latestResult?: SimulationResult
  comparisonResult?: SimulationResult
  setPatients: (patients: Patient[]) => void
  setScenarios: (scenarios: Scenario[]) => void
  setSelectedPatientId: (id?: string) => void
  setSelectedScenarioId: (id?: string) => void
  setLatestResult: (result?: SimulationResult) => void
  setComparisonResult: (result?: SimulationResult) => void
}

export const useAppStore = create<AppState>((set) => ({
  patients: [],
  scenarios: [],
  setPatients: (patients) => set({ patients }),
  setScenarios: (scenarios) => set({ scenarios }),
  setSelectedPatientId: (selectedPatientId) => set({ selectedPatientId }),
  setSelectedScenarioId: (selectedScenarioId) => set({ selectedScenarioId }),
  setLatestResult: (latestResult) => set({ latestResult }),
  setComparisonResult: (comparisonResult) => set({ comparisonResult })
}))
