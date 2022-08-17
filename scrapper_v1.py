from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import sqlite3 as sl
import warnings
import pandas as pd
import time
from math import ceil
from datetime import datetime
warnings.filterwarnings("ignore")

websitesUrlWorking = ['www.pricerunner.se','www.prisjakt.nu',
                        'www.blocket.se','www.tradera.com']

print('Welcome')
print('Only these sites are covered: ')
index = 1
for website in websitesUrlWorking:
    print(f"{index}. {website}")
    index+=1
# Url need to be scrapped
print('Kindly input url need to be scrapped: ', end = '')
url = input().strip()
print('Wait, Scrapping.......')
https://www.pricerunner.se/cl/37/Grafikkort?attr_60534072=60534094%2C60534097%2C60534093%2C60534095%2C60534096%2C60534098%2C60534099%2C60534100
https://www.blocket.se/annonser/hela_sverige?q=Gtx%2B1080%2Bti
https://www.prisjakt.nu/c/grafikkort?6716=16584%7C25236%7C9062&b_in_stock=1
https://www.tradera.com/en/search?q=gtx%201080%20ti

#If want to save in db
db_ = True

#if want to append in existing table only works when save to db
#Change to True if want to append data in existing table
#change to False if want to overwrite existing table
append_ = False

#change to True if want duplicate products
#change to False if want to remove duplicate products
duplicated_ = True

## if want to save in excel
excel_ = True

con = sl.connect('database/scrapper.db')

if not re.search(r'^https?\:\/\/\w\w\w\.',url):
    if re.search(r'^\w\w\w\.',url):
        url = 'https://'+url
    else:
        url = 'https://www.'+url

websiteName = re.search(r'www\.[A-z]+\.[A-z]+',url)

if websiteName:
    websiteName = websiteName[0]

def pricerunner(url,websiteName):
    options = Options()
    # options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True
    options.add_argument("--window-size=1280x720")
    options.add_argument("start-maximised")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    ser = Service("selenium/chromedriver_98.exe")
    driver = webdriver.Chrome(options=options, service=ser)
    driver.get(url)
    time.sleep(3)
    try:
        driver.find_element_by_xpath('//*[@id="consent"]/div/div[2]/div[1]/div[2]/div/div/button[1]').click()
    except:
        pass
    page = 1
    print(f"Loading page {page}")
    while(True):
        try:
            time.sleep(1)
            button = driver.find_element_by_class_name('css-uf38ne')
            page += 1
            print(f"Loading page {page}")
            driver.execute_script("arguments[0].click();", button)
        except:
            print('Completing loading of all pages...')
            time.sleep(3)
            break
    html = driver.page_source
    final_data = []
    soup = bs(html, 'html.parser')
    all_data = soup.find(class_ = "css-ej99yf").find('div').findAll('a')
    product_count = 0
    for data in all_data:
        try:
            productLink = 'https://'+websiteName+data['href']
        except:
            continue
        driver.get(productLink)
        time.sleep(0.5)
        html = driver.page_source
        data_soup = bs(html,'html.parser')
        try:
            productName = data_soup.find(class_ = 'O7j3Z_aB6D').find('h1').text
        except:
            productName = ''
        try:
            productBrand = productName.split(' ',1)[0]
        except:
            productBrand = ''
        try:
            productPrice = data_soup.find(class_ = 'foWwRfeBAj css-1u8qly9').find(class_ = 'css-guoxna').find('span').text
        except:
            try:
                productPrice = data_soup.find(class_ = 'Ir1vyba4H8').find('span').text
            except:
                productPrice = ''
        
        try:
            productDescription = data_soup.find(class_ = 'YYbnpfKxRT').find('p').text
        except:
            productDescription = ''
        # try:
        #     productRating = data_soup.find(class_ = 'Go9sX8QOIe').find(class_ = 'css-1pctpc0').find('span').text
        # except:
        #     productRating = ''
        try:
            productStocksList = data_soup.findAll(class_ = 'foWwRfeBAj css-1u8qly9')
            for productStock in productStocksList:
                try:
                    merchantName = productStock['aria-label'].split(',',1)[0]
                    try:
                        merchantCountry = productStock.find(class_ = 'css-1ryb16f').find('div')['aria-label']
                    except:
                        merchantCountry = ''
                    try:
                        merchantStock = productStock.find(class_ = 'css-guoxna').find('div')['aria-label']
                    except:
                        merchantStock = ''
                    try:
                        merchantPrice = productStock.find(class_ = 'css-guoxna').find('span').text
                        merchantPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',merchantPrice)
                        if productPrice == '':
                            productPrice = merchantPrice
                    except:
                        merchantPrice = ''
                    
                except:
                    continue

                productPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',productPrice)
                productPrice = re.sub(r'\s',' ',productPrice)
                productDescription = re.sub(r'\s',' ',productDescription)
                # productRating = re.sub(r'\s',' ',productRating)
                productName = re.sub(r'\s',' ',productName)
                merchantName = re.sub(r'\s',' ',merchantName)
                merchantCountry = re.sub(r'\s',' ',merchantCountry)
                merchantPrice = re.sub(r'\s',' ',merchantPrice)
                merchantStock = re.sub(r'\s',' ',merchantStock)
                print("Product Name: ", productName)
                print("Description: ", productDescription)
                # print("Rating: ", productRating)
                print("Brand: ", productBrand)
                print("Lowest Price: ", productPrice)
                print("Merchant Name: ", merchantName)
                print("Merchant Country: ", merchantCountry)
                print("Merchant Price: ", merchantPrice)
                print("Stock Status: ", merchantStock)
                print("URL: ", productLink)
                print()
                final_data.append([productName,productDescription,productBrand,productPrice,merchantName,merchantCountry,merchantPrice,merchantStock,productLink])
        except:
            final_data.append([productName,productDescription,productBrand,productPrice,'','','','',productLink])
        product_count += 1

    print(f'Scrapping completed for {product_count} products')
    print()
    columns = ['Product Name', 'Description','Brand','Lowest Price','Merchant Name','Merchant Country','Price' ,'Stock Status', 'URL']
    df = pd.DataFrame(columns=columns,data = final_data)
    df['Time of Scrapping'] = datetime.now()
    return df

