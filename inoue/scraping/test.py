import numpy as np
import requests
from bs4 import BeautifulSoup
import io
import re
url = 'http://west2-univ.jp/sp/kyoto-univ.php'
res = requests.get(url)
# print(res.text)

soup = BeautifulSoup(res.text, 'html.parser')
elems = soup.find_all(href=re.compile("index.php"))
links = []
for i in range(len(elems)):
    # print(i)
    links.append(('http://west2-univ.jp/sp/'+elems[i].attrs['href']).replace('index','menu'))

print(links[2])
print(links[4])
res = requests.get(links[0])
print(res.text)

links = np.unique(links)
text='\n'.join(links)
with io.open('article-url.txt', 'w', encoding='utf-8') as f:
    f.write(text)
