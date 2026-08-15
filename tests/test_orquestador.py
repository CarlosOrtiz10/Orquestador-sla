import unittest
from datetime import datetime, timezone
from orquestador_sla.application.event_bus import BusEventos
from orquestador_sla.application.services import GestorIncidentes
from orquestador_sla.domain.entities import Equipo, Servicio
from orquestador_sla.domain.enums import Impacto, Prioridad, Urgencia
from orquestador_sla.domain.factory import FabricaIncidentes
from orquestador_sla.domain.strategies import PriorizacionPorRiesgo
from orquestador_sla.infrastructure.observers import AuditoriaMemoria
from orquestador_sla.infrastructure.repositories import RepositorioIncidentesMemoria


class OrquestadorTest(unittest.TestCase):
    def setUp(self):
        self.ahora = datetime(2026, 8, 14, tzinfo=timezone.utc)
        self.bus = BusEventos()
        self.audit = AuditoriaMemoria()
        self.bus.suscribir(self.audit)
        self.gestor = GestorIncidentes(FabricaIncidentes(PriorizacionPorRiesgo()),
                                      RepositorioIncidentesMemoria(), self.bus)
        self.servicio = Servicio("CORE", "Núcleo transaccional", True)

    def crear(self):
        return self.gestor.reportar("Bloqueo de transacciones", "No se procesan operaciones",
                                    self.servicio, Impacto.ALTO, Urgencia.ALTA, self.ahora)

    def test_incidente_critico_es_p1(self):
        self.assertEqual(self.crear().prioridad, Prioridad.P1)

    def test_flujo_completo_publica_eventos(self):
        incidente = self.crear()
        equipo = Equipo("PLAT", "Plataforma", {"CORE"})
        self.gestor.asignar(incidente.id, equipo, self.ahora)
        self.gestor.iniciar(incidente.id, self.ahora)
        self.gestor.resolver(incidente.id, "Saturación del pool", self.ahora)
        self.gestor.cerrar(incidente.id, self.ahora)
        self.assertEqual(incidente.estado, "CERRADO")
        self.assertEqual(len(self.audit.eventos), 4)

    def test_transicion_invalida_es_rechazada(self):
        with self.assertRaises(ValueError):
            self.gestor.cerrar(self.crear().id, self.ahora)

    def test_equipo_sin_especialidad_es_rechazado(self):
        with self.assertRaises(ValueError):
            self.gestor.asignar(self.crear().id, Equipo("UX", "Experiencia", {"WEB"}), self.ahora)


if __name__ == "__main__":
    unittest.main()

