# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **Logseq knowledge base** (personal knowledge management vault), not a software project. Logseq is a privacy-first outliner note-taking app. There are no build steps, package managers, or tests.

To use this vault, open the `C:\Dev\graphdev` directory in the Logseq desktop application.

## Repository Structure

- `pages/` — Named note pages (Markdown files)
- `journals/` — Daily journal entries (auto-named by date, e.g., `2026_04_08.md`)
- `logseq/config.edn` — All Logseq configuration (EDN format, Clojure-like syntax)
- `logseq/custom.css` — Custom CSS overrides (currently empty)

## Configuration Conventions (`logseq/config.edn`)

The config uses EDN syntax. Key active settings:

- **Workflow**: `:now` style — tasks use `NOW`, `LATER`, `DOING` markers (not `TODO`/`DOING`)
- **File naming**: `:triple-lowbar` — slashes in page titles are escaped as `___` in filenames
- **Week start**: Sunday (`:start-of-week 6`)
- **Linked references collapse threshold**: 50 items
- **Block max length**: 10,000 characters (blocks beyond this are not searchable)

### Default Journal Queries

Two automatic queries appear at the bottom of each journal page:
- **🔨 NOW** — blocks with `NOW` or `DOING` status from the last 14 days
- **📅 NEXT** — blocks with `NOW`, `LATER`, or `TODO` status in the next 7 days

### Custom Query Helpers

Defined in `:query/views` and `:query/result-transforms`:
- `:pprint` view — renders query results as a formatted code block
- `:sort-by-priority` transform — sorts results by `:block/priority` ascending (missing priority sorts as "Z")

## Editing Notes

- Pages are plain Markdown files; page links use `[[Page Name]]` syntax
- Block references use `((block-uuid))` syntax
- Properties are defined as `key:: value` at the top of a block or page
- Tags use `#tag` or `[[tag]]` interchangeably
- Logseq manages file creation and naming — avoid manually renaming files after they are created, as internal links use the page title, not the filename
