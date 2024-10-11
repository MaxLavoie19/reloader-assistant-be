import json

from reload.service.ScaleReaderService import ScaleReaderService

scale_reader = ScaleReaderService()
values_grid = scale_reader.record_grid()

with open(f"brasses.json", 'w') as destination:
  json.dump(values_grid, destination)
