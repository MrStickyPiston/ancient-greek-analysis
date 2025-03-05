use crate::types::NounMorphology;

pub fn render_noun_morphology(m: &NounMorphology) -> String {
    let mut s = format!(
        "Noun: {}{}{}\nConjugation: {:?} {:?} {:?}",
        m.prefix, m.root, m.suffix, m.amount, m.case, m.gender
    );
    
    s.push_str("\nDefinitions: ");

    for i in 0..m.definitions.len() {
        s.push_str(format!("\n {}. {}", i+1, m.definitions[i]).as_str())
    }
    
    s
}
