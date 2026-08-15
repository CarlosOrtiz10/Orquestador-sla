from datetime import datetime
from uuid import UUID
from .event_bus import BusEventos
from .ports import RepositorioIncidentes
from ..domain.entities import Equipo, Incidente, Servicio
from ..domain.enums import Impacto, Urgencia
from ..domain.factory import FabricaIncidentes


class GestorIncidentes:
    def __init__(self, fabrica: FabricaIncidentes, repositorio: RepositorioIncidentes,
                 bus: BusEventos) -> None:
        self._fabrica = fabrica
        self._repositorio = repositorio
        self._bus = bus

    def reportar(self, titulo: str, descripcion: str, servicio: Servicio,
                 impacto: Impacto, urgencia: Urgencia, ahora: datetime) -> Incidente:
        incidente = self._fabrica.crear(titulo, descripcion, servicio, impacto, urgencia, ahora)
        self._repositorio.guardar(incidente)
        return incidente

    def asignar(self, incidente_id: UUID, equipo: Equipo, ahora: datetime) -> Incidente:
        return self._aplicar(incidente_id, lambda i: i.asignar(equipo, ahora))

    def iniciar(self, incidente_id: UUID, ahora: datetime) -> Incidente:
        return self._aplicar(incidente_id, lambda i: i.iniciar_diagnostico(ahora))

    def resolver(self, incidente_id: UUID, causa: str, ahora: datetime) -> Incidente:
        return self._aplicar(incidente_id, lambda i: i.resolver(ahora, causa))

    def cerrar(self, incidente_id: UUID, ahora: datetime) -> Incidente:
        return self._aplicar(incidente_id, lambda i: i.cerrar(ahora))

    def _aplicar(self, incidente_id: UUID, operacion) -> Incidente:
        incidente = self._repositorio.obtener(incidente_id)
        operacion(incidente)
        self._repositorio.guardar(incidente)
        self._bus.publicar(incidente.extraer_eventos())
        return incidente

