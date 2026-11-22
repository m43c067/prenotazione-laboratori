"""Test dei difetti segnalati nel motore di prenotazione."""

import unittest
from datetime import date

from prenotazioni import Centro, Laboratorio, Sessione


class TestSegnalazioni(unittest.TestCase):
    def test_accetta_sessione_all_orario_di_apertura(self):
        giorno = date(2026, 11, 23)

        sessione = Sessione("C1", giorno, "08:00", "10:00", "Mario Rossi", 12)

        self.assertEqual(sessione.inizio, "08:00")

    def test_accetta_una_classe_che_riempie_il_laboratorio(self):
        oggi = date(2026, 11, 23)
        giorno = date(2026, 11, 24)
        centro = Centro()
        centro.aggiungi_laboratorio(Laboratorio("P1", "Pasticceria", 12))
        sessione = Sessione("P1", giorno, "08:30", "10:00", "Mario Rossi", 12)

        identificativo = centro.prenota(sessione, oggi=oggi)

        self.assertIs(centro.sessione(identificativo), sessione)
