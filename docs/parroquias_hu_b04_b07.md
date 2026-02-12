# HU-B04/B05/B06/B07 - Estado de Implementacion

Fecha: 2026-02-12
Modulo: `parroquias`
Base path: `/api/v1/parroquias`

## 1) Alcance completado
Endpoints implementados:
- `GET /api/v1/parroquias?page=1&size=25`
- `GET /api/v1/parroquias/{parroquia_id}`
- `POST /api/v1/parroquias`
- `PATCH /api/v1/parroquias/{parroquia_id}`

## 2) Reglas de acceso por rol
- `GET /parroquias`: `admin`, `contador`
- `GET /parroquias/{id}`: `admin`, `contador`
- `POST /parroquias`: `admin`
- `PATCH /parroquias/{id}`: `admin`

Implementado mediante dependencias comunes:
- `Backend/app/api/deps.py`

## 3) Comportamiento funcional
- Listado con paginacion (`page`, `size`) usando `offset/limit`.
- Detalle por id con `404` si no existe.
- Creacion con validacion de nombre unico (`409` si duplicado).
- Actualizacion parcial (`PATCH`) con `404` si no existe.
- Validaciones de schema:
- `nombre`: requerido en create, opcional en patch, max 255.
- `cuota_mensual`: no negativa.

## 4) Archivos clave
- `Backend/app/api/v1/endpoints/parroquias.py`
- `Backend/app/models/parroquia.py`
- `Backend/app/schemas/parroquia.py`
- `Backend/app/api/v1/api.py`
- `Backend/app/db/base.py`
- `Backend/sql/schema.sql`

## 5) Base de datos
Tabla:
- `parroquias(id, nombre, cuota_mensual, datos_bancarios)`

Restricciones:
- `nombre` definido como `UNIQUE` en `Backend/sql/schema.sql`.
- Si la tabla existia antes de ese cambio, aplicar:
```sql
ALTER TABLE parroquias ADD CONSTRAINT uq_parroquias_nombre UNIQUE (nombre);
```

## 6) Pruebas manuales recomendadas
Desde `http://127.0.0.1:8000/docs`:
- `admin`: debe poder listar, ver detalle, crear y actualizar.
- `contador`: debe poder listar y ver detalle; `POST/PATCH` deben responder `403`.
- id inexistente en detalle/update -> `404`.
- crear/actualizar con nombre duplicado -> `409`.
