-- Revert lexicount:role.blog_parser from pg

BEGIN;

SET ROLE sqitch;

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT *
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'blog_parser') THEN
          REVOKE ALL PRIVILEGES ON table "blog_details" from blog_parser;
          REVOKE ALL PRIVILEGES ON table "word_details" from blog_parser;
          DROP ROLE blog_parser;
   END IF;
END
$do$;

COMMIT;
