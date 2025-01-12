use crate::entities::{prelude::*, *};
use crate::types::{amount_from_int, case_from_int, gender_from_int, NounMorphology};
use sea_orm::*;


pub(crate) async fn get_morphology(word: &'static str, db: DatabaseConnection) -> Result<Vec<NounMorphology>, DbErr> {
    let unique_conjugations = NounConjugationTable::find()
        .select_only()
        .columns([
            noun_conjugation_table::Column::Prefix,
            noun_conjugation_table::Column::Suffix,

            noun_conjugation_table::Column::MorphologicalAmount,
            noun_conjugation_table::Column::MorphologicalCase,
            noun_conjugation_table::Column::MorphologicalGender
        ])
        .distinct()
        .into_json()
        .all(&db).await?;
    
    let mut possible_morphology = vec![];
    
    for conjugation in unique_conjugations {
        let prefix = conjugation["prefix"].as_str().unwrap_or("");
        let suffix = conjugation["suffix"].as_str().unwrap_or("");

        if !( word.starts_with(prefix) && word.ends_with(suffix) ) {
            // Word does not match the suffix/prefix
            continue;
        }

        let amount = amount_from_int(conjugation["morphological_amount"].as_i64().unwrap());
        let case = case_from_int(conjugation["morphological_case"].as_i64().unwrap());
        let gender = gender_from_int(conjugation["morphological_gender"].as_i64().unwrap());

        let conjugation_col = NounConjugationTable::find().filter(
            Condition::all()

                // The same prefix/suffix
                .add( noun_conjugation_table::Column::Prefix.eq(prefix) )
                .add( noun_conjugation_table::Column::Suffix.eq(suffix) )

                // With the same morphological data
                .add( noun_conjugation_table::Column::MorphologicalAmount.eq(conjugation["morphological_amount"].as_i64()) )
                .add( noun_conjugation_table::Column::MorphologicalCase.eq(conjugation["morphological_case"].as_i64()) )
                .add( noun_conjugation_table::Column::MorphologicalGender.eq(conjugation["morphological_gender"].as_i64()) )
        ).one(&db).await?.unwrap();
        
        let root = NounRootsTable::find()
            .filter(
                Condition::all()
                    .add( noun_roots_table::Column::ConjugationGroup.eq(conjugation_col.conjugation_group))
                    .add( noun_roots_table::Column::Root.eq(word.trim_start_matches(prefix).trim_end_matches(suffix)) )
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