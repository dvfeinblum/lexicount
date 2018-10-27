-- Revert lexicount:table.public.blog_details from pg

BEGIN;

SET ROLE sqitch;

DROP TABLE IF EXISTS public.blog_details;

COMMIT;
