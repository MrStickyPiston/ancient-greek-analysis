DELETE FROM noun_roots_table WHERE true;

INSERT INTO noun_roots_table (root, root_without_accents, conjugation_group, gender, exact) VALUES
    -- Nominative singular ending with -ος
    ('λόγ', 'λογ', 'λόγος', 0, true),

    -- TODO: check if really exact match
    ('ἄνθρωπ', 'ἀνθρωπ', 'ἄνθρωπος', 2, false),
--     ('ἔθν', 'ἐθν', 'ἔθνος', 3, false),          -- fairly similar but somewhat different
    ('κῆπ', 'κηπ', 'κῆπος', 0, false),

    ('κῠ́κλ', 'κυκλ', 'λόγος', 0, true),
    ('κῠ́κλ', 'κυκλ', 'κῠ́κλᾰ', 0, true),               -- Special plural

    ('μῦθ', 'μυθ', 'μῦθος', 0, false),
    ('νόμ', 'νομ', 'λόγος', 0, true),
    ('ποταμ', 'ποταμ', 'λόγος', 0, false),
    ('στόλ', 'στολ', 'λόγος', 0, true),
    ('τρόπ', 'τροπ', 'λόγος', 0, true),

    -- Nominative singular ending with ᾱ́
    ('θε', 'θε', 'θεᾱ́', 1, true),

    -- Nominative singular ending with ᾱ
    ('θέ', 'θε', 'θεᾱ́', 1, false),
    ('ἡμέρ', 'ἡμερ', 'θεᾱ́', 1, false),

    -- Nominative singular ending with ή
    ('τῑμ', 'τιμ', 'τῑμή', 1, true),
    ('μᾰ́χ', 'μαχ', 'τῑμή', 1, false);