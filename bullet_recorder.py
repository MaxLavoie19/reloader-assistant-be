from datetime import datetime
import json

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService

scale_reader = ScaleReaderService()
scale_loop_state = ScaleLoopStateModel(record_length=True)
values_grid = scale_reader.record_grid(scale_loop_state)
now = datetime.now()

with open(f"bullets_{now.isoformat()}.json", 'w') as destination:
  json.dump(values_grid, destination)
