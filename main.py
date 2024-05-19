import requests
from bs4 import BeautifulSoup
import csv

url_main = 'https://www.lego.com'
url_themes = 'https://www.lego.com/en-us/themes'


def get_soup(url, page=1):
    if page == 1:
        r = requests.get(url=url)
    else:
        url = f'{url}?page={page}&offset=0'
        r = requests.get(url=url)

    with open(file='index.html', mode='w') as file:
        file.write(r.text)

    return BeautifulSoup(r.text, 'lxml')


def get_themes(soup):
    themes = soup.find('section').ul
    themes = themes.find_all('li')

    themes_list = []

    for theme in themes:
        themes_dict = {
            'name': theme.h2.span.text,
            'url': f'{url_main}{theme.a.get("href")}'
        }

        themes_list.append(themes_dict)

    keys = themes_list[0].keys()

    with open('themes.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(themes_list)

    return themes_list


def get_toys_pages(soup):
    n_toys = int(soup.select('span[data-value]')[0].get('data-value'))
    n_pages = n_toys // 18 + 1

    return n_toys, n_pages


def get_toys_info(toy_data):
    t_data = {
        'age': None,
        'pieces': None,
        'rating': None
    }
    
    for d in toy_data:
        if '+' in d:
            t_data['age'] = d
        elif '.' in d:
            t_data['rating'] = d
        else:
            t_data['pieces'] = d

    return t_data


def get_price(toy):
    price_div = toy.find('div', {'data-test': 'product-leaf-price-row'}).text
    t_price = toy.find('span', {'data-test': 'product-leaf-price'}).text

    if '%' in price_div:
        t_discount = toy.find('span', {'data-test': 'product-leaf-discounted-price'}).text
        return t_price, t_discount
    else:
        return t_price, 0


def get_toys_values(collection='Marvel'):

    with open(file='index.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    toys = soup.find_all('li', {'data-test': 'product-item'})

    toys_data = []

    for toy in toys:
        toy_name = toy.find('h3').text.strip()
        # print(toy_name)
        toy_data = [item.text.strip() for item in toy.find('div', {'data-test': 'product-leaf-attributes-row'}).find_all('span')]
        toy_data = get_toys_info(toy_data=toy_data)
        # print(toy_data)
        price, discount = get_price(toy)
        # print(price, discount)
        toy_info = {
            'name': toy_name,
            'collection': collection,
            'age': toy_data['age'],
            'pieces': toy_data['pieces'],
            'rating': toy_data['rating'],
            'price': price,
            'discount': discount
        }

        toys_data.append(toy_info)

    keys = toys_data[0].keys()

    with open('toys_data.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toys_data)

    return toys_data

def main():
    # soup = get_soup(url=url_themes)
    # themes = get_themes(soup=soup)
    # print(themes)

    # soup = get_soup(url='https://www.lego.com/en-us/themes/star-wars')
    # print(get_toys_pages(soup=soup))

    # soup = get_soup(url='https://www.lego.com/en-us/themes/marvel')
    get_toys_values()


if __name__ == '__main__':
    main()
