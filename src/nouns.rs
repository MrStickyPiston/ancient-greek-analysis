use crate::entities::{prelude::*, *};
use crate::types::{amount_from_int, case_from_int, gender_from_int, NounMorphology};
use sea_orm::*;
use crate::utils::without_accents;

pub(crate) async fn get_morphology(word: &'static str, db: DatabaseConnection) -> Result<Vec<NounMorphology>, DbErr> {

    let word_without_accents = without_accents(word);

    let conjugations = NounConjugationTable::find()
        .all(&db).await?;
    
    let mut possible_morphology = vec![];
    
    for conjugation in conjugations {
        
        if !( word_without_accents.starts_with(&conjugation.prefix_without_accents) && word_without_accents.ends_with(&conjugation.suffix_without_accents) ) {
            // Word does not match the suffix/prefix
            continue;
        }
        
        let amount = amount_from_int(conjugation.morphological_amount);
        let case = case_from_int(conjugation.morphological_case);
        
        let roots = NounRootsTable::find()
            .filter(
                Condition::all()
                    .add( noun_roots_table::Column::ConjugationGroup.eq(conjugation.conjugation_group))
                    .add( noun_roots_table::Column::RootWithoutAccents.eq(word_without_accents.trim_start_matches(&conjugation.prefix_without_accents).trim_end_matches(&conjugation.suffix_without_accents)) )
            ).all(&db).await?;

        for root in roots {
            
            if root.exact {
                possible_morphology.push(
                    NounMorphology {
                        prefix: conjugation.prefix.clone(),
                        suffix: conjugation.suffix.clone(),
                        root: root.root,

                        amount: amount.clone(),
                        case: case.clone(),
                        gender: gender_from_int(root.gender),

                        exact: true,
                    }
                );

            } else {
                possible_morphology.push(
                    NounMorphology {
                        prefix: conjugation.prefix_without_accents.clone(),
                        suffix: conjugation.suffix_without_accents.clone(),
                        root: root.root_without_accents,

                        amount: amount.clone(),
                        case: case.clone(),
                        gender: gender_from_int(root.gender),

                        exact: false,
                    }
                );
            }
        }

    }
    
    Ok(possible_morphology)
}