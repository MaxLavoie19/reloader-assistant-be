from datetime import datetime

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService
from reload.service.TrayService import TrayService

tray_service = TrayService()
scale_reader = ScaleReaderService(tray_service)
now = datetime.now().isoformat().replace(":", "_")
destination = f"bullets_{now}.json"
scale_loop_state = ScaleLoopStateModel(destination=destination, record_length=True)
values = scale_reader.record_grid(scale_loop_state)
