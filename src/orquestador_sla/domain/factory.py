from datetime import datetime
from uuid import uuid4
from .entities import Incidente, Servicio
from .enums import Impacto, Urgencia
from .strategies import EstrategiaPriorizacion


class FabricaIncidentes:
    def __init__(self, estrategia: EstrategiaPriorizacion) -> None:
        self._estrategia = estrategia

    def crear(self, titulo: str, descripcion: str, servicio: Servicio,
              impacto: Impacto, urgencia: Urgencia, ahora: datetime) -> Incidente:
        prioridad = self._estrategia.calcular(impacto, urgencia, servicio.critico)
        return Incidente(uuid4(), titulo, descripcion, servicio, impacto, urgencia, prioridad, ahora)

