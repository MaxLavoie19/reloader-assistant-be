import json

from reload.service.ScaleReaderService import ScaleReaderService

scale_reader = ScaleReaderService()
min_value = float(input("Min value"))
max_value = float(input("Max value"))
values_grid = scale_reader.record_grid(min_value, max_value)

with open(f"powders.json", 'w') as destination:
  json.dump(values_grid, destination)
