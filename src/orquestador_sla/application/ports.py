from abc import ABC, abstractmethod
from uuid import UUID
from ..domain.entities import Incidente
from ..domain.events import EventoDominio


class RepositorioIncidentes(ABC):
    @abstractmethod
    def guardar(self, incidente: Incidente) -> None: ...

    @abstractmethod
    def obtener(self, incidente_id: UUID) -> Incidente: ...


class ObservadorEventos(ABC):
    @abstractmethod
    def actualizar(self, evento: EventoDominio) -> None: ...

