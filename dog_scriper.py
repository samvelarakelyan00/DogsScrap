import requests
from bs4 import BeautifulSoup


url = "https://www.goodhousekeeping.com/life/pets/g4748/top-smartest-dog-breeds/"


response = requests.get(url)
response_soup = BeautifulSoup(response.text, features="html.parser")

print(response_soup.prettify())


# number, breed, image, description, data
