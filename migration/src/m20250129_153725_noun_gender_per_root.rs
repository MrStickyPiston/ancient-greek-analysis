use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.alter_table(
            Table::alter()
                .table(NounConjugationTable::Table)
                .drop_column(
                    // Default to 4 (Unkown) because of existing entries would bug because of not null
                    NounConjugationTable::MorphologicalGender
                ).take()
        ).await?;

        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .add_column(
                    // Default to 4 (Unkown) because of existing entries would bug because of not null
                    integer(NounRootsTable::Gender).default(4)
                ).take()
        ).await?;
        
        Ok(())

    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .drop_column(
                    // Default to 4 (Unkown) because of existing entries would bug because of not null
                    NounRootsTable::Gender
                ).take()
        ).await?;
        
        manager.alter_table(
            Table::alter()
                .table(NounConjugationTable::Table)
                .add_column(
                    // Default to 4 (Unkown) because of existing entries would bug because of not null
                    integer(NounConjugationTable::MorphologicalGender).default(4)
                ).take()
        ).await?;

        Ok(())
    }
}

#[derive(DeriveIden)]
enum NounConjugationTable {
    Table,

    MorphologicalGender
}

#[derive(DeriveIden)]
enum NounRootsTable {
    Table,

    Gender
}