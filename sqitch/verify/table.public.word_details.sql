-- Verify lexicount:table.public.word_details on pg

BEGIN;

SET ROLE sqitch;

SELECT word, part_of_speech, count FROM public.word_details;

ROLLBACK;
