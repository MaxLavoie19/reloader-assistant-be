from datetime import datetime

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService

scale_reader = ScaleReaderService()
now = datetime.now()
destination = f"brasses_{now.isoformat()}.json"
scale_loop_state = ScaleLoopStateModel(destination=destination)
values = scale_reader.record_grid(scale_loop_state)
