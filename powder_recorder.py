from datetime import datetime
import pyinputplus

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService

scale_reader = ScaleReaderService()

min_value = pyinputplus.inputFloat("Min value")
max_value = pyinputplus.inputFloat("Max value")
now = datetime.now()
destination = f"powders_{min_value.__str__()}-{max_value.__str__()}_{now.isoformat()}.json"
scale_loop_state = ScaleLoopStateModel(
  min_value=min_value, max_value=max_value, destination=destination
)
values = scale_reader.record_grid(scale_loop_state)
