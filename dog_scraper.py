import re

import requests
from bs4 import BeautifulSoup


def get_http_response(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Can't get http response!")

    return response


def create_beautiful_soup_obj(html_content: str):
    response_soup = BeautifulSoup(html_content, features="html.parser")

    return response_soup


def get_and_add_hrefs_to_description(description):
    description_plus_hrefs = ""
    for d in description:
        if str(d).startswith('<a'):
            description_plus_hrefs += d.text + f"({d.get('href')})"
        else:
            description_plus_hrefs += str(d)

    return description_plus_hrefs


def get_dogs_data(bs_obj):
    # number, breed, image, description, data->[height, weight, life_exp.]
    numbers_list, breeds_list, images_list, descriptions_list, data_list = [], [], [], [], []
    dogs_divs = bs_obj.select('div.css-10fz3m9')
    for div in dogs_divs:
        data = {}
        number = div.select('span.e1tmud0h5')[0].string
        breed = div.select('h2.e1tmud0h8')[0].string
        img_src = div.select('img')[0].get('src')
        description = get_and_add_hrefs_to_description(div.find('p', class_='et3p2gv0').contents)
        d = div.select('ul.et3p2gv0')[0].select('li')
        for li in d:
            data_key = li.findChild().text
            data_value = li.text.split(":")[-1].strip()
            data.update({data_key: data_value})

        numbers_list.append(number)
        breeds_list.append(breed)
        images_list.append(f"{img_src}")
        descriptions_list.append(description)
        data_list.append(data)

    numbers_list = [int(x.strip()) for x in numbers_list]
    breeds_list = [x.strip() for x in breeds_list]

    result_data_keys = ['number', 'breed', 'img_url', 'description', 'data']
    result_data_set = {}

    k = 0
    k2 = 1
    dogs = list(zip(numbers_list, breeds_list, images_list, descriptions_list, data_list))
    for dog in dogs:
        tmp = {}
        for p in dog:
            tmp.update({result_data_keys[k]: p})
            k += 1
        result_data_set.update({k2: tmp})
        k2 += 1
        k = 0

    return result_data_set


def main():
    url = "https://www.goodhousekeeping.com/life/pets/g4748/top-smartest-dog-breeds/"

    response = get_http_response(url)
    response_soup = create_beautiful_soup_obj(response.text)

    result_data = get_dogs_data(response_soup)

    print(result_data)
    print(len(result_data))


if __name__ == "__main__":
    main()