def blocket(url,websiteName):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True
    options.add_argument("--window-size=1280x720")
    options.add_argument("start-maximised")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    ser = Service("selenium/chromedriver_98.exe")
    driver = webdriver.Chrome(options=options, service=ser)
    url = re.sub(r'\&page\=[0-9]*','',url)
    url = re.sub(r'page\=[0-9]*\&','',url)
    driver.get(url)
    print('Scrapping for url: ')
    print(url)
    print('Starting from page 1 ')
    print('Scrapping page 1 ...')
    time.sleep(4)
    print()
    html = driver.page_source
    soup = bs(html, 'html.parser')
    final_data = []
    pages_url = []
    pages_url.append(url)
    pages = re.search(r'\d+',soup.find('div',{'data-cy':'search-result-count'}).text)
    if pages:
        pages = ceil(int(pages[0])/40)
        print('Total Pages: ', pages)
        for page in range(2,pages+1):
            if re.search(r'\?',url):
                pages_url.append(url+'&page='+str(page))
            else:
                pages_url.append(url+'?page='+str(page))
    page = 1
    product_count = 0
    for page_url in pages_url:
        if page_url != url:
            print(f'Scrapping Page {page} ...')
            driver.get(page_url)
            print(page_url)
            print()
            time.sleep(4)
            html = driver.page_source
            soup = bs(html, 'html.parser')
        page += 1
        all_data = soup.findAll(class_ = 'styled__Wrapper-sc-1kpvi4z-0 bOXZnc')
        for data in all_data:
            if data.text:
                try:
                    productName = data.find(class_ = 'styled__SubjectWrapper-sc-1kpvi4z-15 kNHTOY').find('h2').text
                except:
                    continue
                try:
                    productPrice = data.find(class_ = 'Price__StyledPrice-sc-1v2maoc-1 jvXHae').text
                except:
                    productPrice = ''
                try:
                    productLocation = data.find(class_ = 'styled__TopInfoWrapper-sc-1kpvi4z-25 fMFkuP').text
                except:
                    productLocation = ''
                try:
                    productTime = data.find(class_ = 'styled__Time-sc-1kpvi4z-21 feESoa').text
                except:
                    productTime = ''
                try:
                    productLink = 'https://'+websiteName+data.find(class_ = 'styled__SubjectWrapper-sc-1kpvi4z-15 kNHTOY').find('a')['href']
                except:
                    productLink = 'https://'+websiteName

                productPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',productPrice)
                productPrice = re.sub(r'\s',' ',productPrice)
                productTime = re.sub(r'\s',' ',productTime)
                productLocation = re.sub(r'\s',' ',productLocation)
                productName = re.sub(r'\s',' ',productName)

                print("Product Name: ", productName)
                print("Price: ", productPrice)
                print("Time: ", productTime)
                print("Location: ", productLocation)
                print("URL: ", productLink)
                print()
                final_data.append([productName,productPrice,productTime,productLocation,productLink])
                product_count += 1

    print(f'Scrapping completed for {product_count} products')
    print()
    columns = ['Product Name', 'Price','Time','Location','URL' ]
    df = pd.DataFrame(columns=columns,data = final_data)
    df['Time of Scrapping'] = datetime.now()
    return df

