# coding: utf-8
import numpy as np
import requests
from bs4 import BeautifulSoup
import codecs
import io
import re

price_lim = 550
red_target = 27
green_target = 10
yellow_target = 57

name = []
price = []
red = []
green = []
yellow = []

ans = []

def menu(menu_tmp, num, price_tmp, red_tmp, green_tmp, yellow_tmp):
    for i in range(num, n):
        next_price_tmp = price_tmp + price[i]
        next_red_tmp = red_tmp + red[i]
        next_green_tmp = green_tmp + green[i]
        next_yellow_tmp = yellow_tmp + yellow[i]

        if next_price_tmp <= price_lim:
            next_menu_tmp = menu_tmp.copy()
            next_menu_tmp.append(name[i])
            menu(next_menu_tmp, i + 1, next_price_tmp, next_red_tmp, next_green_tmp, next_yellow_tmp)

    menu_tmp.append(price_tmp)


    if red_tmp >= red_target and green_tmp >= green_target and yellow_tmp >= yellow_target:
        ans.append(menu_tmp)

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
    text = ''
    soup = BeautifulSoup(res.text, 'html.parser')
    elems = soup.find_all(href=re.compile("detail.php"))
    for j in range(len(elems)):
        m_links[i].append(('http://west2-univ.jp/sp/'+elems[j].attrs['href']))

    n = 0
    name = []
    price = []
    red = []
    green = []
    yellow = []

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
            # ???????????????????????????????????????? ???????????????
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
        n+=1
        name.append(cur_dat[0])
        price.append(int(cur_dat[1]))
        # print(len(cur_dat))
        if(len(cur_dat)==12):
            red.append(round(float(10*cur_dat[9])))
            green.append(round(float(10*cur_dat[10])))
            yellow.append(round(float(10*cur_dat[11])))
        else:
            red.append(0)
            green.append(0)
            yellow.append(0)

        # print(cur_dat)
        # text = text + ' '.join(str(cur_dat))
        # text = text + '\n'

    ans = []

    menu([], 0, 0, 0, 0, 0)

    for i in ans:
        print(i)
    # print(text)
    # f = codecs.open(str(i)+'.txt', 'w', encoding='shift_jis')
    # f = codecs.open(str(i)+'.txt', 'w', encoding='utf-8')
    # f.write(text)
    # f.close()

# print(res.text)
