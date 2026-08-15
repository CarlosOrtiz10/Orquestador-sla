from datetime import datetime, timezone
from .application.event_bus import BusEventos
from .application.services import GestorIncidentes
from .domain.entities import Equipo, Servicio
from .domain.enums import Impacto, Urgencia
from .domain.factory import FabricaIncidentes
from .domain.strategies import PriorizacionPorRiesgo
from .infrastructure.observers import AuditoriaMemoria, NotificadorConsola
from .infrastructure.repositories import RepositorioIncidentesMemoria


def ejecutar_demo() -> None:
    reloj = lambda: datetime.now(timezone.utc)
    bus = BusEventos()
    auditoria = AuditoriaMemoria()
    bus.suscribir(NotificadorConsola())
    bus.suscribir(auditoria)
    gestor = GestorIncidentes(
        FabricaIncidentes(PriorizacionPorRiesgo()),
        RepositorioIncidentesMemoria(), bus,
    )
    pagos = Servicio("PAGOS", "API de pagos", critico=True)
    sre = Equipo("SRE", "Site Reliability Engineering", {"PAGOS", "AUTH"})
    incidente = gestor.reportar(
        "Latencia crítica en pagos",
        "El percentil 95 supera 8 segundos y aumenta el abandono.",
        pagos, Impacto.ALTO, Urgencia.ALTA, reloj(),
    )
    gestor.asignar(incidente.id, sre, reloj())
    gestor.iniciar(incidente.id, reloj())
    gestor.resolver(incidente.id, "Pool de conexiones agotado", reloj())
    gestor.cerrar(incidente.id, reloj())
    print(f"\nIncidente {incidente.id} | {incidente.prioridad.name} | {incidente.estado}")
    print(f"Eventos auditados: {len(auditoria.eventos)}")


if __name__ == "__main__":
    ejecutar_demo()

