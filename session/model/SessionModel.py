from dataclasses import dataclass

import datetime as datetime


@dataclass
class SessionModel:
    email: str
    datetime: datetime
