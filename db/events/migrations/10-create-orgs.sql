DO $$
BEGIN
IF EXISTS (
    SELECT FROM information_schema.columns 
    WHERE table_schema = 'events'
    AND table_name = 'event'
    AND column_name = 'organization'
)
AND NOT EXISTS (
	SELECT FROM information_schema.tables
	WHERE table_schema = 'events'
	AND table_name = 'organization'
)
THEN
    CREATE TABLE events.Organization
    (
        id SERIAL,
        name VARCHAR(256) NOT NULL,
        CONSTRAINT events_organization_pkey PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )
    TABLESPACE pg_default;

    ALTER TABLE events.Organization
    OWNER to postgres;

    INSERT INTO events.organization(name)
	SELECT DISTINCT organization from events.event;
	
	ALTER TABLE events.event
	ADD COLUMN organization_id INT;
	
	UPDATE events.event e
	SET organization_id = o.id
	FROM events.organization o
	WHERE o.name = e.organization;
	
END IF;
END $$;
