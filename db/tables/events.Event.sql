CREATE TABLE events.Event
(
    eid character varying(191) COLLATE pg_catalog."default" NOT NULL,
    hostname text COLLATE pg_catalog."default",
    pid integer,
    state integer NOT NULL,
    scheduled_time timestamp with time zone NOT NULL,
    updated_time timestamp with time zone,
    description text COLLATE pg_catalog."default",
    result text COLLATE pg_catalog."default",
    job_id text COLLATE pg_catalog."default" NOT NULL,
    task_id text COLLATE pg_catalog."default",
    CONSTRAINT scheduler_execution_pkey PRIMARY KEY (eid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE events.Event
    OWNER to postgres;