from typing import Iterable, List
import numpy as np

import matplotlib.pyplot as plt
from filtering.model.KalmanFilterStateModel import KalmanFilterStateModel


def plot_kalman_filter_state_list(state_list: List[KalmanFilterStateModel]):
    positions = []
    position_variances = []
    velocities = []
    velocity_variances = []

    for state in state_list:
        positions.append(state['position'])
        position_variances.append(state['position_variance'])
        velocities.append(state['velocity'])
        velocity_variances.append(state['velocity_variance'])

    plot_kalman_filter_states(
      positions,
      position_variances,
      velocities,
      velocity_variances,
      positions,
      velocities,
    )


def plot_kalman_filter_states(
    positions: Iterable[float],
    position_variances: Iterable[float],
    velocities: Iterable[float],
    velocity_variances: Iterable[float],
    expected_position: Iterable[float],
    expected_velocities: Iterable[float],
):
    fig, [(p, pv), (v, vv)] = plt.subplots(2, 2)
    p.plot(positions)
    pv.plot(position_variances, color='r')
    pv.plot(-np.asarray(position_variances), color='r')
    pv.plot(np.asarray(positions) - expected_position)
    v.plot(velocities)
    vv.plot(velocity_variances, color='r')
    vv.plot(-np.asarray(velocity_variances), color='r')
    vv.plot(np.asarray(velocities) - expected_velocities)
