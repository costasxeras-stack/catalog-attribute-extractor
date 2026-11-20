# 0002: One plain line per product instead of n8n's structured output

**Status:** accepted, 0.1.0

## Context

The first version used n8n's Information Extractor with a JSON schema. It rejected 7 of 10 batches with "Model output doesn't fit required format". Each rejection lost all ten products in the batch, and the automatic retries spent AI credits. Removing the list of allowed values from the schema did not fix it.

## Decision

Use a plain Claude call (Basic LLM Chain) and ask for one line per product with nine fields separated by a pipe character. The "Check answers" step reads each line on its own. A line with the wrong number of fields loses that product only. Allowed values are checked in code, not in the schema.

## Trade-off

- A schema gives typed output and catches format errors before the code sees them.
- Plain lines are shorter than JSON, and one bad line loses one product instead of ten.

The same check runs locally (`scripts/check-answers.js`) on the raw lines saved in `data/results/raw/`, so the scoring can be repeated without calling Claude again.
