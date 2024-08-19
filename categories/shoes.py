import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

parts_sites={
    "+":[
          ("www.tiki.vn","https://tiki.vn/giay-dep-nam/c1686"),
          ("www.lazada.vn","https://www.lazada.vn/giay-sneaker-nam/?spm=a2o4n.searchlistcategory.cate_9_2.1.7003564fFAL7Rj")
        ]
}


def scrape_site(site, part_name, soup):
    if(site == "www.tiki.vn"):
        site_function=tiki
    elif(site == "www.lazada.vn"):
        site_function=lazada
    part_list=site_function(soup, part_name,site)
    return part_list

def tiki(soup, part_name, site):
    driver = webdriver.Chrome() 

    driver.get("https://tiki.vn/giay-dep-nam/c1686")

    driver.implicitly_wait(10)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    products = soup.find_all('div', class_='styles__ProductItemContainerStyled-sc-bszvl7-0 elOGIo')
    part_list=[]
    for product in products:
        try:
            info = product.find('div', class_='info')
            title = info.find('h3').text
            price = info.find('div', class_='price-discount__price').text
            link = ""

            img_ = product.find('div', class_='image-wrapper')
            img_links = img_.find('img')["srcset"]
            urls = re.findall(r'https?://\S+', img_links)
            img_link = urls[0] if urls else ""

            site = product.find('a', class_ = 'style__ProductLink-sc-139nb47-2 cKoUly product-item')["href"]
            if "tiki.vn" not in site:
                site = "tiki.vn" + site
            flag = 0
            for word in part_name.split(" "):
                if(word not in title.lower().split()):
                    flag = 1
                    break
            if(flag == 0):
                part_list.append((title,price,link,img_link,site))
        except:
            print("error")
    driver.quit()

    return part_list

def lazada(soup, part_name, site):
    driver = webdriver.Chrome() 

    driver.get("https://www.lazada.vn/giay-sneaker-nam/?spm=a2o4n.searchlistcategory.cate_9_2.1.7003564fFAL7Rj")

    driver.implicitly_wait(10)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    products = soup.find_all('div', class_='qmXQo')
    part_list=[]
    for product in products:
        try:
            title = product.find('div', class_='RfADt').text
            price = product.find('span', class_='ooOxS').text
            link = ""

            img_link = product.find('img')["src"]

            site = product.find('div', class_ = '_95X4G').a["href"]

            flag = 0
            for word in part_name.split(" "):
                if(word not in title.lower().split()):
                    flag = 1
                    break
            if(flag == 0):
                part_list.append((title,price,link,img_link,site))
        except:
            print("error")
    driver.quit()

    return part_list