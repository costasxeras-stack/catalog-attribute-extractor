# Changelog

All notable changes to this project. Versions follow [docs/versioning.md](docs/versioning.md).

## [0.2.0] - 2026-11-23

### Changed
- New design. The page opens on a product data sheet: a real product, Claude's evidence quotes, and a table of its filter values from the catalogue, Claude and the keyword matcher, each marked as matching or not. It also shows how many filters a shopper could find the product under before and after Claude's right values. Products with the most filled values come first, and the note under the table says so.
- Own look for this app: dark header, price-tag orange, Manrope, square corners.

### Added
- Decision record: open with a product data sheet.

Data and results are unchanged.

## [0.1.0] - 2026-11-20

First release.

### Added
- n8n workflow that reads product text with Claude and proposes style, color, shape and material, each with an evidence quote. Ten products per call, one call at a time.
- Check step: only allowed values with a quote found in the product text are proposed. Every answer is saved to an n8n data table with a status.
- Keyword baseline with no AI, run on the same text.
- Scoring against hidden catalogue values on 259 WANDS products, and a rule that auto-fills only when Claude and the baseline agree.
- Results page with a scorecard, an auto-fill rule simulator and every scored answer with its evidence.
- Case study, product brief and four decision records.
