from typing import Iterable
import numpy as np

import matplotlib.pyplot as plt


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
