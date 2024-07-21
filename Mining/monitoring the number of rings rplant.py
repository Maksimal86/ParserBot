import sys, requests, lxml
import traceback

from bs4 import BeautifulSoup

def get_soup():
    responce = requests.get(get_url())
    soup = BeautifulSoup(responce.text, 'lxml')
    return soup

def get_url():
    return 'https://pool.rplant.xyz/'

def get_headers():
    print(get_soup().get_text().encode('utf-8')) #сохранить в файл

get_headers()