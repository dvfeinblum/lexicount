-- Verify lexicount:table.public.sentence_details on pg

BEGIN;

SELECT url, sentence, length, vector FROM public.sentence_details;

ROLLBACK;
