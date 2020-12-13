CREATE TABLE events.monthly_recurring_schedule
(
    id SERIAL,
    week_day TEXT,
    week_number INT,
    month_day INT,
    CONSTRAINT events_monthly_recurring_schedule_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


ALTER TABLE events.monthly_recurring_schedule
    OWNER to postgres;
