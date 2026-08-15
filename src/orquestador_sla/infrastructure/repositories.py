from uuid import UUID
from ..application.ports import RepositorioIncidentes
from ..domain.entities import Incidente


class RepositorioIncidentesMemoria(RepositorioIncidentes):
    def __init__(self) -> None:
        self._datos: dict[UUID, Incidente] = {}

    def guardar(self, incidente: Incidente) -> None:
        self._datos[incidente.id] = incidente

    def obtener(self, incidente_id: UUID) -> Incidente:
        try:
            return self._datos[incidente_id]
        except KeyError as error:
            raise LookupError("Incidente no encontrado") from error

