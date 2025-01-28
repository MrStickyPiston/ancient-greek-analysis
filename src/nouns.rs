use crate::entities::{prelude::*, *};
use crate::types::{amount_from_int, case_from_int, gender_from_int, NounMorphology};
use sea_orm::*;


pub(crate) async fn get_morphology(word: &'static str, db: DatabaseConnection) -> Result<Vec<NounMorphology>, DbErr> {
    let unique_conjugations = NounConjugationTable::find()
        .all(&db).await?;
    
    let mut possible_morphology = vec![];
    
    for conjugation in unique_conjugations {
        
        let prefix = conjugation.prefix;
        let suffix = conjugation.suffix;
        
        if !( word.starts_with(&prefix) && word.ends_with(&suffix) ) {
            // Word does not match the suffix/prefix
            continue;
        }
        
        let amount = amount_from_int(conjugation.morphological_amount);
        let case = case_from_int(conjugation.morphological_case);
        let gender = gender_from_int(conjugation.morphological_gender);
        
        let root = NounRootsTable::find()
            .filter(
                Condition::all()
                    .add( noun_roots_table::Column::ConjugationGroup.eq(conjugation.conjugation_group))
                    .add( noun_roots_table::Column::Root.eq(word.trim_start_matches(&prefix).trim_end_matches(&suffix)) )
            ).one(&db).await?;
        
        if root.is_none() {
            // no matching roots found, applying the wrong conjugation group
            continue;
        }
        
        possible_morphology.push(
            NounMorphology {
                prefix: prefix.to_string(),
                suffix: suffix.to_string(),
                root: root.unwrap().root,
                amount,
                case,
                gender,
            }
        );
    }
    
    Ok(possible_morphology)
}