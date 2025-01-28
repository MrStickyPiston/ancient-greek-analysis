use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Create the roots table

        manager
            .create_table(
                Table::create()
                    .table(NounRootsTable::Table)
                    .if_not_exists()
                    
                    .col(pk_auto(NounRootsTable::Id))
                    
                    .col(string(NounRootsTable::Root))
                    .col(boolean(NounRootsTable::IsRegular).default(true))
                    .col(string(NounRootsTable::ConjugationGroup))
                    .to_owned(),
            )
            .await?;

        manager.create_table(
            Table::create()
                .table(NounConjugationTable::Table)
                .if_not_exists()
                
                .col(pk_auto(NounConjugationTable::Id))
                
                // Shared amongst all entries for this group
                .col(string(NounConjugationTable::ConjugationGroup))
                
                .col(string(NounConjugationTable::Prefix))
                .col(string(NounConjugationTable::Suffix))
                
                .col(ColumnDef::new(NounConjugationTable::MorphologicalAmount).integer().not_null())
                .col(ColumnDef::new(NounConjugationTable::MorphologicalCase).integer().not_null())
                
                .to_owned(),
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Drop the roots table

        manager
            .drop_table(Table::drop().table(NounRootsTable::Table).to_owned())
            .await?;

        manager
            .drop_table(Table::drop().table(NounConjugationTable::Table).to_owned())
            .await?;

        Ok(())
    }
}

#[derive(DeriveIden)]
enum NounRootsTable {
    Table,
    Id,

    Root,
    IsRegular,
    ConjugationGroup
}

#[derive(DeriveIden)]
enum NounConjugationTable {
    Table,
    Id,

    ConjugationGroup,
    Prefix,
    Suffix,

    MorphologicalAmount,
    MorphologicalCase
}