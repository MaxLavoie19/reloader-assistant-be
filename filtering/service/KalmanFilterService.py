import math

from filtering.model.KalmanFilterStateModel import KalmanFilterStateModel
from filtering.service.FitnessService import FitnessService



class KalmanFilterService:
    def __init__(self, fitness_service: FitnessService):
        self.fitness_service = fitness_service

    @staticmethod
    def state_update(current_value: float, new_reading: float, gain: float):
        if current_value is None:
            return new_reading
        innovation = new_reading - current_value
        return current_value + innovation * gain

    @staticmethod
    def get_kalman_gain(estimate_variance: float, measurement_variance: float):
        total_variance = estimate_variance + measurement_variance
        if total_variance == 0:
            return 1
        return estimate_variance / total_variance

    @staticmethod
    def get_estimate_variance(kalman_gain: float, variance: float):
        return (1 - kalman_gain) * variance

    @staticmethod
    def get_average_rate_of_change(initial_state: float, final_state: float, time_delta: float):
        return (final_state - initial_state) / time_delta

    @staticmethod
    def kinematic_equation(position, velocity, time_delta):
        return position + time_delta * velocity

    def get_anticipated(self, kalman_filter_state: KalmanFilterStateModel, time_delta: int | float = 0):
        predictive_position = self.kinematic_equation(
            kalman_filter_state.last_position or kalman_filter_state.position or 0,
            kalman_filter_state.last_velocity or kalman_filter_state.velocity or 0,
            kalman_filter_state.time_delta or time_delta,
        )
        predictive_position_variance = self.kinematic_equation(
            kalman_filter_state.last_position_variance or kalman_filter_state.position_variance or 0,
            kalman_filter_state.last_velocity_variance or kalman_filter_state.velocity_variance or 0,
            kalman_filter_state.time_delta or time_delta,
        )
        return predictive_position, predictive_position_variance

    @staticmethod
    def init_position(
        kalman_filter_state: KalmanFilterStateModel,
        new_reading: float,
        reading_variance: float,
        timestamp: float
    ):
        kalman_filter_state.position = new_reading
        kalman_filter_state.position_variance = reading_variance
        kalman_filter_state.timestamp = timestamp

    def init_velocity(
        self,
        kalman_filter_state: KalmanFilterStateModel,
        new_reading: float,
        reading_variance: float,
    ):
        self.update_position(kalman_filter_state, new_reading, reading_variance)

        average_velocity = self.get_average_rate_of_change(
            kalman_filter_state.last_position, kalman_filter_state.position, kalman_filter_state.time_delta
        )
        average_velocity_variance = \
            (kalman_filter_state.last_position_variance + reading_variance) / kalman_filter_state.time_delta
        position_standard_deviation = math.sqrt(kalman_filter_state.position_variance)
        new_measure_fitness = self.fitness_service.get_datapoint_fitness(
            kalman_filter_state.last_position, position_standard_deviation, new_reading
        )
        kalman_filter_state.velocity = average_velocity * (1 - new_measure_fitness)
        kalman_filter_state.velocity_variance = average_velocity_variance * (1 - new_measure_fitness)

    @staticmethod
    def progress_kalman_filter_state(kalman_filter_state: KalmanFilterStateModel):
        kalman_filter_state.last_position = kalman_filter_state.position
        kalman_filter_state.last_position_variance = kalman_filter_state.position_variance
        kalman_filter_state.last_velocity = kalman_filter_state.velocity
        kalman_filter_state.last_velocity_variance = kalman_filter_state.velocity_variance
        kalman_filter_state.last_timestamp = kalman_filter_state.timestamp
        kalman_filter_state.last_time_delta = kalman_filter_state.time_delta

    @staticmethod
    def get_velocity_kalman_filter(kalman_filter_state: KalmanFilterStateModel):
        velocity_kalman_filter_state = KalmanFilterStateModel()
        velocity_kalman_filter_state.position = kalman_filter_state.velocity
        velocity_kalman_filter_state.position_variance = kalman_filter_state.velocity_variance
        velocity_kalman_filter_state.min_position_variance = kalman_filter_state.min_velocity_variance
        velocity_kalman_filter_state.time_delta = kalman_filter_state.time_delta
        return velocity_kalman_filter_state

    @staticmethod
    def get_min_variance(variance, min_variance):
        if min_variance is None:
            return variance
        return max(min_variance, variance)

    def update_position(
        self,
        kalman_filter_state: KalmanFilterStateModel,
        new_reading: float,
        reading_variance: float,
    ):
        predictive_position, predictive_position_variance = self.get_anticipated(kalman_filter_state)
        kalman_gain = self.get_kalman_gain(predictive_position_variance, reading_variance)
        effective_gain = kalman_gain * (kalman_filter_state.damping_factor or 1)
        kalman_filter_state.position = self.state_update(predictive_position, new_reading, effective_gain)
        position_variance = self.get_estimate_variance(kalman_gain, predictive_position_variance)
        kalman_filter_state.position_variance = self.get_min_variance(
            position_variance, kalman_filter_state.min_position_variance
        )
        if kalman_filter_state.minimum_position is not None\
                and kalman_filter_state.position < kalman_filter_state.minimum_position:
            kalman_filter_state.position = kalman_filter_state.minimum_position

        if kalman_filter_state.maximum_position is not None \
                and kalman_filter_state.position > kalman_filter_state.maximum_position:
            kalman_filter_state.position = kalman_filter_state.maximum_position

    def update_velocity(self, kalman_filter_state: KalmanFilterStateModel):
        average_velocity = self.get_average_rate_of_change(
            kalman_filter_state.last_position, kalman_filter_state.position, kalman_filter_state.time_delta
        )
        average_velocity_variance = (
                kalman_filter_state.last_position_variance + kalman_filter_state.position_variance
            ) / kalman_filter_state.time_delta
        velocity_kalman_filter_state = self.get_velocity_kalman_filter(kalman_filter_state)
        self.update_position(velocity_kalman_filter_state, average_velocity, average_velocity_variance)
        kalman_filter_state.velocity = velocity_kalman_filter_state.position
        kalman_filter_state.velocity_variance = self.get_min_variance(
            velocity_kalman_filter_state.position_variance, kalman_filter_state.min_velocity_variance
        )
        if kalman_filter_state.minimum_velocity is not None\
                and kalman_filter_state.velocity < kalman_filter_state.minimum_velocity:
            kalman_filter_state.velocity = kalman_filter_state.minimum_velocity

        if kalman_filter_state.maximum_velocity is not None \
                and kalman_filter_state.velocity > kalman_filter_state.maximum_velocity:
            kalman_filter_state.velocity = kalman_filter_state.maximum_velocity

    def kalman_filter(
        self,
        kalman_filter_state: KalmanFilterStateModel,
        new_reading: float,
        reading_variance: float,
        timestamp: float
    ):
        if kalman_filter_state.position is None:
            self.init_position(kalman_filter_state, new_reading, reading_variance, timestamp)
            return

        if kalman_filter_state.timestamp != timestamp:
            last_timestamp = kalman_filter_state.timestamp or 0
            kalman_filter_state.time_delta = timestamp - last_timestamp
            self.progress_kalman_filter_state(kalman_filter_state)
            kalman_filter_state.timestamp = timestamp

        if kalman_filter_state.velocity is None:
            if kalman_filter_state.time_delta is None:
                self.update_position(kalman_filter_state, new_reading, reading_variance)
                return
            self.init_velocity(kalman_filter_state, new_reading, reading_variance)
            return

        self.update_position(kalman_filter_state, new_reading, reading_variance)
        self.update_velocity(kalman_filter_state)
