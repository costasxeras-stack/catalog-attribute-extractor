# Case study: Catalog Attribute Extractor

## The question

Can AI fill missing shop filter values from product text well enough to use? And which values can go live without a person checking them?

## Starting point

WANDS is a public furniture catalogue of 42,994 products. After cleaning the values into short lists, these shares of products have a usable value:

| Attribute | Products with a value |
|---|---|
| Style | 42% |
| Color | 28% |
| Material | 23% |
| Shape | 18% |

Every product without a value is invisible to a shopper who filters by that attribute.

## Approach

1. **Hide values we already have.** I sampled 300 products that have a description and at least one of the four values. Their values were hidden and used only for scoring. 20 other products were used to check the prompt and the workflow.
2. **Ask Claude in n8n.** The workflow sends ten products per call. Claude picks one value per attribute from a fixed list, or "not stated", and copies a short quote from the text as evidence.
3. **Check every answer in code.** A value is only proposed if it is on the list and its quote is found in the product text.
4. **Compare with a keyword matcher.** It looks for the same values and common synonyms in the same text. No AI.
5. **Score both on the same products.** "Right when filled" is how often a filled value matches the hidden one. "Gaps filled" is how many hidden values the method filled at all.

## What happened during the run

These are confirmed facts from the n8n executions on 20 November 2026.

- **First version:** n8n's structured-output step rejected 7 of 10 batches with "Model output doesn't fit required format". Each rejection lost all 10 products, and the automatic retries spent credits. Claude's answers that did get through were good. I switched to a plain call where Claude writes one line per product, and the check step reads each line on its own. One bad line now loses one product, not ten (decision 0002).
- **Empty and cut-off answers:** some batches still came back empty or stopped mid-line, also when calls ran one at a time. In each of the four runs, the total output stopped at 2,955 to 3,000 tokens. My hypothesis is a limit on n8n's built-in AI credits, not the workflow. I stopped there rather than spend more credits.
- **Result:** 259 of the 300 products have a complete answer. The other 41 are listed in `data/results/scorecard.json` and are not scored for either method.

## Findings

Scored on 259 products and 379 hidden values.

### 1. Claude is right more often, but fills about the same share of gaps (confirmed)

| Attribute | Hidden values | Claude: right when filled | Keywords: right when filled | Claude: gaps filled | Keywords: gaps filled |
|---|---|---|---|---|---|
| Style | 154 | 74% | 68% | 52% | 55% |
| Color | 86 | 57% | 38% | 24% | 34% |
| Shape | 60 | 100% | 100% | 27% | 27% |
| Material | 79 | 92% | 84% | 63% | 63% |
| All four | 379 | 80% | 71% | 44% | 47% |

The prompt tells Claude that a blank is better than a guess. That probably explains part of its lower coverage, for example on color.

### 2. Agreement is the best signal for auto-fill (confirmed)

| Case | Values | Claude right |
|---|---|---|
| Claude and keywords give the same value | 131 | 88% |
| They give different values | 23 | 39% |
| Only Claude gives a value | 13 | 69% |

Auto-filling only agreed values fills 35% of the hidden values, with 16 wrong ones. Auto-filling every Claude answer fills 44%, with 34 wrong ones. The rule halves the wrong values for a small loss in coverage, and the 36 other values go to a person.

### 3. Shape and material can be trusted, color cannot (confirmed)

Shape was right 16 of 16 times and material 46 of 50. Color was right 12 of 21 times. Color text often describes several parts ("brown finish and distressed white coloring") or a variant that is not the one in the catalogue.

### 4. Many style "errors" may be label problems (hypothesis)

In 16 of Claude's 21 wrong style values, the quoted text names Claude's style directly. Examples: "a traditional chandelier design" for a product labelled farmhouse, "defined by a crisp, coastal style" for one labelled modern. Either the catalogue value or the description is wrong. The dataset cannot tell which, so I have not changed any labels. A person reviewing these would settle it.

### 5. The evidence check did not catch anything this time (confirmed)

All 376 values Claude proposed came with a quote that was really in the text. One value outside the allowed list was rejected. The check costs nothing and protects against invented quotes, but in this run it was not needed.

## What I learned as a PM

- Measure an AI feature against the cheapest non-AI method first. Here the keyword matcher was 9 points behind on accuracy and slightly ahead on coverage.
- Two cheap methods that agree can be worth more than one strong method. The agreement rule is simple to explain to a catalogue team.
- Decide per attribute, not per feature. Shape and material could be auto-filled today. Color needs a person.
- Labels are not ground truth. Some disagreements are signs of bad catalogue data, which is useful to find too.
- Plan for credits and rate limits from the first run. They shaped the sample size and the workflow design.

## Limits

- One catalogue, English text only, four attributes, one model at temperature 0.
- 259 products. Shape had 16 filled values and color 21, so those rates are rough.
- The catalogue values were cleaned into short lists by my own rules (`scripts/prepare-samples.py`).
- Long descriptions were cut to 1,200 characters for both methods.

## What I would do next

1. Rerun the 41 missing products with a paid Anthropic key, and confirm whether the cut-offs were a credit limit.
2. Add a review screen in n8n for the values that need a person, and measure how long a review takes.
3. Run the agreement rule on products with no values at all, and have a person check a sample.
4. Try product images for color.

## My role

I framed the problem, chose the attributes, the baseline, the sample and the auto-fill rule, and wrote the findings. Claude (Anthropic) built the workflow and the scripts with me and ran the tests.
