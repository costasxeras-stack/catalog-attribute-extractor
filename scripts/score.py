"""Scores Claude's checked answers and the keyword baseline against the hidden WANDS labels.
Usage: python3 scripts/score.py   (reads data/results/claude-test.json, baseline-test.json, data/labels/test-labels.json)
Writes data/results/scorecard.json for the app.

Per attribute, only products that have a label for it are scored:
- answered: the method gave a value (Claude: status 'proposed')
- correct: the value equals the label
- precision = correct / answered (how often a filled value is right)
- coverage = answered / labelled (how many gaps it would fill)
- correct share = correct / labelled
"""
import json, collections

ATTRS = ["style", "color", "shape", "material"]
claude = json.load(open("data/results/claude-test.json"))
# Score only products where Claude returned a complete answer, so both methods are scored on the same products.
# Products whose batch came back empty or cut off (n8n AI credit limits, see the case study) are listed, not scored.
all_labels = json.load(open("data/labels/test-labels.json"))
missing = sorted(int(k) for k in all_labels if any(claude[k][a]["status"] == "missing_in_answer" for a in ATTRS))
labels = {k: v for k, v in all_labels.items() if int(k) not in missing}
base = json.load(open("data/results/baseline-test.json"))
products = {str(p["product_id"]): p for p in json.load(open("data/input/test.json"))}


def score(get):
    out = {}
    for a in ATTRS:
        ids = [k for k in labels if a in labels[k]]
        ans = [k for k in ids if get(k, a)]
        cor = [k for k in ans if get(k, a) == labels[k][a]]
        conf = collections.Counter((labels[k][a], get(k, a)) for k in ans if get(k, a) != labels[k][a])
        out[a] = dict(labelled=len(ids), answered=len(ans), correct=len(cor),
                      precision=round(len(cor) / len(ans), 4) if ans else None,
                      coverage=round(len(ans) / len(ids), 4) if ids else None,
                      confusions=[[l, g, n] for (l, g), n in conf.most_common(6)])
    tot = {k: sum(out[a][k] for a in ATTRS) for k in ["labelled", "answered", "correct"]}
    tot["precision"] = round(tot["correct"] / tot["answered"], 4)
    tot["coverage"] = round(tot["answered"] / tot["labelled"], 4)
    out["all"] = tot
    return out


cl = lambda k, a: claude[k][a]["value"] if claude[k][a]["status"] == "proposed" else None
bl = lambda k, a: base.get(k, {}).get(a, {}).get("value")
status = collections.Counter(claude[k][a]["status"] for k in labels for a in ATTRS)

# Product-level rows for the app: every labelled attribute with both answers (unlabelled ones cannot be scored)
rows = []
for k, lab in labels.items():
    p = products[k]
    for a in [x for x in ATTRS if x in lab]:
        c = claude[k][a]
        rows.append(dict(id=int(k), name=p["name"], cls=p["product_class"], attr=a, label=lab.get(a),
                         claude=c["value"] or None, status=c["status"], evidence=c["evidence"] or None,
                         base=bl(k, a), base_ev=base.get(k, {}).get(a, {}).get("evidence")))

# Review gate: auto-fill only when Claude and the keyword baseline give the same value.
def gate():
    g = {}
    for a in ATTRS + ["all"]:
        attrs = ATTRS if a == "all" else [a]
        b = {"agree": [0, 0], "disagree": [0, 0], "claude_only": [0, 0]}
        for k in labels:
            for x in attrs:
                if x not in labels[k] or not cl(k, x): continue
                key = "claude_only" if not bl(k, x) else ("agree" if bl(k, x) == cl(k, x) else "disagree")
                b[key][0] += 1; b[key][1] += cl(k, x) == labels[k][x]
        g[a] = {key: dict(n=n, correct=c, precision=round(c / n, 4) if n else None) for key, (n, c) in b.items()}
        g[a]["labelled"] = sum(1 for k in labels for x in attrs if x in labels[k])
    return g

card = dict(gate=gate(), claude=score(cl), baseline=score(bl), claude_status=dict(status), products=len(labels), sample=len(all_labels), not_scored=missing, rows=rows)
json.dump(card, open("data/results/scorecard.json", "w"), ensure_ascii=False)
for m in ["claude", "baseline"]:
    print(m)
    for a in ATTRS + ["all"]:
        s = card[m][a]
        print(f"  {a:9} labelled {s['labelled']:4} answered {s['answered']:4} correct {s['correct']:4} "
              f"precision {s['precision'] * 100 if s['precision'] is not None else 0:5.1f}% coverage {s['coverage'] * 100:5.1f}%")
print("gate", json.dumps(card["gate"]["all"]), {a: card["gate"][a]["agree"] for a in ATTRS})
print("claude status", dict(status), "scored", len(labels), "of", len(all_labels), "not scored", len(missing))
