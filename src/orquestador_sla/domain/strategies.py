from abc import ABC, abstractmethod
from .enums import Impacto, Prioridad, Urgencia


class EstrategiaPriorizacion(ABC):
    @abstractmethod
    def calcular(self, impacto: Impacto, urgencia: Urgencia, servicio_critico: bool) -> Prioridad:
        raise NotImplementedError


class PriorizacionPorRiesgo(EstrategiaPriorizacion):
    def calcular(self, impacto: Impacto, urgencia: Urgencia, servicio_critico: bool) -> Prioridad:
        puntaje = impacto.value + urgencia.value + (2 if servicio_critico else 0)
        if puntaje >= 7:
            return Prioridad.P1
        if puntaje >= 5:
            return Prioridad.P2
        if puntaje >= 3:
            return Prioridad.P3
        return Prioridad.P4


class PriorizacionConservadora(EstrategiaPriorizacion):
    """Alternativa polimórfica para equipos que reservan P1 a fallos extremos."""
    def calcular(self, impacto: Impacto, urgencia: Urgencia, servicio_critico: bool) -> Prioridad:
        if impacto is Impacto.ALTO and urgencia is Urgencia.ALTA and servicio_critico:
            return Prioridad.P1
        if impacto.value + urgencia.value >= 5:
            return Prioridad.P2
        return Prioridad.P3

