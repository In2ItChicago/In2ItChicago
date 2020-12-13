CREATE TABLE events.organization
(
    id SERIAL,
    name VARCHAR(256) NOT NULL,
    CONSTRAINT events_organization_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE INDEX org_text_search ON events.organization USING GIN((
    setweight(to_tsvector('english', name), 'A')));

ALTER TABLE events.Organization
    OWNER to postgres;
