CREATE TABLE geocode.Location (
    id serial,
    address varchar(256) COLLATE pg_catalog."default" NOT NULL,
    lat decimal(23,20),
    lon decimal(23,20),
    neighborhood varchar(256),
    CONSTRAINT geocode_Location_pkey PRIMARY KEY (id)
)

WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE geocode.Location
    OWNER to postgres;