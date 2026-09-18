#!/usr/bin/env python3
"""Build private Foundry journals from committed Markdown, with stable IDs."""
from pathlib import Path
import hashlib,json,re,html
import markdown
ROOT=Path(__file__).resolve().parents[1]
def did(s):return hashlib.sha1(s.encode()).hexdigest()[:16]
def clean(s):return re.sub(r'^---\n.*?\n---\n','',s,flags=re.S)
def title(p):return re.search(r'^# (.+)',clean(p.read_text()),re.M).group(1)
sources={p.stem:(p,pack) for folder,pack in [('gm','journals'),('handouts','handouts')] for p in (ROOT/'content'/folder).glob('*.md')}
refs={key:f'Compendium.pnp-end-game.pnp-endgame-{pack}.JournalEntry.{did("journal:"+key)}' for key,(p,pack) in sources.items()}
for pack,kind in [('actors','Actor'),('items','Item')]:
 for p in (ROOT/'build/src'/pack).glob('*.json'):
  d=json.loads(p.read_text());key=re.sub(r'[^a-z0-9]','',d['name'].lower());refs.setdefault(key,f'Compendium.pnp-end-game.pnp-endgame-{pack}.{kind}.{d["_id"]}')
# Source-name aliases for existing stable actor IDs.
aliases={'Embra':'Princess Embra (Impostor)','Princess_Amy':'Princess Amy (Restored)','Robin':"Robin, Finnian's Squire",'Scamp':'Scamp the Squirrel','Drakenshire_Royal_Guard':'Royal Guard','Pippin_Cobbleton':'Pippin Cobbleton','Tifa':'Tifa Bramblebush'}
for key,name in aliases.items():refs[key]=refs[re.sub(r'[^a-z0-9]','',name.lower())]
# Ten location references point to the corresponding card in the full runbook.
for key in ['The_Scorchwoods','01_Cave','02_Boneyard','03_Stump','04_Gnomes','05_Pool','06_Flowers','07_Orchard','08_Stones','09_Cottage','10_Camp']:refs[key]=refs['princess_and_dragon_runbook']
art={p.name:'modules/pnp-end-game/art/'+str(p.relative_to(ROOT/'build/art')) for p in (ROOT/'build/art').rglob('*') if p.is_file()}
def wikilink(m):
 value=m.group(1);target,_,label=value.partition('|');label=label or target.split('#')[0].replace('_',' ');target=target.split('#')[0]
 dest=refs.get(target) or refs.get(re.sub(r'[^a-z0-9]','',target.lower()))
 if target.split('/')[-1] in art:return '['+label+']('+art[target.split('/')[-1]]+')'
 return '@UUID['+dest+']{'+label+'}' if dest else label
for key,(p,pack) in sorted(sources.items()):
 s=clean(p.read_text());s=re.sub(r'!\[\[([^]]+)\]\]',lambda m:'![]('+art[m.group(1).split('/')[-1]]+')' if m.group(1).split('/')[-1] in art else '',s)
 s=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',lambda m:'!['+m.group(1)+']('+art[m.group(2).split('/')[-1]]+')' if m.group(2).split('/')[-1] in art else '',s)
 s=re.sub(r'\[\[([^]]+)\]\]',wikilink,s)
 # Python Markdown needs separation before lists following prose.
 s=re.sub(r'([^\n])\n(?=[-*] )',r'\1\n\n',s)
 body=markdown.markdown(s,extensions=['tables','fenced_code','sane_lists'])
 name=title(p);jid=did('journal:'+key);pid=did('page:'+key)
 page={'_key':f'!journal.pages!{jid}.{pid}','_id':pid,'name':name,'type':'text','sort':0,'title':{'show':True,'level':1},'text':{'content':body,'format':1},'ownership':{'default':-1}}
 doc={'_id':jid,'name':name,'pages':[page],'ownership':{'default':0},'_key':f'!journal!{jid}'}
 out=ROOT/'build/src'/pack;out.mkdir(parents=True,exist_ok=True);(out/(key+'.json')).write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n')
print('Journals:',sum(x[1]=='journals' for x in sources.values()),'; separate private handouts:',sum(x[1]=='handouts' for x in sources.values()))
