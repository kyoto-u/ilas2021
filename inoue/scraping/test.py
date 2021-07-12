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

links = np.unique(links)
text='\n'.join(links)
with io.open('article-url.txt', 'w', encoding='utf-8') as f:
    f.write(text)

m_links = [[]for i in range(len(elems))]

for i in range(len(links)):
    url = links[i]
    res = requests.get(url)
    print('looking ' + url + ' ...')
    soup = BeautifulSoup(res.text, 'html.parser')
    elems = soup.find_all(href=re.compile("detail.php"))
    for j in range(len(elems)):
        m_links[i].append(('http://west2-univ.jp/sp/'+elems[j].attrs['href']))
    for j in range(len(m_links[i])):
        # print('looking ' + m_links[i][j] + ' ...')
        cur_dat = []
        url = m_links[i][j]
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        elems = soup.find_all("h1")
        menu_str = str(elems[1])
        menu_str = menu_str.replace('<h1>','')
        menu_str = menu_str.replace('</h1>','')
        menu_str = menu_str.replace('<span>','(')
        menu_str = menu_str.replace('</span>',')')
        # print(menu_str)
        cur_dat.append(menu_str)

        elems = soup.find_all(class_="price")
        for k in range(len(elems)):
            # print(elems[k])
            cur_lis = re.findall(r"[-+]?\d*\.\d+|\d+",str(elems[k]))
            # メニューの複数サイズの対応? 知らんな…
            if len(cur_lis)>=1:
                cur_dat.append(float(cur_lis[0]))

        elems = soup.find_all(class_="score")
        scspl = str(elems[0]).split('\n')
        for k in range(len(scspl)):
            # print(scspl[k])
            if ('Red' in scspl[k]) or ('Green' in scspl[k]) or ('Yellow' in scspl[k]):
                cur_lis = re.findall(r"[-+]?\d*\.\d+|\d+",scspl[k])
                if len(cur_lis)>=1:
                    cur_dat.append(float(cur_lis[0]))
        print(cur_dat)

# print(res.text)
