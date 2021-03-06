-- Deploy lexicount:table.public.blog_details to pg

BEGIN;

SET ROLE sqitch;

CREATE TABLE IF NOT EXISTS public.blog_details (
    url            VARCHAR(100),
    word           VARCHAR(100),
    count          INTEGER,
    PRIMARY KEY(url, word)
);

COMMIT;
