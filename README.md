# Orquestador de incidentes y SLA

Proyecto académico profesional en Python que demuestra POO, arquitectura modular,
SOLID y patrones de diseño mediante la gestión del ciclo de vida de incidentes.

## Ejecutar

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -e .
python -m orquestador_sla.main
python -m unittest discover -s tests -v  # después de pip install -e .
```

## Patrones aplicados

- Factory Method: creación consistente de incidentes.
- Strategy: cálculo de prioridad sustituible.
- Observer: notificaciones desacopladas por eventos.
- State: transiciones válidas del ciclo de vida.
- Repository: persistencia abstraída.
- Singleton: configuración única del SLA.

La aplicación usa únicamente la biblioteca estándar de Python.
