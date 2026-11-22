"""Test del comportamento della classe Centro."""

import unittest
from datetime import date, timedelta

from prenotazioni import (
    ORIZZONTE_GIORNI,
    Centro,
    DataNonAmmessa,
    Laboratorio,
    LaboratorioNonTrovato,
    Sessione,
    SessioneNonTrovata,
)


class TestCentro(unittest.TestCase):
    def setUp(self):
        self.oggi = date(2026, 11, 23)
        self.centro = Centro()
        self.centro.aggiungi_laboratorio(Laboratorio("C1", "Cucina calda", 16))
        self.centro.aggiungi_laboratorio(Laboratorio("P1", "Pasticceria", 12))

    def _richiesta(self, giorno, codice="C1", inizio="09:00", fine="10:00"):
        return Sessione(codice, giorno, inizio, fine, "Mario Rossi", 8)

    def test_rifiuta_codice_laboratorio_duplicato(self):
        duplicato = Laboratorio("C1", "Seconda cucina", 8)

        with self.assertRaises(ValueError):
            self.centro.aggiungi_laboratorio(duplicato)

    def test_segnala_laboratorio_inesistente(self):
        with self.assertRaises(LaboratorioNonTrovato):
            self.centro.laboratorio("Z9")

    def test_rifiuta_date_fuori_orizzonte(self):
        passato = self.oggi - timedelta(days=1)
        oltre_limite = self.oggi + timedelta(days=ORIZZONTE_GIORNI + 2)
        for giorno in (passato, oltre_limite):
            with self.subTest(giorno=giorno):
                richiesta = self._richiesta(giorno)

                with self.assertRaises(DataNonAmmessa):
                    self.centro.prenota(richiesta, oggi=self.oggi)

    def test_rifiuta_prenotazione_di_venerdi(self):
        richiesta = self._richiesta(date(2026, 11, 27))

        with self.assertRaises(DataNonAmmessa):
            self.centro.prenota(richiesta, oggi=self.oggi)

    def test_accetta_prenotazione_per_oggi(self):
        richiesta = self._richiesta(self.oggi)

        identificativo = self.centro.prenota(richiesta, oggi=self.oggi)

        self.assertIs(self.centro.sessione(identificativo), richiesta)

    def test_assegna_id_progressivi_anche_dopo_una_cancellazione(self):
        primo = self.centro.prenota(self._richiesta(self.oggi), oggi=self.oggi)
        secondo = self.centro.prenota(self._richiesta(self.oggi, "P1"), oggi=self.oggi)
        self.centro.cancella(primo)

        terzo = self.centro.prenota(self._richiesta(self.oggi), oggi=self.oggi)

        self.assertEqual((primo, secondo, terzo), (1, 2, 3))

    def test_segnala_sessione_inesistente(self):
        for operazione in (self.centro.sessione, self.centro.cancella):
            with self.subTest(operazione=operazione.__name__):
                with self.assertRaises(SessioneNonTrovata):
                    operazione(99)

    def test_ordina_e_filtra_le_sessioni_del_giorno(self):
        giorno = date(2026, 11, 24)
        ultima = self._richiesta(giorno, "C1", "11:00", "12:00")
        prima = self._richiesta(giorno, "P1", "09:00", "10:00")
        intermedia = self._richiesta(giorno, "C1", "10:00", "11:00")
        for richiesta in (ultima, prima, intermedia, self._richiesta(self.oggi)):
            self.centro.prenota(richiesta, oggi=self.oggi)

        tutte = self.centro.sessioni_del_giorno(giorno)
        cucina_calda = self.centro.sessioni_del_giorno(giorno, "C1")

        self.assertEqual(tutte, [prima, intermedia, ultima])
        self.assertEqual(cucina_calda, [intermedia, ultima])
