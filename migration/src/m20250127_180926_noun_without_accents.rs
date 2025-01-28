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
                    string(NounConjugationTable::PrefixWithoutAccents).default("")
                ).take()
        ).await?;
        
        manager.alter_table(
            Table::alter()
                .table(NounConjugationTable::Table)
                .add_column(
                    string(NounConjugationTable::SuffixWithoutAccents).default("")
                ).take()
        ).await?;

        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .add_column(
                    string(NounRootsTable::RootWithoutAccents).default("")
                ).take()
        ).await?;

        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .add_column(
                    boolean(NounRootsTable::Exact).default(false)
                ).take()
        ).await?;
        
        Ok(())

    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.alter_table(
            Table::alter()
                .table(NounConjugationTable::Table)
                .drop_column(
                    NounConjugationTable::PrefixWithoutAccents
                ).take()
        ).await?;

        manager.alter_table(
            Table::alter()
                .table(NounConjugationTable::Table)
                .drop_column(
                    NounConjugationTable::SuffixWithoutAccents
                ).take()
        ).await?;

        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .drop_column(
                    NounRootsTable::RootWithoutAccents
                ).take()
        ).await?;

        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .drop_column(
                    NounRootsTable::Exact
                ).take()
        ).await?;
        
        Ok(())
    }
}

#[derive(DeriveIden)]
enum NounConjugationTable {
    Table,

    PrefixWithoutAccents,
    SuffixWithoutAccents,
}

#[derive(DeriveIden)]
enum NounRootsTable {
    Table,

    RootWithoutAccents,
    Exact
}