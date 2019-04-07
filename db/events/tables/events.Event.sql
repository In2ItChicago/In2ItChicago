CREATE TABLE events.Event
(
    id SERIAL,
    title VARCHAR(256) NOT NULL,
    url VARCHAR(256) NOT NULL,
    description VARCHAR(5000) NOT NULL,
    organization VARCHAR(256) NOT NULL,
    price DECIMAL(5,2),
    geocode_id INT REFERENCES geocode.Location(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    category VARCHAR(256),
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT events_event_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE events.Event
    OWNER to postgres;