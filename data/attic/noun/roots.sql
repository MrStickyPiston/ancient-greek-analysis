DELETE FROM noun_roots_table WHERE true;

INSERT INTO noun_roots_table (root, root_without_accents, conjugation_group, exact)
VALUES
    -- Nominative singular ending with -ος
    ('λόγ', 'λογ', 'λόγος', true),

    -- TODO: check if really exact match
    ('ἀνθρώπ', 'ἀνθρωπ', 'λόγος', true),
    ('δαίμον', 'δαιμον', 'λόγος', true),
    ('ἔθν', 'ἐθν', 'λόγος', true),
    ('κῆπ', 'κηπ', 'λόγος', true),
    ('κύκλ', 'κυκλ', 'λόγος', true),
    ('μῦθ', 'μυθ', 'λόγος', true),
    ('νόμ', 'νομ', 'λόγος', true),
    ('ποταμ', 'ποταμ', 'λόγος', true),
    ('στόλ', 'στολ', 'λόγος', true),
    ('τρόπ', 'τροπ', 'λόγος', true),

    -- Nominative singular ending with ᾱ́
    ('θε', 'θε', 'θεᾱ́', true),      -- Godess

    -- Nominative singular ending with ᾱ
    ('θέ', 'θε', 'θεᾱ́', false),          -- View, sight
    ('ἡμέρ', 'ἡμερ', 'θεᾱ́', false),        -- Day

    -- Nominative singular ending with ή
    ('τῑμ', 'τιμ', 'τῑμή', true),        -- Honor, dignity, gift
    ('μᾰ́χ', 'μαχ', 'τῑμή', false);