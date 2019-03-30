CREATE TABLE scheduler.JobAuditLog
(
    job_id text COLLATE pg_catalog."default" NOT NULL REFERENCES scheduler.Jobs(id),
    job_name text COLLATE pg_catalog."default" NOT NULL,
    event integer NOT NULL,
    "user" text COLLATE pg_catalog."default",
    created_time timestamp with time zone NOT NULL,
    description text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE scheduler.JobAuditlog
    OWNER to postgres;