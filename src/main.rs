mod entities;
mod enums;

use std::env::{var};
use futures::executor::block_on;
use sea_orm::*;
use entities::{prelude::*, *};
use crate::enums::{amount_from_int, case_from_int, gender_from_int};

async fn run() -> Result<(), DbErr> {
    let db;
    
    match var("DATABASE_URL") {
        Ok(url) => {
            db = Database::connect(&url).await?;
        }
        Err(e) => {
            // cant connect without url, throw error
            panic!("Env var DATABASE_URL not found: {}", e);
        }
    };

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

    let word = "στόλους";

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
            Condition::any()
                
                // The same prefix/suffix
                .add( noun_conjugation_table::Column::Prefix.eq(prefix) )
                .add( noun_conjugation_table::Column::Suffix.eq(suffix) )
                
                // With the same morphological data
                .add( noun_conjugation_table::Column::MorphologicalAmount.eq(conjugation["morphological_amount"].as_i64()) )
                .add( noun_conjugation_table::Column::MorphologicalCase.eq(conjugation["morphological_case"].as_i64()) )
                .add( noun_conjugation_table::Column::MorphologicalGender.eq(conjugation["morphological_gender"].as_i64()) )
        ).one(&db).await?.unwrap();
        
        if !NounRootsTable::find()
            .filter(
                Condition::any()
                    .add( noun_roots_table::Column::ConjugationGroup.eq(conjugation_col.conjugation_group))
                    .add( noun_roots_table::Column::Root.eq(word.trim_start_matches(prefix).trim_end_matches(suffix)) )
            ).one(&db).await?.is_some() {
            
            // Stem does not match word
            continue;
        }
        
        println!("Prefix: {}\nSuffix: {}\nRoot: {}\nAmount: {:?}\nCase: {:?}\nGender: {:?}", 
                 prefix, 
                 suffix,
                 word.trim_start_matches(prefix).trim_end_matches(suffix), 
                 amount, 
                 case,
                 gender
        );
    }

    Ok(())
}

fn main() {
    if let Err(err) = block_on(run()) {
        panic!("{}", err);
    }
}