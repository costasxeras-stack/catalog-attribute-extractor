# 0003: Auto-fill only when Claude and the keyword matcher agree

**Status:** proposed for the next version, based on the 0.1.0 results

## Context

Claude's filled values were right 80% of the time. For a shop filter, 1 wrong value in 5 is too many to publish without a check. Checking every value by hand removes most of the benefit.

## Decision

Publish a value automatically only when Claude and the keyword matcher give the same value. Send values where they disagree, or where only Claude answers, to a person.

## Trade-off

On the 259 scored products:

| Rule | Values filled automatically | Right | Wrong values live | Values for a person |
|---|---|---|---|---|
| Every Claude answer | 167 | 80% | 34 | 0 |
| Only when both agree | 131 | 88% | 16 | 36 |

The rule fills 36 fewer values automatically and needs 36 reviews, but it halves the wrong values. The keyword matcher costs nothing to run, so the extra signal is free.

## Open question

Shape and material were already right 92% to 100% of the time. A per-attribute rule (auto-fill shape and material from Claude alone, require agreement for style and color) may be better. The samples for shape and color are too small to decide that yet.
