# 0005: Open with a product data sheet

**Status:** Accepted · 23 November 2026

## Context

Version 0.1.0 opened with three number tiles and kept the individual answers in a long list at the bottom. It shared one visual template with the other portfolio apps, and the point of the project (a product with no values is invisible to a shopper's filters) was only in the text.

## Decision

Open with a product data sheet. One real product, Claude's evidence quotes, and its filter values from the catalogue, Claude and the keyword matcher, each marked as matching the catalogue or not. A before and after count shows how many filters a shopper could find the product under: none before, and as many as Claude got right after. Wrong values are not counted as found.

"Show another product" moves through the 68 products with two or more checked values, ordered by how many values Claude filled. The first products are therefore the best cases. The note under the table says the order, and the overall results sit directly below the sheet.

The app gets its own look: dark header, price-tag orange, Manrope.

## Consequences

- A visitor sees the mechanism (evidence quote to filter value) and the reason it matters (findable under a filter) on one product before any number.
- Opening on a best case is a curation choice. It is stated on the page, and the 80%, 88% and 57% findings follow immediately.
