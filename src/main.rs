mod entities;
mod types;
mod nouns;
mod utils;
mod ui;

use crate::nouns::get_morphology;
use futures::executor::block_on;
use sea_orm::*;
use std::env::var;
use crate::ui::terminal::render_noun_morphology;

async fn run() -> Result<(), DbErr> {
    let db;

    // Connect to the database from the environment variable DATABASE_URL
    match var("DATABASE_URL") {
        Ok(url) => {
            db = Database::connect(&url).await?;
        }
        Err(e) => {
            // cant connect without url, throw error
            panic!("Env var DATABASE_URL not found: {}", e);
        }
    };

    // TODO: provide a real input method
    // Currently this is used for testing purposes so no new word has to be entered over and over again
    let word = "ᾰ̓́νδρᾰς";
    get_morphology(word, db).await?.iter().for_each(|m| println!("{}\n", render_noun_morphology(m)));
    
    Ok(())
}

fn main() {
    if let Err(err) = block_on(run()) {
        panic!("{}", err);
    }
}