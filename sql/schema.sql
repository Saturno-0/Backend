BEGIN;

CREATE TABLE IF NOT EXISTS parroquias (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    cuota_mensual NUMERIC(12, 2) NOT NULL DEFAULT 0,
    datos_bancarios TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    parroquia_id BIGINT,
    CONSTRAINT ck_users_role CHECK (role IN ('admin', 'parroquia', 'contador')),
    CONSTRAINT fk_users_parroquia FOREIGN KEY (parroquia_id)
        REFERENCES parroquias (id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS conceptos_ingreso (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    es_colecta BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS conceptos_egreso (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    es_colecta BOOLEAN NOT NULL DEFAULT FALSE,
    es_deducible BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ingresos (
    id BIGSERIAL PRIMARY KEY,
    parroquia_id BIGINT NOT NULL,
    concepto_id BIGINT NOT NULL,
    monto NUMERIC(12, 2) NOT NULL,
    fecha DATE NOT NULL,
    mes INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    observaciones TEXT,
    CONSTRAINT ck_ingresos_mes CHECK (mes BETWEEN 1 AND 12),
    CONSTRAINT ck_ingresos_anio CHECK (anio >= 1900),
    CONSTRAINT ck_ingresos_monto CHECK (monto >= 0),
    CONSTRAINT fk_ingresos_parroquia FOREIGN KEY (parroquia_id)
        REFERENCES parroquias (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_ingresos_concepto FOREIGN KEY (concepto_id)
        REFERENCES conceptos_ingreso (id)
);

CREATE TABLE IF NOT EXISTS egresos (
    id BIGSERIAL PRIMARY KEY,
    parroquia_id BIGINT NOT NULL,
    concepto_id BIGINT NOT NULL,
    monto NUMERIC(12, 2) NOT NULL,
    fecha DATE NOT NULL,
    mes INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    proveedor VARCHAR(255),
    numero_factura VARCHAR(120),
    CONSTRAINT ck_egresos_mes CHECK (mes BETWEEN 1 AND 12),
    CONSTRAINT ck_egresos_anio CHECK (anio >= 1900),
    CONSTRAINT ck_egresos_monto CHECK (monto >= 0),
    CONSTRAINT fk_egresos_parroquia FOREIGN KEY (parroquia_id)
        REFERENCES parroquias (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_egresos_concepto FOREIGN KEY (concepto_id)
        REFERENCES conceptos_egreso (id)
);

CREATE TABLE IF NOT EXISTS facturas (
    id BIGSERIAL PRIMARY KEY,
    egreso_id BIGINT NOT NULL UNIQUE,
    s3_url TEXT NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    fecha_carga TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_facturas_egreso FOREIGN KEY (egreso_id)
        REFERENCES egresos (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cuotas_pagos (
    id BIGSERIAL PRIMARY KEY,
    parroquia_id BIGINT NOT NULL,
    mes INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    monto_pagado NUMERIC(12, 2) NOT NULL,
    fecha_pago DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    CONSTRAINT ck_cuotas_mes CHECK (mes BETWEEN 1 AND 12),
    CONSTRAINT ck_cuotas_anio CHECK (anio >= 1900),
    CONSTRAINT ck_cuotas_monto CHECK (monto_pagado >= 0),
    CONSTRAINT ck_cuotas_estado CHECK (estado IN ('pendiente', 'pagado', 'parcial')),
    CONSTRAINT fk_cuotas_parroquia FOREIGN KEY (parroquia_id)
        REFERENCES parroquias (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_users_role ON users (role);
CREATE INDEX IF NOT EXISTS idx_users_parroquia_id ON users (parroquia_id);

CREATE INDEX IF NOT EXISTS idx_ingresos_parroquia_id ON ingresos (parroquia_id);
CREATE INDEX IF NOT EXISTS idx_ingresos_concepto_id ON ingresos (concepto_id);
CREATE INDEX IF NOT EXISTS idx_ingresos_fecha ON ingresos (fecha);

CREATE INDEX IF NOT EXISTS idx_egresos_parroquia_id ON egresos (parroquia_id);
CREATE INDEX IF NOT EXISTS idx_egresos_concepto_id ON egresos (concepto_id);
CREATE INDEX IF NOT EXISTS idx_egresos_fecha ON egresos (fecha);

CREATE INDEX IF NOT EXISTS idx_cuotas_pagos_parroquia_id ON cuotas_pagos (parroquia_id);
CREATE INDEX IF NOT EXISTS idx_cuotas_pagos_mes_anio ON cuotas_pagos (mes, anio);

COMMIT;
