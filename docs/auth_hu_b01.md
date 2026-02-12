# HU-B01/B02/B03 - Estado de Implementacion

Fecha: 2026-02-12
Modulo: `auth`
Base path: `/api/v1/auth`

## 1) Alcance completado
Endpoints implementados:
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`

Componentes:
- Seguridad JWT (`access` y `refresh`)
- Hash/verificacion de contrasenas con `bcrypt`
- Capa SQLAlchemy para conexion/sesion
- Modelo `users` y datos semilla

## 2) Archivos clave
- `Backend/app/api/v1/endpoints/auth.py`
- `Backend/app/core/security.py`
- `Backend/app/api/deps.py`
- `Backend/app/models/user.py`
- `Backend/sql/schema.sql`
- `Backend/sql/seed_auth.sql`

## 3) Configuracion de entorno
Variables usadas en `.env`:
- `PROJECT_NAME`
- `API_V1_STR`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES=15`
- `REFRESH_TOKEN_EXPIRE_DAYS=7`
- `DATABASE_URL`

## 4) Datos de prueba
Usuarios seed:
- `parroquia1 / pass123` (`parroquia`)
- `admin / admin123` (`admin`)
- `contador / cont123` (`contador`)

## 5) Flujo de autenticacion
1. `login` valida credenciales y emite `access_token` + `refresh_token`.
2. `refresh` acepta solo token tipo `refresh` y devuelve nuevo `access_token`.
3. `me` acepta solo token tipo `access` y devuelve datos publicos del usuario.

## 6) Ejecucion y pruebas
Arranque desde `Backend/`:
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Pruebas manuales via Swagger:
- URL: `http://127.0.0.1:8000/docs`
- Casos minimos:
- login valido -> `200`
- login invalido -> `401`
- refresh con refresh token -> `200`
- refresh con access token -> `401`
- me con access token -> `200`
