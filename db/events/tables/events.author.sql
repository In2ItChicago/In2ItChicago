CREATE TABLE events.author
(
    id SERIAL,
    name TEXT NOT NULL,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT events_author_pkey PRIMARY KEY (id),
    UNIQUE(name)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE events.author
    OWNER to postgres;
