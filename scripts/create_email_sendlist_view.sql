-- One row per unique email address, safe to merge into a campaign.
--
-- Why this exists: `contacts` is keyed by title record, not by person. One
-- human can hold several rows because they own several properties or vest
-- under several entities. richardkay@sbcglobal.net has 4 rows (a trust, a
-- personal vesting, an LLC, and a property-derived row) all mailing to the
-- same house. Sending straight from `contacts` mails him four copies.
--
-- Those rows are NOT duplicates to delete. Each is a real title record and
-- deleting any of them loses property data. So collapse at send time instead.
--
-- Opt-out is treated as a property of the PERSON, not the row: if any row for
-- an address is do_not_contact or bounced, the whole address is withheld.
-- Otherwise one stray title record could resurrect someone who asked to stop.

DROP VIEW IF EXISTS email_sendlist;

CREATE VIEW email_sendlist AS
SELECT
    lower(trim(email))              AS email,
    -- max() ignores NULLs, so a named row wins over unnamed rows for the
    -- same person. Groups never disagree on the name; where no row resolved
    -- a name this stays NULL and templates fall back to "Hi there,".
    max(greeting_name)              AS greeting_name,
    max(city)                       AS city,
    max(mailing_address)            AS mailing_address,
    max(phone)                      AS phone,
    count(*)                        AS title_records,
    group_concat(id, ',')           AS contact_ids
FROM contacts
WHERE email IS NOT NULL
  AND trim(email) != ''
GROUP BY lower(trim(email))
HAVING sum(
    CASE WHEN status IN ('do_not_contact', 'bounced') THEN 1 ELSE 0 END
) = 0;
