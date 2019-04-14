CREATE TABLE geocode.Location (
    id SERIAL,
    address VARCHAR(256) NOT NULL,
    lat DECIMAL(23,20),
    lon DECIMAL(23,20),
    neighborhood VARCHAR(256),
    expire_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT geocode_Location_pkey PRIMARY KEY (id)
)

WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE geocode.Location
    OWNER to postgres;