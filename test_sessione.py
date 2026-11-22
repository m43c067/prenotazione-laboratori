"""Test del comportamento della classe Sessione."""

import unittest
from datetime import date

from prenotazioni import Sessione


class TestSessione(unittest.TestCase):
    def setUp(self):
        self.giorno = date(2026, 11, 23)
        self.sessione = Sessione(
            "C1", self.giorno, "08:30", "10:00", "Mario Rossi", 12, "Pane"
        )

    def test_rifiuta_orari_non_ammessi(self):
        casi = (
            ("08:15", "10:00"),
            ("07:30", "10:00"),
            ("19:00", "20:30"),
            ("10:00", "10:00"),
            ("10:00", "09:30"),
        )
        for inizio, fine in casi:
            with self.subTest(inizio=inizio, fine=fine):
                with self.assertRaises(ValueError):
                    Sessione("C1", self.giorno, inizio, fine, "Mario Rossi", 12)

    def test_rifiuta_giorno_che_non_e_una_data(self):
        with self.assertRaises(TypeError):
            Sessione("C1", "2026-11-23", "08:30", "10:00", "Mario Rossi", 12)

    def test_calcola_la_durata_in_minuti(self):
        durata = self.sessione.durata_minuti()

        self.assertEqual(durata, 90)

    def test_verifica_la_sovrapposizione(self):
        casi = (
            ("P1", self.giorno, False),
            ("C1", date(2026, 11, 24), False),
            ("C1", self.giorno, True),
        )
        for laboratorio, giorno, atteso in casi:
            with self.subTest(laboratorio=laboratorio, giorno=giorno):
                altra = Sessione(laboratorio, giorno, "09:00", "09:30", "Anna Verdi", 8)

                self.assertEqual(self.sessione.si_sovrappone(altra), atteso)

    def test_ricostruisce_la_sessione_dal_dizionario(self):
        self.sessione.id = 7
        dati = self.sessione.to_dict()

        ricostruita = Sessione.from_dict(dati)

        self.assertEqual(ricostruita.to_dict(), dati)
        self.assertEqual(ricostruita.id, 7)
