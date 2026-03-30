from dataclasses import dataclass


@dataclass
class PIDConfig:
    kp: float = 0.015
    ki: float = 0.00008
    kd: float = 0.08
    target_glucose: float = 110.0
    min_u_per_hr: float = 0.0
    max_u_per_hr: float = 6.0


class PIDController:
    """PID insulin controller that returns temporary basal insulin in U/hr."""

    def __init__(self, config: PIDConfig):
        self.config = config
        self._integral = 0.0
        self._prev_error = 0.0

    def reset(self) -> None:
        self._integral = 0.0
        self._prev_error = 0.0

    def step(self, glucose_mgdl: float, dt_min: int) -> float:
        error = glucose_mgdl - self.config.target_glucose
        dt_hr = dt_min / 60
        self._integral += error * dt_hr
        derivative = 0.0 if dt_hr <= 0 else (error - self._prev_error) / dt_hr

        output = (
            (self.config.kp * error)
            + (self.config.ki * self._integral)
            + (self.config.kd * derivative)
        )
        self._prev_error = error

        return max(self.config.min_u_per_hr, min(self.config.max_u_per_hr, output))
