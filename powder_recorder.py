from datetime import datetime
import json
import pyinputplus

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService

scale_reader = ScaleReaderService()

min_value = pyinputplus.inputFloat("Min value")
max_value = pyinputplus.inputFloat("Max value")
scale_loop_state = ScaleLoopStateModel(min_value=min_value, max_value=max_value)
values_grid = scale_reader.record_grid(scale_loop_state)
now = datetime.now()
file_name = f"{now.isoformat()}_{min_value.__str__()}-{max_value.__str__()}_powders.json"
with open(file_name, 'w') as destination:
  json.dump(values_grid, destination)
