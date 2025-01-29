use crate::types::NounMorphology;

pub fn render_noun_morphology(m: &NounMorphology) -> String {
    format!(
        "Noun: {}{}{}\nExact: {}\nConjugation: {:?} {:?} {:?}",
        m.prefix, m.root, m.suffix, m.exact, m.amount, m.case, m.gender
    )
}
