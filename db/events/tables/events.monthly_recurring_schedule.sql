CREATE TABLE events.monthly_recurring_schedule
(
    id SERIAL,
    weekday TEXT,
    week_number INT,
    day_of_month INT,
    recurring_event_id INT NOT NULL REFERENCES events.recurring_event (id),
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT events_monthly_recurring_schedule_pkey PRIMARY KEY (id),
    UNIQUE(weekday, day_of_month, recurring_event_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


ALTER TABLE events.monthly_recurring_schedule
    OWNER to postgres;
