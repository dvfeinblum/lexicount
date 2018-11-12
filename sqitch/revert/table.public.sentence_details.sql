-- Revert lexicount:table.public.sentence_details from pg

BEGIN;

SET ROLE sqitch;

DROP TABLE IF EXISTS public.sentence_details;

COMMIT;
