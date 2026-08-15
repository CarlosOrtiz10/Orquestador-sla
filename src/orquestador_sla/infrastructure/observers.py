from ..application.ports import ObservadorEventos
from ..domain.events import EventoDominio


class NotificadorConsola(ObservadorEventos):
    def actualizar(self, evento: EventoDominio) -> None:
        print(f"[NOTIFICACIÓN] {evento.nombre}: {evento.datos}")


class AuditoriaMemoria(ObservadorEventos):
    def __init__(self) -> None:
        self.eventos: list[EventoDominio] = []

    def actualizar(self, evento: EventoDominio) -> None:
        self.eventos.append(evento)

