DO
$body$
BEGIN
    IF NOT EXISTS(
            SELECT *
            FROM pg_catalog.pg_user
            WHERE usename = 'ss')
    THEN
        CREATE ROLE ss WITH PASSWORD 'pass.word';
    END IF;
END
$body$;

ALTER ROLE ss NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION LOGIN;