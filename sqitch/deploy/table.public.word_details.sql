-- Deploy lexicount:table.public.word_details to pg

BEGIN;

SET ROLE sqitch;

CREATE TABLE IF NOT EXISTS public.word_details (
    word           VARCHAR(100) PRIMARY KEY,
    part_of_speech VARCHAR(5),
    count          INTEGER
);

COMMIT;
