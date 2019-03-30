CREATE TABLE events.Event
(
    id serial,
    title varchar(256) COLLATE pg_catalog."default" NOT NULL,
    url varchar(256) COLLATE pg_catalog."default" NOT NULL,
    description varchar(5000) COLLATE pg_catalog."default" NOT NULL,
    organization varchar(256) COLLATE pg_catalog."default" NOT NULL,
    price decimal(5,2) NOT NULL,
    geocode_id int REFERENCES geocode.Location(id),
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    start_timestamp int,
    end_timestamp int,
    created_date timestamp with time zone,
    CONSTRAINT events_event_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE events.Event
    OWNER to postgres;