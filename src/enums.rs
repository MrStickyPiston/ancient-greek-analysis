#[derive(Debug)]
pub(crate) enum Amount {
    Singular,
    Dual,
    Plural,
    
    Unknown
}

#[derive(Debug)]
pub(crate) enum Case {
    Nominative,
    Genitive,
    Dative,
    Accusative,
    Vocative,
    
    Unknown
}

#[derive(Debug)]
pub(crate) enum Gender {
    Masculine,
    Feminine,
    MasculineOrFeminine,
    Neuter,
    
    Unknown
}

pub(crate) fn amount_from_int(n: i64) -> Amount {
    match n {
        0 => Amount::Singular,
        1 => Amount::Dual,
        2 => Amount::Plural,
        _ => Amount::Unknown
    }
}

pub(crate) fn case_from_int(n: i64) -> Case {
    match n {
        0 => Case::Nominative,
        1 => Case::Genitive,
        2 => Case::Dative,
        3 => Case::Accusative,
        4 => Case::Vocative,
        _ => Case::Unknown
    }
}

pub(crate) fn gender_from_int(n: i64) -> Gender {
    match n {
        0 => Gender::Masculine,
        1 => Gender::Feminine,
        2 => Gender::MasculineOrFeminine,
        3 => Gender::Neuter,
        _ => Gender::Unknown,
    }
}