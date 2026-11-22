"""Test dei difetti segnalati nel motore di prenotazione."""

import unittest
from datetime import date

from prenotazioni import Sessione


class TestSegnalazioni(unittest.TestCase):
    def test_accetta_sessione_all_orario_di_apertura(self):
        giorno = date(2026, 11, 23)

        sessione = Sessione("C1", giorno, "08:00", "10:00", "Mario Rossi", 12)

        self.assertEqual(sessione.inizio, "08:00")
