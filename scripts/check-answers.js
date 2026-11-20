// Same rules as the "Check answers" node in workflows/01-extract.json, run locally on Claude's raw lines.
// Usage: node scripts/check-answers.js data/input/test.json data/results/raw/*.txt > data/results/claude-test.json
// Later files win when a product appears twice (used for reruns of failed batches).
const fs = require('fs');

const ALLOWED = {
  style: ['modern', 'traditional', 'glam', 'farmhouse', 'industrial', 'coastal', 'boho', 'lodge'],
  color: ['white', 'black', 'gray', 'brown', 'blue', 'beige', 'green', 'red', 'pink', 'yellow', 'orange', 'purple', 'silver', 'gold', 'clear', 'multicolor'],
  shape: ['rectangular', 'square', 'round', 'oval', 'l-shaped', 'u-shaped', 'hexagonal', 'octagonal'],
  material: ['metal', 'wood', 'plastic', 'glass', 'ceramic', 'fabric', 'natural fiber', 'stone'],
};
const ATTRS = Object.keys(ALLOWED);
const flat = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '');

const [inputPath, ...rawPaths] = process.argv.slice(2);
const products = JSON.parse(fs.readFileSync(inputPath, 'utf8'));

const answers = {};
rawPaths.forEach((p) => {
  fs.readFileSync(p, 'utf8').split('\n').forEach((line) => {
    const f = line.split('|').map((s) => s.trim());
    if (f.length < 9 || !/^\d+$/.test(f[0])) return;
    const a = {};
    ATTRS.forEach((attr, k) => { a[attr] = { value: f[1 + 2 * k], evidence: f[2 + 2 * k] }; });
    answers[Number(f[0])] = a;
  });
});

const out = {};
products.forEach((p) => {
  const hay = flat(p.name + ' ' + p.product_class + ' ' + String(p.description || '').slice(0, 1200));
  const row = {};
  ATTRS.forEach((attr) => {
    const a = answers[p.product_id] && answers[p.product_id][attr];
    const value = a ? String(a.value || '').toLowerCase().trim() : '';
    const evidence = a ? String(a.evidence || '').trim().slice(0, 200) : '';
    let status;
    if (!answers[p.product_id]) status = 'missing_in_answer';
    else if (!value || value === 'not_stated') status = 'not_stated';
    else if (!ALLOWED[attr].includes(value)) status = 'rejected_invalid_value';
    else if (flat(evidence).length < 3 || !hay.includes(flat(evidence))) status = 'rejected_no_evidence';
    else status = 'proposed';
    row[attr] = { status, value: status === 'proposed' || status.startsWith('rejected') ? value : '', evidence };
  });
  out[p.product_id] = row;
});
process.stdout.write(JSON.stringify(out, null, 0));
