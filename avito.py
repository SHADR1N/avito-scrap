from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import requests, pickle
from bs4 import BeautifulSoup as bs
from models import *

proxy = 'https://4WtLdh:Tfx6CD@5.101.71.97:8000'

headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36 OPR/42.7.2246.114996',
        'Accept': '*/*',
        'Referer':'https://www.m.avito.ru/rossiya',
        'Connection':'keep-alive',
        'Accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,lt;q=0.6'}



def get_phone(driver, id_link, token):

    link = f'https://m.avito.ru/api/1/items/{id_link}/phone?key={token}'
    driver.get(link)
    sleep(2)
    dr = driver.find_element_by_xpath('//pre').text
    templates = json.loads(dr)
    if 'Телефон недоступен' in str(templates):
        return 'Телефон недоступен'
    phone =  str(templates['result']['action']['uri']).split('%2B')[1].strip()
    return phone



def get_data_requests(link, driver):
    soup = get_session(link, driver)
    if soup.findAll('span', class_="css-1axmv3b"):
        return 1,2,3,4,5,6,7,8
    if soup.findAll('span', {'data-marker': "seller-info/name"}):
        name = soup.find('span', {'data-marker': "seller-info/name"}).text
        location = soup.find('span', {'data-marker': "delivery/location"}).text
        views = soup.find('div', {'data-marker': "item-stats/views"}).text
        person = soup.find('span', {'data-marker': 'seller-info/postfix'}).text
        date = soup.find('div', {'data-marker': "item-stats/timestamp"}).find('span').text
        if soup.findAll('span', {'data-marker': "item-description/price"}):
            price = soup.find('span', {'data-marker': "item-description/price"}).text

        else:
            price = 'Не указано'

        name_product = soup.find('h1', {'data-marker': "item-description/title"}).text

    else:
        name = soup.find('span', {'data-marker': "marketplace-title/title"}).text
        views = soup.find('span', class_="css-llflfb").text
        views = views.split(',')[0].strip()
        location = 'Не указано'
        person = soup.find('span', {'data-marker': 'marketplace-seller-info/postfix'}).text
        date = 'Не указано'
        name_product = soup.find('span', {'data-marker': "marketplace-title/title"}).text
        if soup.findAll('span', {'data-marker': "marketplace-title/price"}):
            price = soup.find('span', {'data-marker': "marketplace-title/price"}).text

        else:
            price = 'Не указано'
  
    


    if soup.findAll('div', {'data-marker': "item-description/text"}):
        description = soup.find('div', {'data-marker': "item-description/text"}).text
    else:
        description = 'Без описания'

    

    return name, location, views, name_product, date, price, description, person


def get_driver_proxy():
    all_proxy = ProxyList.select().where(ProxyList.Role == 'Default')
    for proxy in all_proxy:

        options = {
            'proxy': {
                'https': f'https://{proxy.Proxy}'
            }
        }

        chrome_options = Options()
        #chrome_options.add_argument(f"--headless") 
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36 OPR/42.7.2246.114996')
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options, seleniumwire_options=options)
        driver.get('https://www.avito.ru/izhevsk')
        sleep(2)
        soup = bs(driver.page_source, 'html.parser')

        if 'Доступ с вашего IP-адреса временно ограничен' not in str(soup):
            return driver
        driver.quit()

    else:
        chrome_options = Options()
        #chrome_options.add_argument(f"--headless") 
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36 OPR/42.7.2246.114996')
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
        driver.get('https://www.avito.ru/izhevsk')
        sleep(2)
        soup = bs(driver.page_source, 'html.parser')
        if 'Доступ с вашего IP-адреса временно ограничен' not in str(soup):
            return driver

        driver.quit()
        return False


def get_driver():
    proxy = ProxyList.get(ProxyList.Role == 'Main').Proxy

    options = {
        'proxy': {
            'https': f'https://{proxy}'
        }
    }

    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir=youla") 
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options, seleniumwire_options=options)
    return driver




def get_session(link, driver):
    driver.get(link)
    sleep(2)
    soup = bs(driver.page_source, 'html.parser')
    return soup

def get_links_page(soup):

    page = soup.find('div', {'data-marker': "items/list"})
    page = page.findAll('div', {'itemtype': "http://schema.org/Product"})

    Links = []
    for link in page:
        links = link.find('a', {'data-marker': "item/link"}, href=True)
        link = f'https://avito.ru{links["href"]}'
        Links.append(link)


    return Links


def get_all_link(link, token, driver_autorizate, driver):
    soup = get_session(link, driver)
    Links = get_links_page(soup)


    answer = []
    for link in Links:

        id_link = link.split('_')[-1]
        phone = get_phone(driver_autorizate, id_link, token)
        name, location, views, name_product, date, price, description, person = get_data_requests(link, driver)
        if name == 1:
            continue

        answer.append([name, location, views, name_product, date, price, description, person, phone])
        print(f'Телефон: {phone}\n'
                f'Имя: {name}\n'
                f'Город: {location}\n'
                f'{views}\n'
                f'Наименование: {name_product}\n'
                f'Дата: {date}\n'
                f'Цена: {price}\n'
                f'Описание: {description}\n'
                f'Тип продавца: {person}\n'
                )

    return answer







me = ''
you = 'af0deccbgcgidddjguijhdinfgjgfjir'

link = 'https://www.avito.ru/izhevsk/lichnye_veschi'

driver_autorizate = get_driver()
driver = get_driver_proxy()

if driver == False:
    print('Пополните список IP адресов.')
    
else:
    get_all_link(link, me, driver_autorizate, driver)
    driver.quit()
    driver_autorizate.quit()

