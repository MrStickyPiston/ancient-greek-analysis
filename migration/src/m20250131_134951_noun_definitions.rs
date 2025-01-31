use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .add_column(
                    string(NounRootsTable::Metadata).default("{}")
                ).take()
        ).await?;

        Ok(())

    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.alter_table(
            Table::alter()
                .table(NounRootsTable::Table)
                .drop_column(
                    NounRootsTable::Metadata
                ).take()
        ).await?;

        Ok(())
    }
}

#[derive(DeriveIden)]
enum NounRootsTable {
    Table,

    Metadata
}