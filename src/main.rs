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
    
    match var("DATABASE_URL") {
        Ok(url) => {
            db = Database::connect(&url).await?;
        }
        Err(e) => {
            // cant connect without url, throw error
            panic!("Env var DATABASE_URL not found: {}", e);
        }
    };

    let word = "ψᾰ́μμοιν";
    get_morphology(word, db).await?.iter().for_each(|m| println!("{}\n", render_noun_morphology(m)));
    
    Ok(())
}

fn main() {
    if let Err(err) = block_on(run()) {
        panic!("{}", err);
    }
}