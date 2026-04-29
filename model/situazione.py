import datetime
from dataclasses import dataclass
# from json.decoder import NaN


@dataclass
class Situazione:
    localita: str
    data: datetime.date
    umidita: int

    def __eq__(self, other):
        return self.localita == other.localita and self.data == other.data

    def __hash__(self):
        return hash((self.localita, self.data))

    def __str__(self):
        return f"[{self.localita} - {self.data}] Umidità = {self.umidita}"
