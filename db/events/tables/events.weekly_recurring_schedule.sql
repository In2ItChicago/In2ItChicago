CREATE TABLE events.weekly_recurring_schedule
(
    id SERIAL,
    recurring_event_id INT NOT NULL REFERENCES events.recurring_event(id),
    weekday TEXT,
    CONSTRAINT events_weekly_recurring_schedule_pkey PRIMARY KEY (id),
    UNIQUE(recurring_event_id, weekday)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


ALTER TABLE events.weekly_recurring_schedule
    OWNER to postgres;
