CREATE TABLE events.Organization
(
    id SERIAL,
    name VARCHAR(256) NOT NULL,
    CONSTRAINT events_organization_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE events.Organization
    OWNER to postgres;
