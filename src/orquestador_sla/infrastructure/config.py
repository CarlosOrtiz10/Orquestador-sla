from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class ConfiguracionSLA:
    minutos_p1: int = 15
    minutos_p2: int = 60
    minutos_p3: int = 240
    minutos_p4: int = 480
    _instancia: ClassVar["ConfiguracionSLA | None"] = None

    @classmethod
    def instancia(cls) -> "ConfiguracionSLA":
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia
