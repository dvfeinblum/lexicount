-- Verify lexicount:role.blog_parser on pg

BEGIN;

SET ROLE blog_parser;

SELECT has_table_privilege('public.blog_details', 'UPDATE');
SELECT has_table_privilege('public.blog_details', 'INSERT');
SELECT has_table_privilege('public.blog_details', 'SELECT');

SELECT has_table_privilege('public.word_details', 'UPDATE');
SELECT has_table_privilege('public.word_details', 'INSERT');
SELECT has_table_privilege('public.word_details', 'SELECT');

ROLLBACK;
