from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class EventoDominio:
    nombre: str
    ocurrido_en: datetime
    datos: dict[str, Any]

