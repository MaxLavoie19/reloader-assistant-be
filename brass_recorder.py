from datetime import datetime

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService
from reload.service.TrayService import TrayService

tray_service = TrayService()
scale_reader = ScaleReaderService(tray_service)
now = datetime.now()
destination = f"brasses_{now.isoformat()}.json"
scale_loop_state = ScaleLoopStateModel(destination=destination)
values = scale_reader.record_grid(scale_loop_state)
