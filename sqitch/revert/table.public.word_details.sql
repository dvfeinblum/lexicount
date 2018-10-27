-- Revert lexicount:table.public.word_details from pg

BEGIN;

SET ROLE sqitch;

DROP TABLE IF EXISTS public.word_details;

COMMIT;
