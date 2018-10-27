-- Verify lexicount:table.public.blog_details on pg

BEGIN;

SET ROLE sqitch;

SELECT url, word, count FROM public.blog_details;

ROLLBACK;
