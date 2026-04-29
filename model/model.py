from os import WCONTINUED
from sys import flags
from traceback import print_tb
from model.situazione import Situazione
from database.meteo_dao import MeteoDao

class Model:
    _CITTA = ['Milano', 'Torino', 'Genova']
    _MAX_GIORNI_PER_CITTA = 6
    _MIN_GIORNI_CONSECUTIVI = 3
    _NUM_GIORNI = 15

    def __init__(self):
        self._data = None
        self._best_cost = float("inf")
        self._best_seq = []

    def get_umidita_media_mese(self, mese):
        data = MeteoDao.get_umidita_media_mese(mese)
        result = ""
        for r in data:
            localita = r["Localita"]
            avg_umidita = r["Avg_umidita"]
            result += f"{localita}: {avg_umidita:.2f}%\n"
        return result

    def load_dati(self, mese):
        """
        dati gi ogetti sitazione gia ordinati crescenti per data
        crea un dizionario <locailita> : [<umidita_day1>...]
        """
        situazioni = MeteoDao.get_situazioni_mese(mese)
        umidita = {}
        for s in situazioni:
            if s.localita not in umidita:
                umidita[s.localita] = []
            umidita[s.localita].append((s.umidita, s.data))
        return umidita

    def genera_sol_ottima(self, mese):
        self._data = self.load_dati(mese)
        _contatore = {c: 0 for c in self._CITTA}
        self._best_cost = float("inf")
        self._best_seq = []
        self._ricorsione(0, [], None,0,
                         0, _contatore)
        return self._best_seq, self._best_cost

    def _ricorsione(self, livello, seq, ultima_citta, giorni_consecutivi,
                    costo_parziale, contatore):

        # CONDIZIONE TERMINALE
        if livello == self._NUM_GIORNI:
            if costo_parziale < self._best_cost:
                self._best_cost = costo_parziale
                self._best_seq = seq.copy()
            return

        # PRUNING
        # Se il costo parziale supera il best è inutile continuare il calcolo
        if costo_parziale >= self._best_cost:
            return

        # LOOP
        # Prova ogni città per il livello in esame
        for citta in self._CITTA:
            umidita = self._data[citta][livello][0]
            giorno  = self._data[citta][livello][1]

            # CALCOLO COSTO PARZIALE
            costo_spostamento = 100 if (ultima_citta is not None
                                        and citta != ultima_citta ) else 0
            nuovo_costo = costo_parziale + costo_spostamento + umidita

            nuovi_giorni_consecutivi = giorni_consecutivi + 1 if citta == ultima_citta else 1

            # FILTRO
            # VINCOLO 1: non piu di 6 giorni per citta
            if contatore[citta] >= self._MAX_GIORNI_PER_CITTA:
                continue
            # VINCOLO 2: minimo 3 giorni per citta prima di cambiare
            if ultima_citta is not None and citta != ultima_citta:
                if giorni_consecutivi < self._MIN_GIORNI_CONSECUTIVI:
                    continue
            # AGGIORNO STATO
            seq.append(Situazione(citta, giorno, umidita))
            contatore[citta] += 1

            # CHIAMATA RICORSIVA
            self._ricorsione(livello + 1, seq, citta, nuovi_giorni_consecutivi,nuovo_costo,contatore)

            # BACKTRACKING
            seq.pop()
            contatore[citta] -= 1



