import json, urllib.request, urllib.parse, os
UA={'User-Agent':'UebiHub-logo-test/1.0 (contato@uebihub.com)'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
brands=['Dove','La Roche-Posay','Huggies','Pampers','Colgate','Garnier','Cetaphil','Rexona','Listerine','Oral-B']
out={}
for b in brands:
    q=urllib.parse.urlencode({'action':'query','list':'search','srnamespace':6,'srsearch':f'{b} logo','format':'json','srlimit':20})
    res=json.loads(get('https://commons.wikimedia.org/w/api.php?'+q))['query']['search']
    for r in res:
        t=r['title']
        key=b.lower().split()[0].replace('-',' ').split()[0]
        if not any(k in t.lower() for k in ['logo','wordmark']) or key not in t.lower().replace('-',' '): continue
        q2=urllib.parse.urlencode({'action':'query','titles':t,'prop':'imageinfo','iiprop':'url','iiurlwidth':600,'format':'json'})
        pg=list(json.loads(get('https://commons.wikimedia.org/w/api.php?'+q2))['query']['pages'].values())[0]
        ii=pg.get('imageinfo',[{}])[0]; u=ii.get('thumburl') or ii.get('url')
        if not u: continue
        fn='tmp/marcas/'+b.lower().replace(' ','-').replace("'",'')+'.png'
        open(fn,'wb').write(get(u)); out[b]=t; break
json.dump(out,open('tmp/marcas/fontes2.json','w'),indent=1,ensure_ascii=False)
print(out)
