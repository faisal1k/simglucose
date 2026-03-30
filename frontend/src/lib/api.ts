import axios from 'axios'
import type { Patient, Scenario, SimulationResult } from '../types'

const api = axios.create({ baseURL: 'http://127.0.0.1:8000' })

export const Api = {
  async getPatients() {
    const { data } = await api.get<Patient[]>('/patients')
    return data
  },
  async createPatient(payload: Omit<Patient, 'id'>) {
    const { data } = await api.post<Patient>('/patients', payload)
    return data
  },
  async updatePatient(id: string, payload: Omit<Patient, 'id'>) {
    const { data } = await api.put<Patient>(`/patients/${id}`, payload)
    return data
  },
  async deletePatient(id: string) {
    await api.delete(`/patients/${id}`)
  },
  async getScenarios() {
    const { data } = await api.get<Scenario[]>('/scenarios')
    return data
  },
  async createScenario(payload: Omit<Scenario, 'id'>) {
    const { data } = await api.post<Scenario>('/scenarios', payload)
    return data
  },
  async simulate(patient_id: string, scenario_id: string, seed?: number) {
    const { data } = await api.post<SimulationResult>('/simulate', { patient_id, scenario_id, seed })
    return data
  }
}
