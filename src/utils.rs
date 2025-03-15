use unicode_normalization::{UnicodeNormalization, char::is_combining_mark};

// spiritus asper, spritus lenis and iota subscript
const ALLOWED_ACCENTS: [char; 3] = ['̓', '̔', 'ͅ'];

pub(crate) fn without_accents<T: AsRef<str>>(input: T) -> String {
    // Filters out all accents of a word except the ALLOWED_ACCENTS
    input.as_ref().nfd()
        .filter(|c| !is_combining_mark(*c) || ALLOWED_ACCENTS.contains(c))
        .nfc().collect::<String>()
}

#[test]
fn test_without_accents() {
    // Filter out accents, but not spiriti or iota subscript
    assert_eq!(without_accents("Ὁ ἄνθρωπος ἀγαθός"), "Ὁ ἀνθρωπος ἀγαθος");
}