def prisjakt(url,websiteName):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True
    options.add_argument("--window-size=1280x720")
    options.add_argument("start-maximised")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    ser = Service("selenium/chromedriver_98.exe")
    driver = webdriver.Chrome(options=options, service=ser)
    url = re.sub(r'\&offset\=[0-9]*','',url)
    url = re.sub(r'offset\=[0-9]*\&','',url)
    driver.get(url)
    print('Scrapping for url: ')
    print(url)
    print('Starting from page 1 ')
    print('Scrapping page 1 ...')
    time.sleep(3)
    print()
    html = driver.page_source
    soup = bs(html, 'html.parser')
    pages_urls = []
    pages_urls.append(url)
    try:
        all_data = soup.find('ul', {"data-test" : "ProductGrid"}).findAll('li',{"data-test" : "ProductRow"})
        offset = 44
    except:
        all_data = soup.find('ul',{'data-test':'ProductLayoutList'}).findAll('li',{'data-test' : 'ProductCompactListCard'})
        offset = 48
    pages = re.search(r'\d+\s?\d*',soup.find('div',{'data-test':'ProductsHeaderTitleWrapper'}).text)
    if pages:
        pages = re.sub('\s', '',pages[0])
        pages = ceil(int(pages)/offset)
        for page in range(1,pages):
            if re.search(r'\?',url):
                pages_urls.append(url+'&offset='+str(page*offset))
            else:
                pages_urls.append(url+'?offset='+str(page*offset))
    final_data = []
    page = 1
    product_count = 0
    for page_url in pages_urls:
        if page_url != url:
            driver.get(page_url)
            print(f'Scrapping page {page} ...')
            print(page_url)
            print()
            time.sleep(3)
            html = driver.page_source
            soup = bs(html, 'html.parser')
            try:
                all_data = soup.find('ul', {"data-test" : "ProductGrid"}).findAll('li',{"data-test" : "ProductRow"})
            except:
                all_data = soup.find('ul',{'data-test':'ProductLayoutList'}).findAll('li',{'data-test' : 'ProductCompactListCard'})
        page += 1
        for data in all_data:
            try:
                productLink = 'https://'+websiteName+data.find('a',{'data-test':'InternalLink'})['href']
            except:
                continue
            driver.get(productLink)
            time.sleep(0.5)
            html = driver.page_source
            data_soup = bs(html,'html.parser')
            data_soup = data_soup.find('section',{"data-test":"AppMain"})
            try:
                productName = data_soup.find('div',{'data-test':'ProductTitle'}).text
            except:
                continue
            
            try:
                productDescription = '\n'.join([re.sub(r'\s',' ',li.text) for li in \
                            data_soup.findAll('div',{'data-test':'ProductTitle'})[-1].findNext('div').find('ul').findAll('li')])
            except:
                try:
                    productDescription = '\n'.join([re.sub(r'\s',' ',li.text) for li in \
                            data_soup.find('div',{'data-test':'ProductTitle'}).findNext('div').find('ul').findAll('li')])
                except:
                    productDescription = ''
            productPrice = ''
            productName = re.sub(r'\s',' ',productName)
            try:
                productStocksList = data_soup.findAll('div',{'data-test':'PriceRow'})
                merchants = 0
                for productstock in productStocksList:
                    try:
                        merchantName = productstock.find('picture'
                        )['alt']
                        merchants += 1
                    except:
                        continue
                    try:
                        merchantMore = productstock.findAll('span',{"data-test":"PriceLabel"})
                        if len(merchantMore)>1:
                            merchantShipping = merchantMore[0].text
                            merchantPrice = merchantMore[-1].text
                        else:
                            merchantShipping = ''
                            merchantPrice = merchantMore[-1].text
                        if not productPrice:
                            productPrice = merchantPrice
                            productPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',productPrice)
                            productPrice = re.sub(r'\s',' ',productPrice)
                    except:
                        merchantShipping = ''
                        merchantPrice = ''
                    try:
                        merchantStock = productstock.findAll('div',class_ = 'Row-sc-6fgy6m-3')[-1].findAll('span')[-1].text
                    except:
                        merchantStock = 'No stock'

                    merchantName = re.sub(r'\s',' ',merchantName)
                    merchantPrice = re.sub(r'\s',' ',merchantPrice)
                    merchantPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',merchantPrice)
                    merchantStock = re.sub(r'\s',' ',merchantStock)
                    print("Product Name: ", productName)
                    print("Description: ", productDescription)
                    print("Price: ", productPrice)
                    print("Merchant Name: ", merchantName)
                    print("Merchant Price: ", merchantPrice)
                    print("Merchant Shipping: ", merchantShipping)
                    print("Merchant Stock: ", merchantStock)
                    print("URL: ", productLink)
                    print()
                    final_data.append([productName,productDescription,productPrice,merchantName,merchantPrice,merchantShipping,merchantStock,productLink])

                if not merchants:
                    if not productPrice:
                        try:
                            productPrice = data_soup.find('div',{'data-test':'PriceRow'}).findAll('span',{"data-test":"PriceLabel"})[-1].text
                            productPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',productPrice)
                            productPrice = re.sub(r'\s',' ',productPrice)
                        except:
                            productPrice = ''
                    print("Product Name: ", productName)
                    print("Description: ", productDescription)
                    print("Price: ", productPrice)
                    print("No merchant available")
                    print("URL: ", productLink)
                    print()
                    final_data.append([productName,productDescription,productPrice,'','','','',productLink])
            except:
                final_data.append([productName,productDescription,productPrice,'','','','',productLink])
            product_count += 1

    print(f'Scrapping completed for {product_count} products')
    print()
    columns = ['Product Name','Description','Lowest Price', 'Merchant Name','Price','Shipping', 'Stock Status', 'URL']
    df = pd.DataFrame(columns=columns,data = final_data)
    df['Time of Scrapping'] = datetime.now()
    return df

