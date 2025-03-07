pub use sea_orm_migration::prelude::*;

mod m20220101_000001_create_roots_table;
mod m20250111_124939_noun_gender;
mod m20250127_180926_noun_without_accents;
mod m20250129_153725_noun_gender_per_root;
mod m20250131_134951_noun_definitions;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m20220101_000001_create_roots_table::Migration),
            Box::new(m20250111_124939_noun_gender::Migration),
            Box::new(m20250127_180926_noun_without_accents::Migration),
            Box::new(m20250129_153725_noun_gender_per_root::Migration),
            Box::new(m20250131_134951_noun_definitions::Migration),
        ]
    }
}
