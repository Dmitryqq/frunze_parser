import re

f = open('sitemap.xml','r')
o = open('links.txt', 'w')

res = f.readlines()
x=0
for d in res:
    data = re.findall('<loc>(http:\/\/.+)<\/loc>',d)
    for i in data:
        o.writelines(i+'\n')
        x+=1
print("Parsed %d links" % x)
