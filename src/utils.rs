use unicode_normalization::{UnicodeNormalization, char::is_combining_mark};

const ALLOWED_ACCENTS: [char; 3] = ['̓', '̔', 'ͅ'];

pub(crate) fn without_accents<T: AsRef<str>>(input: T) -> String {
    input.as_ref().nfd()
        .filter(|c| !is_combining_mark(*c) || ALLOWED_ACCENTS.contains(c))
        .collect()
}

#[test]
fn test_without_accents() {
    // Filter out accents, but not spiriti or iota subscript
    assert_eq!(without_accents("Ὁ ἄνθρωπος ἀγαθός"), "Ὁ ἀνθρωπος ἀγαθος");
}