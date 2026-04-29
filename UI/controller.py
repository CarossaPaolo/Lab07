import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = self._view.dd_mese

    def handle_umidita_media(self, e):
        mese = self._mese
        if mese is None:
            self._view.lst_result.controls.append(
                ft.Text("Devi selezionare un mese!")
            )
        else:
            self._view.lst_result.controls.append(
                ft.Text(f"L'umidità media nel mese {mese}:")
            )
            self._view.lst_result.controls.append(
                ft.Text(self._model.get_umidita_media_mese(mese))
            )
        self._view.update_page()

    def handle_sequenza(self, e):
        mese = self._mese
        if mese is None:
            self._view.lst_result.controls.append(
                ft.Text("Devi selezionare un mese!")
            )
        else:
            seq, costo = self._model.genera_sol_ottima(mese)
            self._view.lst_result.controls.append(
                ft.Text(f"L'sequenza del mese ({mese}) fino al giorno 15:")
            )
            self._view.lst_result.controls.append(
                ft.Text(f"Costo sequenza ottima: {costo}")
            )
            for situazione in seq:
                self._view.lst_result.controls.append(
                    ft.Text(situazione.__str__())
                )

        self._view.update_page()


    def read_mese(self, e):
        self._mese = int(e.control.value)

