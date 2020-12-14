CREATE TABLE events.recurring_event
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
    requires_physical_activities BOOLEAN NOT NULL DEFAULT FALSE,
    handicap_accessible BOOLEAN NOT NULL DEFAULT FALSE,
    monthly_recurring_schedule_id INT REFERENCES events.monthly_recurring_schedule(id),
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT events_recurring_event_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


ALTER TABLE events.recurring_event
    OWNER to postgres;
