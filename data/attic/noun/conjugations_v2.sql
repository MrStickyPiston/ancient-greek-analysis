DELETE FROM noun_conjugation_table WHERE true;

-- All groups formatted as [DECLENSION-N][GENDER-L]-[PRONUNCIATION-L]-[ENDING-S]

--- First declension

-- Feminine long
INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, prefix_without_accents, suffix_without_accents, morphological_amount, morphological_case) VALUES
                                                                                                                                                                     ('1f-l-α', '', 'ᾱ', '', 'α', 0, 0),
                                                                                                                                                                     ('1f-l-α', '', 'ᾱ', '', 'α', 1, 0),
                                                                                                                                                                     ('1f-l-α', '', 'αι', '', 'αι', 2, 0),
                                                                                                                                                                     ('1f-l-α', '', 'ᾱς', '', 'ας', 0, 1),
                                                                                                                                                                     ('1f-l-α', '', 'αιν', '', 'αιν', 1, 1),
                                                                                                                                                                     ('1f-l-α', '', 'ῶν', '', 'ων', 2, 1),
                                                                                                                                                                     ('1f-l-α', '', 'ᾳ', '', 'ᾳ', 0, 2),
                                                                                                                                                                     ('1f-l-α', '', 'αιν', '', 'αιν', 1, 2),
                                                                                                                                                                     ('1f-l-α', '', 'αις', '', 'αις', 2, 2),
                                                                                                                                                                     ('1f-l-α', '', 'ᾱν', '', 'αν', 0, 3),
                                                                                                                                                                     ('1f-l-α', '', 'ᾱ', '', 'α', 1, 3),
                                                                                                                                                                     ('1f-l-α', '', 'ᾱς', '', 'ας', 2, 3),
                                                                                                                                                                     ('1f-l-α', '', 'ᾱ', '', 'α', 0, 4),
                                                                                                                                                                     ('1f-l-α', '', 'ᾱ', '', 'α', 1, 4),
                                                                                                                                                                     ('1f-l-α', '', 'αι', '', 'αι', 2, 4);
INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, prefix_without_accents, suffix_without_accents, morphological_amount, morphological_case) VALUES
                                                                                                                                                                     ('1f-l-ά', '', 'ᾱ́', '', 'α', 0, 0),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾱ́', '', 'α', 1, 0),
                                                                                                                                                                     ('1f-l-ά', '', 'αί', '', 'αι', 2, 0),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾶς', '', 'ας', 0, 1),
                                                                                                                                                                     ('1f-l-ά', '', 'αῖν', '', 'αιν', 1, 1),
                                                                                                                                                                     ('1f-l-ά', '', 'ῶν', '', 'ων', 2, 1),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾷ', '', 'ᾳ', 0, 2),
                                                                                                                                                                     ('1f-l-ά', '', 'αῖν', '', 'αιν', 1, 2),
                                                                                                                                                                     ('1f-l-ά', '', 'αῖς', '', 'αις', 2, 2),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾱ́ν', '', 'αν', 0, 3),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾱ́', '', 'α', 1, 3),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾱ́ς', '', 'ας', 2, 3),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾱ́', '', 'α', 0, 4),
                                                                                                                                                                     ('1f-l-ά', '', 'ᾱ́', '', 'α', 1, 4),
                                                                                                                                                                     ('1f-l-ά', '', 'αί', '', 'αι', 2, 4);

INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, prefix_without_accents, suffix_without_accents, morphological_amount, morphological_case) VALUES
                                                                                                                                                                     ('1f-l-ή', '', 'ή', '', 'η', 0, 0),
                                                                                                                                                                     ('1f-l-ή', '', 'ᾱ́', '', 'α', 1, 0),
                                                                                                                                                                     ('1f-l-ή', '', 'αί', '', 'αι', 2, 0),
                                                                                                                                                                     ('1f-l-ή', '', 'ῆς', '', 'ης', 0, 1),
                                                                                                                                                                     ('1f-l-ή', '', 'αῖν', '', 'αιν', 1, 1),
                                                                                                                                                                     ('1f-l-ή', '', 'ῶν', '', 'ων', 2, 1),
                                                                                                                                                                     ('1f-l-ή', '', 'ῇ', '', 'ῃ', 0, 2),
                                                                                                                                                                     ('1f-l-ή', '', 'αῖν', '', 'αιν', 1, 2),
                                                                                                                                                                     ('1f-l-ή', '', 'αῖς', '', 'αις', 2, 2),
                                                                                                                                                                     ('1f-l-ή', '', 'ήν', '', 'ην', 0, 3),
                                                                                                                                                                     ('1f-l-ή', '', 'ᾱ́', '', 'α', 1, 3),
                                                                                                                                                                     ('1f-l-ή', '', 'ᾱ́ς', '', 'ας', 2, 3),
                                                                                                                                                                     ('1f-l-ή', '', 'ή', '', 'η', 0, 4),
                                                                                                                                                                     ('1f-l-ή', '', 'ᾱ́', '', 'α', 1, 4),
                                                                                                                                                                     ('1f-l-ή', '', 'αί', '', 'αι', 2, 4);

