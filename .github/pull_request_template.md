## Description

Use this section to describe what changes are being made and/or call
out anything specific that you would like to have reviewed.

Before adding reviewers please check:

* [ ] rebase with master for a clean merge
* [ ] all tests are passing `make test`
* [ ] migrations have been reduced to one file (see migration discussion below)
* [ ] remove any debugging statement (e.g. `print`)
* [ ] code has been formatted with black `make black`
* [ ] code is passing all linting rules `make lint`

## Note on Migrations
When working on a branch, often you will end up with multiple migration files as you are experimenting with the model implementation. It is much nicer commit a single migration file, to do this:

1. Migrate the app backward to the index before your first migration. eg. if you have made migratinos 004-006, rollback to 003
2. Delete your new migration files
3. Regenerate the migration, which will produce one file
