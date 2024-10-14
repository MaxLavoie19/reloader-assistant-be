from datetime import datetime

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel
from reload.service.ScaleReaderService import ScaleReaderService

scale_reader = ScaleReaderService()
now = datetime.now()
destination = f"bullets_{now.isoformat()}.json"
scale_loop_state = ScaleLoopStateModel(destination=destination, record_length=True)
values = scale_reader.record_grid(scale_loop_state)
