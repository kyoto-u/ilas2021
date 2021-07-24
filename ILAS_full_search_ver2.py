name = []
price = []
red = []
green = []
yellow = []

n = int(input())

for i in range(n):
    name_tmp, price_tmp, red_tmp, green_tmp, yellow_tmp = input().split()
    name.append(name_tmp)
    price.append(int(price_tmp))
    red.append(round(float(red_tmp) * 10))
    green.append(round(float(green_tmp) * 10))
    yellow.append(round(float(yellow_tmp) * 10))

ans = []

def menu(menu_tmp, num, price_tmp, red_tmp, green_tmp, yellow_tmp):
    for i in range(num, n):
        next_price_tmp = price_tmp + price[i]
        next_red_tmp = red_tmp + red[i]
        next_green_tmp = green_tmp + green[i]
        next_yellow_tmp = yellow_tmp + yellow[i]

        if next_price_tmp <= 550:
            next_menu_tmp = menu_tmp.copy()
            next_menu_tmp.append(name[i])
            menu(next_menu_tmp, i + 1, next_price_tmp, next_red_tmp, next_green_tmp, next_yellow_tmp)
    
    menu_tmp.append(price_tmp)


    if red_tmp >= 27 and green_tmp >= 10 and yellow_tmp >= 57:
        ans.append(menu_tmp)

menu([], 0, 0, 0, 0, 0)

for i in ans:
    print(i)