def tradera(url,websiteName):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True
    options.add_argument("--window-size=1280x720")
    options.add_argument("start-maximised")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    ser = Service("selenium/chromedriver_98.exe")
    driver = webdriver.Chrome(options=options, service=ser)
    final_data = []
    url = re.sub(r'\&paging\=.*','',url)
    url = re.sub(r'\&spage\=.*','',url)
    driver.get(url)
    print(url)
    print('Starting from page 1 ')
    print('Scrapping page 1 ...')
    time.sleep(3)
    print()
    html = driver.page_source
    soup = bs(html, 'html.parser')
    page = 1
    product_count = 0
    while(True):
        all_data = soup.find('main',class_='main--1_vGx').find('section',class_ = 'row mb-4').findAll('div', class_ = 'item-card-container')
        for data in all_data:
            if data.text:
                data = data.find('div',class_ = 'item-card-inner-wrapper')
                try:
                    productLink = 'https://'+websiteName+data.find('a')['href']
                except:
                    continue
                driver.get(productLink)
                time.sleep(0.5)
                html = driver.page_source
                data_soup = bs(html,'html.parser')
                try:
                    productName = data.find('p').text
                except:
                    try:
                        productName = data_soup.find('h1',{'id':'view-item-main'}).text
                    except:
                        continue
                try:
                    productPrice = data.find(class_ = 'item-card-details').find(class_ = 'd-inline-block text-nowrap font-weight-bold item-card-details-price').text
                except:
                    try:
                        productPrice = data_soup.find('p',class_ = 'text-nowrap heading-madrid mb-0 bid-details-amount').text
                    except:
                        productPrice = ''
                try:
                    productTime = data_soup.find(class_ = 'd-flex flex-column text-center').find('dd').text
                except:
                    productTime = ''
                try:
                    productEndTime = re.sub(r'\s',' ', data_soup.find('p', class_ = 'text-nowrap mb-0 bid-details-time-title').text)
                    productEndTime = productEndTime.split(" ",1)[-1]
                except:
                    productEndTime = ''
                try:
                    productleastBidPrice = re.search('\d+\s*\d*\s*\d*',data_soup.find('section',class_ = 'pt-2 pt-md-0').find('p').text)[0]
                except:
                    productleastBidPrice = 'No need to bid, Buy: '+ productPrice
                try:
                    productDescription = data_soup.findAll(class_ = 'position-relative description mb-md-4')[-1].text
                except:
                    productDescription = ''
                try:
                    productShipping = data_soup.find('div',class_ = 'shipping-options--3i-hm').findAll('p')
                    productShipping = '\n'.join([re.sub(r'\s',' ',ptag.text) for ptag in productShipping])
                except:
                    productShipping = ''
                try:
                    productViews = data_soup.find('dd').text
                except:
                    productViews = '0'
                try:
                    productBids = re.search('\d+\s*\d*\s*\d*',data.find(class_ = 'item-card-details').find(class_ = 'd-inline-block text-nowrap mr-2').text)[0]
                except:
                    productBids = '0'
                productPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',productPrice)
                productleastBidPrice = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',productleastBidPrice)
                productBids = re.sub(r'(?<=[0-9])\s(?=[0-9])',',',productBids)
                productPrice = re.sub(r'\s',' ',productPrice)
                productName = re.sub(r'\s',' ',productName)
                productTime = re.sub(r'\s',' ',productTime)
                productShipping = re.sub(r'\s',' ',productShipping)
                productBids = re.sub(r'\s',' ',productBids)

                print("Product Name: ", productName)
                print("Description: ", productDescription)
                print("Leading Bid: ", productPrice)
                print("Minimum Bid: ", productleastBidPrice)
                print("Published: ", productTime)
                print("End Time: ", productEndTime)
                print("Bids: ", productBids)
                print("Shipping: ", productShipping)
                print("Views: ", productViews)
                print("URL: ", productLink)
                print()
                final_data.append([productName,productDescription,productPrice,productleastBidPrice,productTime,
                productEndTime,productBids,productShipping,productViews,productLink])
                product_count += 1

        try:
            next_page = soup.find('a',{'rel':'next'})['href']
            if not next_page.strip():
                break
            next_page = 'https://'+websiteName+next_page
            driver.get(next_page)
            page += 1
            print(f'Scrapping page {page} ...')
            print(next_page)
            print()
            time.sleep(3)
            html = driver.page_source
            soup = bs(html, 'html.parser')
        except:
            break
    print(f'Scrapping completed for {product_count} products')
    print()
    columns = ['Product Name', 'Description', 'Leading Bid','Minimum Bid', 'Published',
     'End Time','Bids', 'Shipping', 'Views','URL']
    df = pd.DataFrame(columns=columns,data = final_data)
    df['Time of Scrapping'] = datetime.now()
    return df

