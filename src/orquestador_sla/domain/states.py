from abc import ABC


class EstadoIncidente(ABC):
    nombre = "ABSTRACTO"

    def asignar(self):
        raise ValueError(f"No se puede asignar desde {self.nombre}")

    def iniciar(self):
        raise ValueError(f"No se puede iniciar desde {self.nombre}")

    def resolver(self):
        raise ValueError(f"No se puede resolver desde {self.nombre}")

    def cerrar(self):
        raise ValueError(f"No se puede cerrar desde {self.nombre}")


class Reportado(EstadoIncidente):
    nombre = "REPORTADO"
    def asignar(self): return Asignado()


class Asignado(EstadoIncidente):
    nombre = "ASIGNADO"
    def iniciar(self): return EnDiagnostico()


class EnDiagnostico(EstadoIncidente):
    nombre = "EN_DIAGNOSTICO"
    def resolver(self): return Resuelto()


class Resuelto(EstadoIncidente):
    nombre = "RESUELTO"
    def cerrar(self): return Cerrado()


class Cerrado(EstadoIncidente):
    nombre = "CERRADO"

