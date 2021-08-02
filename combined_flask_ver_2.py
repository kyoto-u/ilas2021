'''Copyright 2021 Ryoto Nishida, Masahiro Inoue
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.'''

# coding: utf-8
import numpy as np
import requests
from bs4 import BeautifulSoup
import codecs
import io
import re
import sys

try:
    price_lim = int(input('上限金額を入力してください。 '))
except ValueError:
    print('エラー：数字を入力してください。')
    sys.exit()
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
            menu(next_menu_tmp, i + 1, next_price_tmp,
                 next_red_tmp, next_green_tmp, next_yellow_tmp)

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
    links.append(('http://west2-univ.jp/sp/' +
                 elems[i].attrs['href']).replace('index', 'menu'))

links = np.unique(links)
text = '\n'.join(links)
with io.open('article-url.txt', 'w', encoding='utf-8') as f:
    f.write(text)

m_links = [[]for i in range(len(elems))]

try:
    i = int(input('どの食堂か数字を入力してください。0:中央 1:吉田 2:北部 3:南部 4:ルネ '))
except ValueError:
    print('エラー：1から5の数字を入力してください。')
    sys.exit()

if i < 0 or i > 4:
    print('エラー：1から5の数字を入力してください。')
    sys.exit()

else:
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
        menu_str = menu_str.replace('<h1>', '')
        menu_str = menu_str.replace('</h1>', '')
        menu_str = menu_str.replace('<span>', '(')
        menu_str = menu_str.replace('</span>', ')')
        # print(menu_str)
        cur_dat.append(menu_str)

        elems = soup.find_all(class_="price")
        for k in range(len(elems)):
            # print(elems[k])
            cur_lis = re.findall(r"[-+]?\d*\.\d+|\d+", str(elems[k]))
            # メニューの複数サイズの対応? 知らんな…
            if len(cur_lis) >= 1:
                cur_dat.append(float(cur_lis[0]))

        elems = soup.find_all(class_="score")
        scspl = str(elems[0]).split('\n')
        for k in range(len(scspl)):
            # print(scspl[k])
            if ('Red' in scspl[k]) or ('Green' in scspl[k]) or ('Yellow' in scspl[k]):
                cur_lis = re.findall(r"[-+]?\d*\.\d+|\d+", scspl[k])
                if len(cur_lis) >= 1:
                    cur_dat.append(float(cur_lis[0]))
        n += 1
        name.append(cur_dat[0])
        price.append(int(cur_dat[1]))
        # print(len(cur_dat))
        if(len(cur_dat) == 12):
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

    name.append('ライスSS(Boiled rice SS)')
    price.append(73)
    red.append(0)
    green.append(0)
    yellow.append(21)

    name.append('ライスS(Boiled rice S)')
    price.append(94)
    red.append(0)
    green.append(0)
    yellow.append(36)

    name.append('ライスL(Boiled rice L)')
    price.append(136)
    red.append(0)
    green.append(0)
    yellow.append(66)

    name.append('ライスLL(Boiled rice LL)')
    price.append(181)
    red.append(0)
    green.append(0)
    yellow.append(98)

    n += 4

    if i != 1 or i != 3:
        name.append('ライスM(Boiled rice M)')
        price.append(115)
        red.append(0)
        green.append(0)
        yellow.append(51)
        n += 1

    ans = []

    menu([], 0, 0, 0, 0, 0)

    try:
        way_of_sort = int(input('金額の昇順で表示する場合は1、降順の場合は0を入力してください。 '))
    except ValueError:
        print('エラー：1から5の数字を入力してください。')
        sys.exit()

    if way_of_sort != 0 and way_of_sort != 1:
        print('エラー：0か1を入力してください。')
        sys.exit()
    elif way_of_sort == 1:
        ans = sorted(ans, key=lambda x: x[-1])
    else:
        ans = sorted(ans, reverse=True, key=lambda x: x[-1])

    try:
        num_of_menu = int(input('表示するメニュー数を入力してください。 '))
    except ValueError:
        print('エラー：数字を入力してください。')
        sys.exit()
    for i in range(min(len(ans), num_of_menu)):
        print('')
        for j in range(len(ans[i])):
            if j == len(ans[i]) - 1:
                print('合計金額：' + str(ans[i][j]) + '円')
            else:
                print(ans[i][j])
    # print(text)
    # f = codecs.open(str(i)+'.txt', 'w', encoding='shift_jis')
    # f = codecs.open(str(i)+'.txt', 'w', encoding='utf-8')
    # f.write(text)
    # f.close()

# print(res.text)