-- Feminine short

-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείᾱ'. Using prefix '' and suffix 'ᾱ', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείᾱς'. Using prefix '' and suffix 'ᾱς', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείαιν'. Using prefix '' and suffix 'αιν', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθειῶν'. Using prefix '' and suffix 'ῶν', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείᾳ'. Using prefix '' and suffix 'ίᾳ', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείαιν'. Using prefix '' and suffix 'αιν', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείαις'. Using prefix '' and suffix 'αις', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείᾱ'. Using prefix '' and suffix 'ᾱ', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείᾱς'. Using prefix '' and suffix 'ᾱς', but a manual check is recommended.
-- WARNING: root with different accent for conjugation 'ᾰ̓ληθείᾱ'. Using prefix '' and suffix 'ᾱ', but a manual check is recommended.
INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, prefix_without_accents, suffix_without_accents, morphological_amount, morphological_case) VALUES
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾰ', '', 'α', 0, 0),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾱ', '', 'α', 1, 0),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'αι', '', 'αι', 2, 0),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾱς', '', 'ας', 0, 1),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'αιν', '', 'αιν', 1, 1),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ῶν', '', 'ων', 2, 1),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ίᾳ', '', 'ιᾳ', 0, 2),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'αιν', '', 'αιν', 1, 2),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'αις', '', 'αις', 2, 2),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾰν', '', 'αν', 0, 3),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾱ', '', 'α', 1, 3),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾱς', '', 'ας', 2, 3),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾰ', '', 'α', 0, 4),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'ᾱ', '', 'α', 1, 4),
                                                                                                                                                                     ('1f-s-ᾰ', '', 'αι', '', 'αι', 2, 4);
-- η not in attic, https://en.wikipedia.org/wiki/Ancient_Greek_nouns#First_declension

-- Masculine

-- WARNING: root with different accent for conjugation 'νεᾱνῐῶν'. Using prefix '' and suffix 'ῶν', but a manual check is recommended.

INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, prefix_without_accents, suffix_without_accents, morphological_amount, morphological_case) VALUES
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾱς', '', 'ας', 0, 0),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾱ', '', 'α', 1, 0),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'αι', '', 'αι', 2, 0),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ου', '', 'ου', 0, 1),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'αιν', '', 'αιν', 1, 1),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ῶν', '', 'ων', 2, 1),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾳ', '', 'ᾳ', 0, 2),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'αιν', '', 'αιν', 1, 2),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'αις', '', 'αις', 2, 2),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾱν', '', 'αν', 0, 3),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾱ', '', 'α', 1, 3),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾱς', '', 'ας', 2, 3),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾱ', '', 'α', 0, 4),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'ᾱ', '', 'α', 1, 4),
                                                                                                                                                                     ('1m-l-ᾱς', '', 'αι', '', 'αι', 2, 4);

INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, prefix_without_accents, suffix_without_accents, morphological_amount, morphological_case) VALUES
                                                                                                                                                                     ('1m-l-ής', '', 'ής', '', 'ης', 0, 0),
                                                                                                                                                                     ('1m-l-ής', '', 'ᾱ́', '', 'α', 1, 0),
                                                                                                                                                                     ('1m-l-ής', '', 'αί', '', 'αι', 2, 0),
                                                                                                                                                                     ('1m-l-ής', '', 'οῦ', '', 'ου', 0, 1),
                                                                                                                                                                     ('1m-l-ής', '', 'αῖν', '', 'αιν', 1, 1),
                                                                                                                                                                     ('1m-l-ής', '', 'ῶν', '', 'ων', 2, 1),
                                                                                                                                                                     ('1m-l-ής', '', 'ῇ', '', 'ῃ', 0, 2),
                                                                                                                                                                     ('1m-l-ής', '', 'αῖν', '', 'αιν', 1, 2),
                                                                                                                                                                     ('1m-l-ής', '', 'αῖς', '', 'αις', 2, 2),
                                                                                                                                                                     ('1m-l-ής', '', 'ήν', '', 'ην', 0, 3),
                                                                                                                                                                     ('1m-l-ής', '', 'ᾱ́', '', 'α', 1, 3),
                                                                                                                                                                     ('1m-l-ής', '', 'ᾱ́ς', '', 'ας', 2, 3),
                                                                                                                                                                     ('1m-l-ής', '', 'ᾰ́', '', 'α', 0, 4),
                                                                                                                                                                     ('1m-l-ής', '', 'ᾱ́', '', 'α', 1, 4),
                                                                                                                                                                     ('1m-l-ής', '', 'αί', '', 'αι', 2, 4);

--- Second declension

-- TODO: check https://en.wikipedia.org/wiki/Ancient_Greek_nouns#Second_declension root accent changes