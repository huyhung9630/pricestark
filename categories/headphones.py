from bs4 import BeautifulSoup
import requests

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"}

parts_sites ={ "+":[("www.flipkart.com" , "https://www.flipkart.com/search?q=item"),
                    ("www.snapdeal.com" , "https://www.snapdeal.com/search?keyword=item"),
                    ("www.amazon.in", "https://www.amazon.in/s?k=item")
                ]
}


'''elif(site == "www.ebay.com"):
    site_function = ebay'''


def scrape_site(site, part_name, soup):

    if(site == "www.amazon.in"):
        site_function = amazon
    elif(site == "www.flipkart.com"):
        site_function = flipkart
    elif(site == "www.snapdeal.com"):
        site_function = snapdeal

    part_list = site_function(soup, part_name, site)
    return part_list

def amazon(soup , part_name , site):
    part_list = []
    print("amazon")
    results = soup.findAll("div", {"class": "a-section a-spacing-medium"})
    for result in results:
        try:
            title = result.find("span" , {"class":"a-size-medium a-color-base a-text-normal"}).get_text().strip()

            price = result.find("span", {"class": "a-offscreen"}).get_text().strip().replace("Rs.", "₹")

            link = "https://amazon.in" + \
                result.find("a", {"class": "a-link-normal a-text-normal"})['href'].strip()

            img = result.find("div", {"class": "a-section aok-relative s-image-fixed-height"}).img["src"]

            flag = 0
            for word in part_name.split(" "):

                if(word not in title.lower().split()):
                    flag = 1
                    break
            if(flag == 0):
                    part_list.append((title,price,link,img,site))
        except:
            continue
    return part_list

def flipkart(soup , part_name , site):
    part_list = []
    results = soup.find_all("div" , {"class":"slAVV4"})
    print("flipkart") 
    for result in results:
        try:
            title = result.find("a" , {"class":"wjcEIp"}).text

            price = result.find("div" , {"class":"Nx9bqj"}).text

            link_ = result.find("a" , {"class":"Zhf2z-"})
            link = link_["href"]

            img_ = result.find("a" , {"class":"Zhf2z-"})
            img = img_["href"]

            link_ = result.find("a" , {"class":"_2cLu-l"})
            link = link_["href"]
            print(title, price)
            flag = 0

            # for word in part_name.split(" "):
            #     if(word not in title.lower().split()):
            #         flag = 1
            #         break
            if(flag == 0):
                    part_list.append((title,price,link,img,site))
        except:
            continue
    return part_list

def snapdeal(soup , part_name , site):
    part_list = []
    print("snapdeal")
    results = soup.find_all("div" , {"class":"product-tuple-description"})

    for item in results:
        try:
            result = item.find("div" , {"class":"product-desc-rating"})

            title = result.a.p.get_text().strip()

            price = result.find("span" , {"class":"lfloat product-price"}).get_text().strip().replace("Rs.","₹")

            img_ = item.find("img" , {"class":"product-image"})
            img = img_["src"]

            link = result.a["href"]

            flag = 0

            for word in part_name.split(" "):
                if(word not in title.lower().split()):
                    flag = 1
                    break
            if(flag == 0):
                    part_list.append((title,price,link.img,site))
        except:
            continue

    return part_list



