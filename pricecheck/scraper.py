from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform

# silent browser
# options = webdriver.FirefoxOptions()
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
# check os if windows or linux

if platform.system() == "Windows":
    driver_path = "webdriver/windows/chromedriver.exe"
if platform.system() == "Linux":
    driver_path = "webdriver/linux/chromedriver"

# browser = webdriver.Firefox(options=options, executable_path=driver_path)
browser = webdriver.Chrome(options=options, executable_path=driver_path)

def get_data(query, page='ebay'):
    page=page.lower()
    if page == 'ebay':
        return get_ebay_data(query)
    
    elif page == 'cashconverter':
        return get_cashconverter_data(query)

def get_ebay_data(query):
    query = query.replace(' ', '+')
    url  = f"https://www.ebay.com.au/sch/i.html?_from=R40&_nkw={query}&_sacat=0&LH_Auction=1&_sop=1"

    # Get the HTML from the URL
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_="s-item__wrapper clearfix")

    list_items = []
    for item in items:
        #image
        image = item.find('div', class_="s-item__image-wrapper image-treatment")
        if image:
            image = image.find('img')['src']
        else:
            continue

        title = item.find('div', class_="s-item__title")
        if title:
            title = title.text
        else:
            continue

        itemlink = item.find('a', class_="s-item__link")
        if itemlink:
            itemlink = itemlink['href']
        else:
            continue

        condition = item.find('span', class_="SECONDARY_INFO")
        if condition:
            condition = condition.text
        else:
            continue

        price = item.find('span', class_="s-item__price")
        if price:
            price = price.text
        else:
            continue

        timeleft = item.find('span', class_="s-item__time-left")
        if timeleft:
            timeleft = timeleft.text
        else:
            continue

        shippingcost = item.find('span', class_="s-item__logisticsCost")
        if shippingcost:
            shippingcost = shippingcost.text
        else:
            continue

        # print(title, condition, price, timeleft, shippingcost)
        if condition == "Parts only":
            continue
        dict_item = {'image':image, 'title': title, 'itemlink': itemlink,  'price': price, 'timeleft': timeleft, 'shippingcost': shippingcost}
        list_items.append(dict_item)
    
    return list_items

def get_cashconverter_data(query):
    url  = f"https://www.cashconverters.com.au/search-results?query={query}&page=10"

    # r = requests.get(url)
    browser.get(url)
    # wait until the class product-item__body is loaded
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))
    browser.implicitly_wait(5)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    main_html = browser.page_source
    soup = BeautifulSoup(main_html, 'html.parser')
    items = soup.find_all('div', class_="product-item")

    list_items = []
    for i, item in enumerate(items):
        # image
        image = item.find('div', class_="product-item__image")
        if image:
            image_div = image.find('img')
            if image_div:
                image_src = "https://www.cashconverters.com.au/" + image.find('img')['src']
            else:
                image_src = ""
        else:
            continue

        title = item.find('span', class_="product-item__title__description")
        if title:
            title = title.text
        else:
            continue

        itemlink = item.find('a', class_="product-item__title")
        if itemlink:
            itemlink = "https://www.cashconverters.com.au/" + itemlink['href']
        else:
            continue

        price = item.find('div', class_="product-item__price")
        if price:
            price = price.text
        else:
            continue

        shippingcost = item.find('div', class_="product-item__postage")
        if shippingcost:
            shippingcost = shippingcost.text
        else:
            continue

        dict_item = {'image':image_src, 'title': title, 'itemlink': itemlink, 'price': price, 'shippingcost': shippingcost}
        list_items.append(dict_item)

    return list_items
