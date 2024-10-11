from typing import Dict

from session.model.RadarShotModel import RadarShotModel

METER_TO_FEET_CONVERSION_CONSTANT = 3.28084


def fit_file_to_radar_shots_mapper(radar_messages_dict: Dict) -> RadarShotModel:
    if len(radar_messages_dict.keys()) == 0:
        return []

    shot_dicts = radar_messages_dict['chrono_shot_data_mesgs']
    session_messages = radar_messages_dict['chrono_shot_session_mesgs']
    session_message = session_messages[0]
    weight_grain = session_message['grain_weight']
    shots = []

    for shot_dict in shot_dicts:
        shot_speed_meter_per_second = shot_dict['shot_speed']
        shot_speed_fps = shot_speed_meter_per_second * METER_TO_FEET_CONVERSION_CONSTANT

        shot_energy_joules = energy_equation_joules(weight_grain, shot_speed_fps)
        radar_shot = RadarShotModel(
            shot_number=shot_dict['shot_num'],
            speed_fps=shot_speed_fps,
            datetime=shot_dict['timestamp'],
            weight_grain=weight_grain,
            energy_joules=shot_energy_joules,
        )
        shots.append(radar_shot)
    return shots


def radar_shot_to_dict(radar_shot: RadarShotModel):
    radar_dict = radar_shot.__dict__.copy()
    radar_dict["datetime"] = radar_shot.datetime.isoformat()
    return radar_dict


def energy_equation_joules(mass_grains, velocity_fps):
    conversion_constant = 332270.47791102016
    return mass_grains * (velocity_fps ** 2) / conversion_constant
