import datetime
from model.situazione import Situazione
from dataclasses import dataclass

@dataclass
class Stato:
    situazioni: Situazione = None
    giorni_cons: int = 0
    seq: list[Situazione] = None
    costo_totale: int = 0

    def __eq__(self, other):
        return self.situazioni == other.situazioni

    def __hash__(self):
        return hash(self.situazioni)

    def __str__(self):
        return f"[{self.seq}\ncosto_attuale: {self.costo_totale}]"
