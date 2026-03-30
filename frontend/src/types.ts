export interface Patient {
  id: string
  name: string
  body_weight_kg: number
  age_years: number
  baseline_glucose_mgdl: number
  insulin_sensitivity_factor: number
  carb_ratio: number
  basal_rate_u_per_hr: number
  insulin_action_duration_min: number
  carb_absorption_duration_min: number
  glucose_effectiveness: number
  variability_noise_std: number
  activity_sensitivity_modifier: number
}

export interface MealEvent {
  time_min: number
  carbs_g: number
}

export interface InsulinEvent {
  time_min: number
  units: number
}

export interface ExerciseEvent {
  start_min: number
  end_min: number
  intensity: number
}

export interface Scenario {
  id: string
  name: string
  duration_min: number
  time_step_min: number
  starting_glucose_mgdl: number
  target_glucose_mgdl: number
  meals: MealEvent[]
  boluses: InsulinEvent[]
  correction_threshold_mgdl?: number | null
  exercise: ExerciseEvent[]
  disturbance_std: number
  model_name: string
  controller_enabled: boolean
  controller_kp: number
  controller_ki: number
  controller_kd: number
  activity_effect_scale: number
}

export interface SimulationPoint {
  t_min: number
  glucose_mgdl: number
  insulin_on_board_u: number
  carbs_on_board_g: number
  basal_units_delivered: number
  bolus_units_delivered: number
  meal_carbs_ingested: number
}

export interface SimulationSummary {
  average_glucose: number
  peak_glucose: number
  minimum_glucose: number
  time_in_range_percent: number
  hypo_events: number
  hyper_events: number
}

export interface SimulationResult {
  id: string
  patient_name: string
  scenario_name: string
  points: SimulationPoint[]
  summary: SimulationSummary
  model_version: string
}
