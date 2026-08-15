from .ports import ObservadorEventos
from ..domain.events import EventoDominio


class BusEventos:
    def __init__(self) -> None:
        self._observadores: list[ObservadorEventos] = []

    def suscribir(self, observador: ObservadorEventos) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def publicar(self, eventos: list[EventoDominio]) -> None:
        for evento in eventos:
            for observador in tuple(self._observadores):
                observador.actualizar(evento)

