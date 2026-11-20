# 0001: Every value needs a quote, and code checks the quote

**Status:** accepted, 0.1.0

## Context

A filled value changes which filter a product appears under. A reviewer needs to see why the AI chose it, and an AI can invent a reason that sounds right.

## Decision

Claude must return a 2 to 10 word quote from the product text for every value. The "Check answers" step in n8n compares the quote with the text, ignoring spacing and punctuation. A value is only proposed if the quote is found and the value is on the allowed list. Otherwise it is saved with a rejection status.

## Trade-off

- The quote makes each answer longer, so each call costs more output tokens.
- In return, every proposed value can be checked by a person in seconds, and invented quotes are caught by code.

In this run the check found no invented quotes in 376 proposed values. I keep it anyway: it costs no AI calls, and one run with one model is not proof that it will never be needed.
