BEGIN;

INSERT INTO users (username, password_hash, role, parroquia_id)
VALUES
    ('parroquia1', '$2b$12$XyWgbz6WP/lua1ol3l.5XOSrWh1GhxhPbNrn24zXX2SeIBdnsiNFC', 'parroquia', NULL),
    ('admin', '$2b$12$0jSSZvyOM.rEoQr1o2buienH7AUWvD6u13kURPKObfjdsqZdtY3SS', 'admin', NULL),
    ('contador', '$2b$12$Osrmg19CEyU2skEPPa8bjebV2CL03QsP58qcCL8IIZq6VGVwpPibO', 'contador', NULL)
ON CONFLICT (username) DO UPDATE SET
    password_hash = EXCLUDED.password_hash,
    role = EXCLUDED.role,
    parroquia_id = EXCLUDED.parroquia_id;

COMMIT;
