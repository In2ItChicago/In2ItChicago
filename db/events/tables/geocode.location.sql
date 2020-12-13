CREATE TABLE geocode.location (
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

ALTER TABLE geocode.location
    OWNER to postgres;

CREATE EXTENSION cube schema pg_catalog;
CREATE EXTENSION earthdistance schema pg_catalog;

CREATE INDEX lat_lon_distance
ON geocode.location
USING gist(ll_to_earth(lat, lon))
WHERE lat IS NOT NULL AND Lon IS NOT NULL AND Lat != 'NaN' AND Lon != 'NaN';