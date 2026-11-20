"""Builds the samples from WANDS product.csv (download it to scripts/product.csv from github.com/wayfair/WANDS).
Writes data/input/{dev,test}.json (no labels) and data/labels/{dev,test}-labels.json.
Labels are cleaned into a short list of values per attribute, the same lists Claude is given."""
import pandas as pd, json, random, re
df=pd.read_csv('scripts/product.csv',sep='\t')
def feats(f):
    d={}
    if isinstance(f,str):
        for kv in f.split('|'):
            if ':' in kv: k,v=kv.split(':',1); d.setdefault(k.strip(),v.strip())
    return d
STYLE={'modern':'modern','traditional':'traditional','glam':'glam','country / farmhouse':'farmhouse','country':'farmhouse','country/farmhouse':'farmhouse','industrial':'industrial','coastal':'coastal','boho':'boho','lodge':'lodge'}
SHAPE={'rectangular':'rectangular','rectangle':'rectangular','square':'square','round':'round','circle':'round','circular':'round','oval':'oval','l-shaped':'l-shaped','l-shape':'l-shaped','u-shaped':'u-shaped','hexagon':'hexagonal','octagonal':'octagonal'}
MAT={}
for k in ['metal','brass','stainless steel','steel','aluminum','zinc','cast iron','metal/wire','solid brass','iron','wrought iron','copper','bronze']: MAT[k]='metal'
for k in ['wood','solid wood','manufactured wood','solid + manufactured wood','bamboo','engineered wood']: MAT[k]='wood'
for k in ['plastic','resin','acrylic','vinyl','pvc','polypropylene','resin/plastic','melamine','polyethylene']: MAT[k]='plastic'
for k in ['glass','crystal']: MAT[k]='glass'
for k in ['ceramic','porcelain','stoneware','earthenware','porcelain china']: MAT[k]='ceramic'
for k in ['fabric','polyester','cotton','100 % cotton','synthetic fiber','linen','velvet','wool','microfiber']: MAT[k]='fabric'
for k in ['coir','wicker/rattan','jute','seagrass','rattan','wicker']: MAT[k]='natural fiber'
for k in ['stone','marble','granite','concrete']: MAT[k]='stone'
COL={}
def fam(words,f):
    for w in words: COL[w]=f
fam(['white','off-white','off white','antique white','snow'],'white')
fam(['black','ebony'],'black')
fam(['gray','grey','light gray','dark gray','charcoal','charcoal gray','silver gray','slate'],'gray')
fam(['brown','espresso','walnut','dark brown','light brown','cherry','chocolate','cappuccino','dark walnut','mahogany','oak','coffee'],'brown')
fam(['blue','navy','navy blue','light blue','turquoise','aqua','teal','dark blue','royal blue'],'blue')
fam(['beige','ivory','cream','tan','taupe','ivory & cream','khaki','sand'],'beige')
fam(['green','sage','olive','mint','emerald'],'green')
fam(['red','burgundy','maroon','crimson'],'red')
fam(['pink','blush','rose','coral'],'pink')
fam(['yellow','mustard','gold yellow'],'yellow')
fam(['orange','rust'],'orange')
fam(['purple','lavender','plum','violet'],'purple')
fam(['silver','chrome','stainless steel','nickel','brushed nickel'],'silver')
fam(['gold','brass','antique brass'],'gold')
fam(['clear','transparent'],'clear')
fam(['multicolor','multi','multi-color','multi color'],'multicolor')
def color(v):
    if not v: return None
    if '/' in v or '&' in v and v not in COL: 
        parts=[p.strip() for p in re.split(r'[/&]',v)]
        fams={COL.get(p) for p in parts}
        if None in fams: return None
        return 'multicolor' if len(fams)>1 else fams.pop()
    return COL.get(v)
rows=[]
for r in df.itertuples():
    d=feats(r.product_features)
    lab={'style':STYLE.get(d.get('dsprimaryproductstyle')),'color':color(d.get('color')),'shape':SHAPE.get(d.get('shape')),'material':MAT.get(d.get('primarymaterial'))}
    desc=r.product_description if isinstance(r.product_description,str) else ''
    rows.append(dict(product_id=int(r.product_id),name=r.product_name,product_class=r.product_class if isinstance(r.product_class,str) else '',description=desc,labels={k:v for k,v in lab.items() if v}))
print('labelled share in full catalogue:',{k:round(sum(1 for x in rows if k in x['labels'])/len(rows)*100,1) for k in ['style','color','shape','material']})
withdesc=[x for x in rows if len(x['description'])>=80]
lab=[x for x in withdesc if x['labels']]
none=[x for x in withdesc if not x['labels']]
random.seed(20261120); random.shuffle(lab); random.shuffle(none)
dev, test = lab[:20], lab[20:320]
for name, smp in [('dev', dev), ('test', test)]:
    json.dump([{k: p[k] for k in ['product_id', 'name', 'product_class', 'description']} for p in smp], open(f'data/input/{name}.json', 'w'), ensure_ascii=False)
    json.dump({str(p['product_id']): p['labels'] for p in smp}, open(f'data/labels/{name}-labels.json', 'w'), indent=0)
    print(name, len(smp), {k: sum(1 for x in smp if k in x['labels']) for k in ['style', 'color', 'shape', 'material']})
import collections
print({k:collections.Counter(x['labels'][k] for x in test if k in x['labels']).most_common() for k in ['style','color','shape','material']})
