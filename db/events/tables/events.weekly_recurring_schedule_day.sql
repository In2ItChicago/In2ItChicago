CREATE TABLE events.weekly_recurring_schedule_day
(
    id SERIAL,
    recurring_event_id INT REFERENCES events.recurring_event(id),
    CONSTRAINT events_weekly_recurring_schedule_day_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


ALTER TABLE events.weekly_recurring_schedule_day
    OWNER to postgres;
