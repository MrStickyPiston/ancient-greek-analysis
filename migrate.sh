sea-orm-cli migrate up
rm -rf src/entities
sea-orm-cli generate entity -u sqlite://db.sqlite?mode=rwc -o src/entities