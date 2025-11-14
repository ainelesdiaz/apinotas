# API de Notas (FastAPI)

Proyecto mínimo con CRUD de notas usando FastAPI y SQLite (SQLModel).

Requisitos
- Python 3.9+

Instalación
```powershell
python -m pip install -r requirements.txt
```

Ejecutar servidor
```powershell
uvicorn main:app --reload
```

Endpoints
- POST /notes  -> Crear nota
- GET /notes   -> Listar notas
- GET /notes/{id} -> Obtener una nota
- PUT /notes/{id} -> Actualizar una nota
- DELETE /notes/{id} -> Eliminar una nota

Tests
```powershell
pytest -q
```
