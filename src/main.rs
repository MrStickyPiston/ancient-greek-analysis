mod entities;
mod enums;

use std::env::{var, VarError};
use futures::executor::block_on;
use sea_orm::*;
use entities::{prelude::*, *};
use crate::enums::{Amount, Case};

async fn run() -> Result<(), DbErr> {
    let db;
    
    match var("DATABASE_URL") {
        Ok(url) => {
            db = Database::connect(&url).await?;
        }
        Err(e) => {
            // cant connect without url, throw error
            panic!("Env var DATABASE_URL not found");
        }
    };
    
    let new_conjugation = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Singular as i32),
        morphological_case: ActiveValue::Set(Case::Nominative as i32),
        suffix: ActiveValue::Set(Option::from("ος".to_owned())),
        ..Default::default()
    };
    
    new_conjugation.save(&db).await?;

    let new_root = noun_roots_table::ActiveModel {
        root: ActiveValue::Set("ἀβυσσ".to_owned()),
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        ..Default::default()
    };

    new_root.save(&db).await?;

    let matching_morphology = NounConjugationTable::find()
        .filter(
            Condition::any()
                .add(noun_conjugation_table::Column::Suffix.eq("ος"))
        ).all(&db).await?;

    for morphology in matching_morphology {
        println!("Match case {}", morphology.morphological_case);
        println!("Match amount {}", morphology.morphological_amount);
    }

    Ok(())
}

fn main() {
    if let Err(err) = block_on(run()) {
        panic!("{}", err);
    }
}