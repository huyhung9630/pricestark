from bs4 import BeautifulSoup
from selenium import webdriver
import re

parts_sites={
             '+':[('www.tiki.vn','https://tiki.vn/dien-thoai-smartphone/c1795'),
                  ('www.thegioididong.com', 'https://www.thegioididong.com/dtdd'),
                  ('www.lazada.vn', 'https://www.lazada.vn/dien-thoai-di-dong//?from=hp_categories&q=Mobiles')
                  ]
             }
def scrape_site(site, part_name, soup):
    if (site == "www.tiki.vn"):
        site_function = tiki
    elif(site == 'www.lazada.vn'):
        site_function = lazada
    elif (site == "www.thegioididong.com"):
        site_function = thegioididong
    part_list = site_function(soup, part_name, site)

    return part_list

def tiki(soup, part_name, site):
    driver = webdriver.Chrome() 

    driver.get("https://tiki.vn/dien-thoai-smartphone/c1795")

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

            link = product.find('a', class_ = 'style__ProductLink-sc-139nb47-2 cKoUly product-item')["href"]
            if "tiki.vn" not in link:
                link = "tiki.vn" + link
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

def thegioididong(soup, part_name,site):
    driver = webdriver.Chrome()

    driver.get("https://www.thegioididong.com/dtdd#c=42&o=17&pi=1")

    driver.implicitly_wait(10)

    part_list = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    products = soup.find_all('li', class_='item ajaxed __cate_42')

    for product in products:
        try:
            name = product.find('h3').text
            price = product.find('strong', class_='price').text
            link = "https://www.thegioididong.com" + product.a['href']
            img_link = product.find('div', class_='item-img item-img_42').img['src']
            flag = 0
            for word in part_name.lower().split():
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
    driver.get("https://www.lazada.vn/dien-thoai-di-dong//?from=hp_categories&page=&q=Mobiles")
    driver.implicitly_wait(10)

    part_list = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    products = soup.find_all('div', class_='qmXQo')
    
    for product in products:
        try:
            name = product.find('div',class_='RfADt').text
            price = product.find('span', class_='ooOxS').text
            link = product.find('div',class_='_95X4G').a['href']
            img_link = product.find('img')['src']
            flag = 0
            for word in part_name.lower().split():
                if (word not in name.lower().split()):
                    flag = 1
                    break
            if (flag == 0):
                part_list.append((name,price,link,img_link,site))
        except:
            continue
    driver.quit()
    return part_list

