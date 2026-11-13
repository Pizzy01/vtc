import re,html,os
os.chdir('/home/claude/vtc')
NEW={
 'corporate-chauffeur-geneva/index.html':(None,"Corporate chauffeur service in Geneva for executives, banks, international organisations and roadshows. Mercedes S-Class and V-Class, one contact."),
 'wef-davos-chauffeur/index.html':(None,"Private chauffeur for the World Economic Forum in Davos, January 2027. Mercedes S-Class and V-Class VIP, by the day or per transfer, from Zurich or Geneva."),
 'fr/chauffeur-prive-business-geneve/index.html':("Chauffeur privé business à Genève | Prosper &amp; Co.","Chauffeur privé business à Genève : dirigeants, banques, organisations internationales. Mercedes Classe S et Classe V, facturation société."),
 'fr/chauffeur-prive-diplomate-geneve/index.html':("Chauffeur privé diplomate Genève | Prosper &amp; Co.","Chauffeur privé pour diplomates et délégations à Genève : Palais des Nations, conférences, visites officielles. Mercedes Classe S et V, un seul contact."),
}
fp='/home/claude/outils/fr_pages.py'; F=open(fp).read()
for p,(t,d) in NEW.items():
    s=open(p).read()
    if t:
        old=re.search(r'<title>(.*?)</title>',s).group(1); F=F.replace(old,t)
        s=s.replace('<title>%s</title>'%old,'<title>%s</title>'%t)
        s=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m.group(1)+t.replace(' | ',' · '),s,count=1)
    oldd=re.search(r'<meta name="description" content="([^"]*)"',s).group(1); F=F.replace(oldd,d)
    for k in ('name="description"','property="og:description"'):
        s=re.sub(r'(<meta %s content=")[^"]*'%k,lambda m:m.group(1)+d,s,count=1)
    open(p,'w').write(s)
    tt=html.unescape(re.search(r'<title>(.*?)</title>',s).group(1)); print(p,len(tt),len(d))
open(fp,'w').write(F)
