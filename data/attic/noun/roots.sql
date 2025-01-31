DELETE FROM noun_roots_table WHERE true;

INSERT INTO noun_roots_table (root, root_without_accents, conjugation_group, gender, exact, metadata) VALUES
    -- Nominative singular ending with -ος
    ('λόγ', 'λογ', 'λόγος', 0, true, '{"wiktionary_id": "%CE%BB%CF%8C%CE%B3%CE%BF%CF%82", "definitions": ["That which is said: word, sentence, speech, story, debate, utterance, argument", "That which is thought: reason, consideration, computation, reckoning.", "An account, explanation, or narrative.", "Subject matter.", " The word or wisdom of God, identified with Jesus in the New Testament, by whom the world was created; God the Son."]}'),

    -- TODO: check if really exact match
    ('ἄνθρωπ', 'ἀνθρωπ', 'λόγος', 2, false,'{"wiktionary_id": "%E1%BC%84%CE%BD%CE%B8%CF%81%CF%89%CF%80%CE%BF%CF%82", "definitions": ["human being, person ; man, woman", " man, humanity", " all human beings, mankind", " female slave"]}'),
    --     ('ἔθν', 'ἐθν', 'ἔθνος', 3, false),          -- fairly similar but somewhat different
    ('κῆπ', 'κηπ', 'λόγος', 0, false, '{"wiktionary_id": "%CE%BA%E1%BF%86%CF%80%CE%BF%CF%82", "definitions": ["garden, orchard or plantation", "enclosure for the Olympic games", "sort of fashion of cropping the hair", "female genitals"]}'),

    ('κῠ́κλ', 'κυκλ', 'λόγος', 0, true, '{"wiktionary_id": "%CE%BA%CF%8D%CE%BA%CE%BB%CE%BF%CF%82", "definitions": ["circle, ring", "Any circular object, such as a wheel", "A crowd of people", "marketplace", "circular movement", "sphere, globe"]}'),
    ('κῠ́κλ', 'κυκλ', 'κῠ́κλᾰ', 0, true, '{"wiktionary_id": "%CE%BA%CF%8D%CE%BA%CE%BB%CE%BF%CF%82", "definitions": ["circle, ring", "Any circular object, such as a wheel", "A crowd of people", "marketplace", "circular movement", "sphere, globe"]}'),               -- Special plural

    ('μῦθ', 'μυθ', 'λόγος', 0, false, '{"wiktionary_id": "%CE%BC%E1%BF%A6%CE%B8%CE%BF%CF%82", "definitions": ["something said: word, speech, conversation", "public speech", "talk, conversation", "advice, counsel, command, order, promise", "the subject of a speech or talk", "a resolve, purpose, design, plan", "saying, proverb", "the talk of men, rumor, report, message", "public speech", "talk, conversation", "advice, counsel, command, order, promise", "the subject of a speech or talk", "a resolve, purpose, design, plan", "saying, proverb", "the talk of men, rumor, report, message", "tale, story, narrative", "tale, legend, myth", "a legend of the early Greek times, before the dawn of history", "a professed work of fiction, fable, such as those of Aesop", "the plot of a tragedy or comedy", "tale, legend, myth", "a legend of the early Greek times, before the dawn of history", "a legend of the early Greek times, before the dawn of history", "a professed work of fiction, fable, such as those of Aesop", "the plot of a tragedy or comedy"]}'),
    ('νόμ', 'νομ', 'λόγος', 0, true, '{"wiktionary_id": "%CE%BD%CE%BF%CE%BC%CF%8C%CF%82", "definitions": ["pasture, field", "herbage, food", "division, distribution", "dwelling, residence", "district, region, province (particularly of Egypt), satrapy"]}'),
    ('ποταμ', 'ποταμ', 'λόγος', 0, false, '{"wiktionary_id": "ποταμός", "definitions": ["river, stream", "canal"]}'),
    ('στόλ', 'στολ', 'λόγος', 0, true,'{"wiktionary_id": "%CF%83%CF%84%CF%8C%CE%BB%CE%BF%CF%82", "definitions": ["expedition", "army, fleet, troop"]}'),
    ('τρόπ', 'τροπ', 'λόγος', 0, true, '{"wiktionary_id": "%CF%84%CF%81%CF%8C%CF%80%CE%BF%CF%82", "definitions": ["a turn, way, manner, style", "a trope or figure of speech", "a mode in music", "a mode or mood in logic", "the time and space on the battlefield when one side"s belief turns from victory to defeat, the turning point of the battle"]}'),

    -- Nominative singular ending with ᾱ́
    ('θε', 'θε', 'θεᾱ́', 1, true, '{"wiktionary_id": "%CE%B8%CE%B5%CE%AC", "definitions": ["goddess"]}'),

    -- Nominative singular ending with ᾱ
    ('θέ', 'θε', 'θεᾱ́', 1, false,'{"wiktionary_id": "%CE%B8%CE%AD%CE%B1", "definitions": ["view, sight"]}'),
    ('ἡμέρ', 'ἡμερ', 'θεᾱ́', 1, false, '{"wiktionary_id": "%E1%BC%A1%CE%BC%CE%AD%CF%81%CE%B1", "definitions": ["day", "a time of life of a particular type or length", "time", "within a certain number of days; by day; sometime during a particular day", "on a particular day", "for a day or days; after a day or a certain number of days; in the daytime", "within a certain number of days; by day; sometime during a particular day", "on a particular day", "for a day or days; after a day or a certain number of days; in the daytime"]}'),

    -- Nominative singular ending with ή
    ('τῑμ', 'τιμ', 'τῑμή', 1, true, '{"wiktionary_id": "%CF%84%CE%B9%CE%BC%CE%AE", "definitions": ["honor, worship, esteem", "high office, dignity", "gift, offering", "worth, value", "price"]}'),
    ('μᾰ́χ', 'μαχ', 'τῑμή', 1, false, '{"wiktionary_id": "%CE%BC%CE%AC%CF%87%CE%B7", "definitions": ["battle, combat", "quarrel, strife, dispute", "contest, game", "battlefield", "contradiction, inconsistency"]}');