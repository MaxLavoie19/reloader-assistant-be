from datetime import datetime
import pyinputplus

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService
from reload.service.TrayService import TrayService

tray_service = TrayService()
scale_reader = ScaleReaderService(tray_service)

min_value = pyinputplus.inputFloat("Min value (gn): ")
max_value = pyinputplus.inputFloat("Max value (gn): ")
now = datetime.now().isoformat().replace(":", "_")
destination = f"powders_{min_value.__str__()}-{max_value.__str__()}_{now}.json"
scale_loop_state = ScaleLoopStateModel(
  destination=destination, min_value=min_value, max_value=max_value
)
values = scale_reader.record_grid(scale_loop_state)
