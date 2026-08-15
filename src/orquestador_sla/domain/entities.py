from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from .enums import Impacto, Prioridad, Urgencia
from .events import EventoDominio
from .states import EstadoIncidente, Reportado


@dataclass(slots=True)
class Servicio:
    codigo: str
    nombre: str
    critico: bool = False


@dataclass(slots=True)
class Equipo:
    codigo: str
    nombre: str
    especialidades: set[str]

    def puede_atender(self, servicio: Servicio) -> bool:
        return servicio.codigo in self.especialidades


@dataclass(slots=True)
class Incidente:
    id: UUID
    titulo: str
    descripcion: str
    servicio: Servicio
    impacto: Impacto
    urgencia: Urgencia
    prioridad: Prioridad
    creado_en: datetime
    _estado: EstadoIncidente = field(default_factory=Reportado, repr=False)
    _equipo: Equipo | None = field(default=None, repr=False)
    _eventos: list[EventoDominio] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if not self.titulo.strip() or not self.descripcion.strip():
            raise ValueError("Título y descripción son obligatorios")

    @property
    def estado(self) -> str:
        return self._estado.nombre

    @property
    def equipo(self) -> Equipo | None:
        return self._equipo

    def asignar(self, equipo: Equipo, ahora: datetime) -> None:
        if not equipo.puede_atender(self.servicio):
            raise ValueError("El equipo no tiene la especialidad requerida")
        self._estado = self._estado.asignar()
        self._equipo = equipo
        self._registrar("incidente_asignado", ahora, equipo=equipo.nombre)

    def iniciar_diagnostico(self, ahora: datetime) -> None:
        self._estado = self._estado.iniciar()
        self._registrar("diagnostico_iniciado", ahora)

    def resolver(self, ahora: datetime, causa: str) -> None:
        if not causa.strip():
            raise ValueError("La causa de resolución es obligatoria")
        self._estado = self._estado.resolver()
        self._registrar("incidente_resuelto", ahora, causa=causa)

    def cerrar(self, ahora: datetime) -> None:
        self._estado = self._estado.cerrar()
        self._registrar("incidente_cerrado", ahora)

    def extraer_eventos(self) -> list[EventoDominio]:
        eventos, self._eventos = self._eventos.copy(), []
        return eventos

    def _registrar(self, nombre: str, ahora: datetime, **datos: str) -> None:
        self._eventos.append(EventoDominio(nombre, ahora, {"incidente_id": str(self.id), **datos}))

