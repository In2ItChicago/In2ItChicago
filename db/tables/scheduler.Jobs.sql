CREATE TABLE scheduler.Jobs
(
    id character varying(191) COLLATE pg_catalog."default" NOT NULL,
    next_run_time double precision,
    job_state bytea NOT NULL,
    CONSTRAINT scheduler_jobs_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.scheduler_jobs
    OWNER to postgres;

-- Index: ix_scheduler_jobs_next_run_time

-- DROP INDEX public.ix_scheduler_jobs_next_run_time;

CREATE INDEX ix_scheduler_jobs_next_run_time
    ON public.scheduler_jobs USING btree
    (next_run_time)
    TABLESPACE pg_default;