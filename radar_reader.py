from pprint import pprint

from garmin_fit_sdk import Decoder, Stream

from session.mapper.FitFileToRadarShotMapper import fit_file_to_radar_shots_mapper

stream = Stream.from_file("./data/users/maxlavoie1960@hotmail.com/09-20-2024_14-15-10.fit")
decoder = Decoder(stream)
messages, errors = decoder.read()

shots = fit_file_to_radar_shots_mapper(messages)
pprint(messages)

for shot in shots:
    pprint(shot.__dict__)
