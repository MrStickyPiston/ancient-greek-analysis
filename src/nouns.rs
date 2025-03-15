use crate::entities::{prelude::*, *};
use crate::types::{amount_from_int, case_from_int, gender_from_int, Amount, Case, ConjugationLite, NounMorphology};
use crate::utils::without_accents;
use sea_orm::*;
use serde_json::json;
use serde_json::Value::Null;
use unicode_normalization::UnicodeNormalization;

pub(crate) async fn get_morphology(word: &'static str, db: DatabaseConnection) -> Result<Vec<NounMorphology>, DbErr> {

    let word_without_accents = without_accents(word);

    // Query all unique conjugation endings
    let conjugations: Vec<ConjugationLite> = NounConjugationTable::find()
        .select_only()
        .columns([noun_conjugation_table::Column::Prefix, noun_conjugation_table::Column::Suffix])
        .distinct()
        .into_model()
        .all(&db).await?;

    let mut possible_morphology = vec![];

    // Loop through all unique conjugation endings, note that this is not
    for conjugation in conjugations {

        let prefix = conjugation.prefix;
        let suffix = conjugation.suffix;


        if !( word_without_accents.starts_with(&prefix) && word_without_accents.ends_with(&suffix) ) {
            // Word does not match the suffix/prefix
            continue;
        }

        let roots = NounRootsTable::find()
            .filter(
                Condition::all()
                    // .nfc().collect::<String>() fixes no match being found due to unicode combining
                    // This requires the data in the database to be NFC
                    .add( noun_roots_table::Column::Root.eq(word_without_accents.trim_start_matches(&prefix).trim_end_matches(&suffix).nfc().collect::<String>()) )
            ).all(&db).await?;

        for root in roots {

            let full_conjugations = NounConjugationTable::find()
                .filter(
                    Condition::all()
                        .add( noun_conjugation_table::Column::Prefix.eq(&prefix) )
                        .add( noun_conjugation_table::Column::Suffix.eq(&suffix) )
                        .add( noun_conjugation_table::Column::ConjugationGroup.eq(root.conjugation_group) )
                ).all(&db).await?;

            let metadata: serde_json::Value = serde_json::from_str(&root.metadata).unwrap_or(json!(Null));

            for full_conjugation in full_conjugations {
                possible_morphology.push(
                    NounMorphology {
                        prefix: prefix.clone(),
                        suffix: suffix.clone(),
                        root: root.root.clone(),

                        amount: amount_from_int(full_conjugation.morphological_amount),
                        case: case_from_int(full_conjugation.morphological_case),
                        gender: gender_from_int(root.gender),

                        definitions: metadata["definitions"].as_array().unwrap_or(&Vec::new()).iter().map(|x| x.as_str().unwrap().to_string()).collect(),
                        wiktionary_id: metadata["wiktionary_id"].as_str().unwrap_or("").to_string(),
                    }
            );
            }
        }

    }

    Ok(possible_morphology)
}