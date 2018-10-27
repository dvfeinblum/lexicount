-- Deploy lexicount:role.blog_parser to pg

BEGIN;

SET ROLE sqitch;

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT *
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'blog_parser') THEN
        CREATE ROLE blog_parser LOGIN;
   END IF;
END
$do$;

GRANT SELECT, INSERT, UPDATE ON public.blog_details to blog_parser;
GRANT SELECT, INSERT, UPDATE ON public.word_details to blog_parser;

COMMIT;
