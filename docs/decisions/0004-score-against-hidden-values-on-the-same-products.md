# 0004: Score against hidden catalogue values, on the same products for both methods

**Status:** accepted, 0.1.0

## Context

Products that are missing a value cannot be scored, because there is nothing to compare with. Products that have one can be scored if the value is hidden. Some batches came back from Claude empty or cut off, so 41 of the 300 sampled products have no complete answer.

## Decision

- Sample products that already have values, hide the values, and score against them.
- Use 20 separate products to check the prompt and workflow, and do not change the prompt after looking at the 300.
- Score both methods only on the 259 products where Claude returned a complete answer. List the 41 others.

## Trade-off

- Products with values may differ from products without them, for example in how detailed their descriptions are. The scores may be higher than on the real gaps.
- Leaving out the 41 products keeps the comparison fair, but makes the sample smaller. Counting them as blanks would have made Claude look worse for a reason that had nothing to do with its answers.

The next step (case study, "What I would do next") is to run the agreement rule on products with no values and have a person check a sample.
