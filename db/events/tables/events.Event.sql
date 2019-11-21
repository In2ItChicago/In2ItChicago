CREATE TABLE events.Event
(
    id SERIAL,
    title VARCHAR(256) NOT NULL,
    url VARCHAR(256) NOT NULL,
    description VARCHAR(5000) NOT NULL,
    organization VARCHAR(256) NOT NULL,
    price DECIMAL(5,2),
    geocode_id INT REFERENCES geocode.Location(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    category VARCHAR(256),
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_manual BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT events_event_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE INDEX organization_search ON events.event USING GIN (to_tsvector('english', organization));
CREATE INDEX event_title_search ON events.event USING GIN (to_tsvector('english', title));
CREATE INDEX event_description_search ON events.event USING GIN (to_tsvector('english', description));


ALTER TABLE events.Event
    OWNER to postgres;
-- http://rachbelaid.com/postgres-full-text-search-is-good-enough/
-- SELECT title, description, ts_rank_cd(to_tsvector(description), query) AS descscore, null as titlescore
-- FROM  events.event, to_tsquery('year') query
-- WHERE description @@ query
-- UNION
-- SELECT title, description, null as descscore, ts_rank_cd(to_tsvector(title), query) AS descscore
-- FROM  events.event, to_tsquery('year') query
-- WHERE title @@ query
-- order by titlescore desc, descscore desc