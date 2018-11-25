-- Deploy lexicount:table.public.sentence_details to pg

BEGIN;

SET ROLE sqitch;

CREATE TABLE IF NOT EXISTS public.sentence_details (
    sentence       VARCHAR(1000),
    url            VARCHAR(100),
    length         INTEGER,
    vector         DECIMAL[],
    PRIMARY KEY(sentence, url)
);

GRANT SELECT, INSERT, UPDATE ON public.sentence_details to blog_parser;

COMMIT;