if websiteName in (websitesUrlWorking):
    websitefunction = re.search(r'(?<=www\.)[A-z]+(?=\.)',websiteName)[0].lower()
    try:
        df = eval(websitefunction)(url,websiteName)
        try:
            if excel_:
                df.to_excel('excel/'+websitefunction+'.xlsx',index=False)
        except Exception as e:
            print('Saving to excel didnt work and thrown exception as follows:')
            print(e)
        try:
            if db_:
                if append_:
                    if duplicated_:
                        df.to_sql(websitefunction,con=con,if_exists='append',index=False)
                    else:
                        query = f"select * from {websitefunction}"
                        try:
                            df_temp = pd.read_sql(query,con)
                            if not df_temp.empty:
                                df_temp['Time of Scrapping'] = pd.to_datetime(df_temp['Time of Scrapping'])
                                df = pd.concat([df_temp,df])
                                df = df.drop_duplicates(keep='last',subset=['URL']).reset_index(drop=True)
                                df.to_sql(websitefunction,con=con,if_exists='replace',index=False)
                            else:
                                df.to_sql(websitefunction,con=con,if_exists='replace',index=False)
                        except Exception as e:
                            print(e)
                            df.to_sql(websitefunction,con=con,if_exists='replace',index=False)
                else:
                    df.to_sql(websitefunction,con=con,if_exists='replace',index=False)
        except Exception as e:
            print('Saving to database didnt work and thrown exception as follows:')
            print(e)
    except Exception as e:
        print(e)
        print('Website url could not be scrapped')
        

else:
    if websiteName:
        print('Website is not yet covered for scrapper')
    else:
        print('Provided Link is not correct.')
    print('Only these sites are covered: ')
    index = 1
    for website in websitesUrlWorking:
        print(f"{index}. {website}")
        index+=1