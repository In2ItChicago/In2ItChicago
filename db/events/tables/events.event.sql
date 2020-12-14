CREATE TABLE events.event
(
    id SERIAL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(5,2),
    geocode_id INT REFERENCES geocode.location(id),
    organization_id INT REFERENCES events.organization(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    handicap_accessible BOOLEAN NOT NULL DEFAULT FALSE,
    requires_physical_activities BOOLEAN NOT NULL DEFAULT FALSE,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT events_event_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE INDEX event_text_search ON events.event USING GIN((
    setweight(to_tsvector('english', title), 'B') || 
    setweight(to_tsvector('english', description), 'C')));


ALTER TABLE events.event
    OWNER to postgres;
