mod entities;
mod types;
mod nouns;

use crate::nouns::get_morphology;
use futures::executor::block_on;
use sea_orm::*;
use std::env::var;

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

    let word = "θεαῖν";
    get_morphology(word, db).await?.iter().for_each(|m| println!("{:#?}", m));

    Ok(())
}

fn main() {
    if let Err(err) = block_on(run()) {
        panic!("{}", err);
    }
}