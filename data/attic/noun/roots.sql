DELETE FROM noun_roots_table WHERE true;

INSERT INTO noun_roots_table (root, conjugation_group)
VALUES
    -- Nominative singular ending with -ος
    ('ἀνθρώπ', 'λόγος'),
    ('δαίμον', 'λόγος'),
    ('ἔθν', 'λόγος'),
    ('κῆπ', 'λόγος'),
    ('κύκλ', 'λόγος'),
    ('λόγ', 'λόγος'),
    ('μῦθ', 'λόγος'),
    ('νόμ', 'λόγος'),
    ('ποταμ', 'λόγος'),
    ('στόλ', 'λόγος'),
    ('τρόπ', 'λόγος'),

    -- Nominative singular ending with ᾱ́
    ('θε', 'θεά'),      -- Godess

    -- Nominative singular ending with ᾱ
    ('θέ', 'θέα'),          -- View, sight
    ('ἡμέρ', 'θέα'),        -- Day

    -- Nominative singular ending with ή
    ('τῑμ', 'τῑμή');        -- Honor, dignity, gift