use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.alter_table(
            Table::alter()
                .table(NounConjugationTable::Table)
                .add_column(
                    // Default to 4 (Unkown) because of existing entries would bug because of not null
                    integer(NounConjugationTable::MorphologicalGender).default(4)
                ).take()
        ).await
        
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.alter_table(
            Table::alter()
                .table(NounConjugationTable::Table)
                .drop_column(
                    NounConjugationTable::MorphologicalGender
                ).take()
        ).await
    }
}

#[derive(DeriveIden)]
enum NounConjugationTable {
    Table,
    
    MorphologicalGender
}