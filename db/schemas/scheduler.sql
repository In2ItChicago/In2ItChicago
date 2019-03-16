CREATE SCHEMA scheduler
    AUTHORIZATION postgres;

COMMENT ON SCHEMA scheduler
    IS 'standard public schema';

GRANT ALL ON SCHEMA scheduler TO postgres;

GRANT ALL ON SCHEMA scheduler TO PUBLIC;