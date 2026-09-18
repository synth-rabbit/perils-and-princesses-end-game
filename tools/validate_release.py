#!/usr/bin/env python3
"""Validate release references, permissions, stable IDs, and key adventure rules."""
from pathlib import Path
import json,re,subprocess
R=Path(__file__).resolve().parents[1];B=R/'build';m=json.loads((B/'module.json').read_text());docs={};uuids=set()
for pack in m['packs']:
 name=pack['name'].removeprefix('pnp-endgame-');paths=list((B/'src'/name).glob('*.json'));assert paths,pack
 docs[name]=[json.loads(p.read_text()) for p in paths];assert len({d['_id'] for d in docs[name]})==len(paths)
 assert pack['ownership']['PLAYER']=='NONE' and pack['ownership']['TRUSTED']=='NONE'
 for d in docs[name]:
  assert d['ownership']['default']==0,(name,d['name'])
  uuids.add(f'Compendium.pnp-end-game.{pack["name"]}.{pack["type"]}.{d["_id"]}')
  for asset in re.findall(r'modules/pnp-end-game/([^"<>\s)]+)',json.dumps(d)):
   asset=asset.rstrip(chr(92))
   assert (B/asset).exists(),(d['name'],asset)
  # IDs of existing compendium entries must remain stable.
  filename=next(p for p in paths if json.loads(p.read_text())['_id']==d['_id'])
  old=subprocess.run(['git','show','HEAD:'+str(filename.relative_to(R))],cwd=R,capture_output=True,text=True)
  if old.returncode==0:assert json.loads(old.stdout)['_id']==d['_id']
for group in docs.values():
 for d in group:
  for ref in re.findall(r'@UUID\[([^]]+)\]',json.dumps(d)):assert ref in uuids,(d['name'],ref)
  assert '[[' not in json.dumps(d),(d['name'],'unconverted wiki link')
a={d['name']:d for d in docs['actors']};i={d['name']:d for d in docs['items']}
assert a['Princess Embra (Impostor)']['system']['hp']['max']==8
assert a['Princess Embra (Impostor)']['system']['save']['value']=='15'
assert 'original was destroyed' not in i['The Gnomish Magical Key']['system']['description']
assert 'Nearby' in i['The Magic Necklaces']['system']['description']
assert 'Blood-Forged' not in a['Sir Damon the Unyielding']['system']['notes']
assert 'Animate, Restoration, Disguise, Haste' in a['Magus Ulrik']['system']['notes']
for d in docs['handouts']:
 body=d['pages'][0]['text']['content']
 assert 'GM answer' not in body and '**GM' not in body and '@UUID' not in body
assert len(docs['handouts'])==9
assert m['download'].endswith('pnp-end-game-'+m['version']+'.zip')
print('PASS:',', '.join(f'{len(v)} {k}' for k,v in docs.items()),'— assets, links, permissions, existing IDs and adventure invariants')
