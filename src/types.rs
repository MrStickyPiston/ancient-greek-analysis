use sea_orm::FromQueryResult;

#[derive(Debug)]
#[derive(Clone)]
pub(crate) enum Amount {
    Singular,
    Dual,
    Plural,
    
    Unknown
}

#[derive(Debug)]
#[derive(Clone)]
pub(crate) enum Case {
    Nominative,
    Genitive,
    Dative,
    Accusative,
    Vocative,
    
    Unknown
}

#[derive(Debug)]
#[derive(Clone)]
pub(crate) enum Gender {
    Masculine,
    Feminine,
    MasculineOrFeminine,
    Neuter,
    
    Unknown
}

#[derive(Debug)]
pub(crate) struct NounMorphology {
    pub(crate) prefix: String,
    pub(crate) suffix: String,
    pub(crate) root: String,
    
    pub(crate) amount: Amount,
    pub(crate) case: Case,
    pub(crate) gender: Gender,

    pub(crate) definitions: Vec<String>,
    pub(crate) wiktionary_id: String,
}

pub(crate) fn amount_from_int(n: i32) -> Amount {
    match n {
        0 => Amount::Singular,
        1 => Amount::Dual,
        2 => Amount::Plural,
        _ => Amount::Unknown
    }
}

pub(crate) fn case_from_int(n: i32) -> Case {
    match n {
        0 => Case::Nominative,
        1 => Case::Genitive,
        2 => Case::Dative,
        3 => Case::Accusative,
        4 => Case::Vocative,
        _ => Case::Unknown
    }
}

pub(crate) fn gender_from_int(n: i32) -> Gender {
    match n {
        0 => Gender::Masculine,
        1 => Gender::Feminine,
        2 => Gender::MasculineOrFeminine,
        3 => Gender::Neuter,

        _ => Gender::Unknown,
    }
}

#[derive(Debug, FromQueryResult, PartialEq)]
pub(crate) struct ConjugationLite {
    // Only contains prefix and suffix to alloy finding distinct prefixes and suffixes
    pub(crate) prefix: String,
    pub(crate) suffix: String
}