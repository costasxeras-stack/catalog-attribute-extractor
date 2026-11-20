"""Keyword baseline with no AI: looks for value words (and common synonyms) in the same text Claude sees.
Name matches win over description matches; within a field, the earliest match wins.
Usage: python3 scripts/baseline.py data/input/test.json > data/results/baseline-test.json"""
import json, re, sys

WORDS = {
    "style": {
        "modern": ["modern", "contemporary", "mid-century", "mid century", "minimalist", "sleek"],
        "traditional": ["traditional", "classic", "timeless", "vintage-inspired"],
        "glam": ["glam", "glamorous", "glamour"],
        "farmhouse": ["farmhouse", "country", "shiplap"],
        "industrial": ["industrial"],
        "coastal": ["coastal", "nautical", "beach", "seaside"],
        "boho": ["boho", "bohemian"],
        "lodge": ["lodge", "cabin", "rustic"],
    },
    "color": {
        "white": ["white", "ivory white", "off-white"],
        "black": ["black", "ebony"],
        "gray": ["gray", "grey", "charcoal", "slate"],
        "brown": ["brown", "espresso", "walnut", "cherry", "chocolate", "mahogany"],
        "blue": ["blue", "navy", "turquoise", "teal", "aqua"],
        "beige": ["beige", "ivory", "cream", "tan", "taupe", "khaki"],
        "green": ["green", "sage", "olive", "mint", "emerald"],
        "red": ["red", "burgundy", "maroon"],
        "pink": ["pink", "blush"],
        "yellow": ["yellow", "mustard"],
        "orange": ["orange", "rust"],
        "purple": ["purple", "lavender", "plum"],
        "silver": ["silver", "chrome", "nickel"],
        "gold": ["gold", "golden"],
        "clear": ["clear", "transparent"],
        "multicolor": ["multicolor", "multi-color", "multicolored", "colorful"],
    },
    "shape": {
        "rectangular": ["rectangular", "rectangle"],
        "square": ["square"],
        "round": ["round", "circular", "circle"],
        "oval": ["oval"],
        "l-shaped": ["l-shaped", "l shaped", "l-shape"],
        "u-shaped": ["u-shaped", "u shaped"],
        "hexagonal": ["hexagonal", "hexagon"],
        "octagonal": ["octagonal", "octagon"],
    },
    "material": {
        "metal": ["metal", "steel", "iron", "aluminum", "brass", "zinc"],
        "wood": ["wood", "wooden", "mdf", "bamboo", "oak", "pine", "walnut", "acacia"],
        "plastic": ["plastic", "resin", "acrylic", "polypropylene", "vinyl", "pvc", "melamine"],
        "glass": ["glass", "crystal"],
        "ceramic": ["ceramic", "porcelain", "stoneware", "earthenware"],
        "fabric": ["fabric", "polyester", "cotton", "linen", "velvet", "microfiber", "wool"],
        "natural fiber": ["jute", "rattan", "wicker", "coir", "seagrass"],
        "stone": ["stone", "marble", "granite", "concrete"],
    },
}


def first_match(text, attr):
    best = None
    for value, words in WORDS[attr].items():
        for w in words:
            m = re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", text)
            if m and (best is None or m.start() < best[0]):
                best = (m.start(), value, w)
    return best


def extract(p):
    name = (p["name"] or "").lower()
    desc = (p["description"] or "")[:1200].lower()  # same cut as the n8n workflow
    out = {}
    for attr in WORDS:
        hit = first_match(name, attr) or first_match(desc, attr)
        if hit:
            out[attr] = {"value": hit[1], "evidence": hit[2]}
    return out


if __name__ == "__main__":
    products = json.load(open(sys.argv[1]))
    json.dump({str(p["product_id"]): extract(p) for p in products}, sys.stdout, indent=0)
