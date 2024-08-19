import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"}

parts_sites ={"+":[("www.lazada.vn" , "https://www.lazada.vn/tag/headphone"), ("www.thegioididong.com", "https://www.thegioididong.com/tai-nghe")] }

def scrape_site(site, part_name, soup):

    if(site == 'www.lazada.vn'):
        site_function = lazada
    elif (site == "www.thegioididong.com"):
        site_function = thegioididong

    part_list = site_function(soup, part_name, site)
    return part_list

# #HEADPHONEZONE

def thegioididong(soup, part_name, site):
    
    driver = webdriver.Chrome()

    driver.get("https://www.thegioididong.com/tai-nghe")

    driver.implicitly_wait(10)
    part_list = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    products = soup.find_all('li', class_ = "item __cate_54")

    for product in products:
        try:
            name = product.find('h3').text.strip()
            price = product.find('strong', class_='price').text
            link = "https://www.thegioididong.com" + product.a['href']
            img_link = product.find('img')['src']
            flag = 0
            for word in part_name.split():
                if (word not in name.lower().split()):
                    flag = 1
                    break
            if (flag == 0):
                part_list.append((name,price,link, img_link,site))
        except:
            continue
    return part_list

def lazada(soup, part_name, site):
    driver = webdriver.Chrome() 
    driver.get("https://www.lazada.vn/tag/headphone")
    driver.implicitly_wait(10)

    part_list = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    products = soup.find_all('div', class_='qmXQo')

    for product in products[0:10]:
        try:
            name = product.find('div',class_='RfADt').text
            price = product.find('span', class_='ooOxS').text
            link = product.find('div',class_='_95X4G').a['href']
            img_link = product.find('img')['src']
            flag = 0
            for word in part_name.split():
                if (word not in name.lower().split()):
                    flag = 1
                    break
            if (flag == 0):
                part_list.append((name,price,link,img_link,site))
        except:
            continue
    driver.quit()
    return part_list

