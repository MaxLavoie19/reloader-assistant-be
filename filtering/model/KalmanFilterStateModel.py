from dataclasses import dataclass


@dataclass
class KalmanFilterStateModel:
    position: float = None
    last_position: float = None
    position_variance: float = None
    last_position_variance: float = None
    min_position_variance: float = None
    velocity: float = None
    last_velocity: float = None
    velocity_variance: float = None
    last_velocity_variance: float = None
    min_velocity_variance: float = None
    timestamp: float = None
    last_timestamp: float = None
    time_delta: float = None
    last_time_delta: float = None
    damping_factor: float = None
    maximum_position: float = None
    minimum_position: float = None
    maximum_velocity: float = None
    minimum_velocity: float = None
