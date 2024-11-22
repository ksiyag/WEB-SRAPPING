from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class WebScraper:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=self.options)

    def _amazon_scraper(self,response):
        products = []
        soup = BeautifulSoup(response,'html.parser')
        for bf in soup.findAll('div',attrs={'class':'puisg-row'}):
            name = bf.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text if bf.find('span',{'class':'a-size-medium a-color-base a-text-normal'}) else None
            image = bf.find('img',{'class':'s-image'})['src'] if bf.find('img',{'class':'s-image'}) else None
            price = bf.find('span',{'class':'a-offscreen'}).text if bf.find('span',{'class':'a-offscreen'}) else None
            stars = bf.find('span',{'class':'a-icon-alt'}).text if bf.find('span',{'class':'a-icon-alt'}) else None
            rating = bf.find('span',{'class':'a-size-base s-underline-text'}).text if bf.find('span',{'class':'a-size-base s-underline-text'}) else None
            merchant = 'Amazon'
            if  name != None and image != None and price != None and stars != None and rating != None:
                product = {'name':name,'image':image,'price':price,'stars':stars,'rating':rating,'merchant':merchant}
                products.append(product)
        return products


    def _flipkart_scraper(self,response):
        products = []
        soup = BeautifulSoup(response,'html.parser')
        print(response)
        for bf in soup.findAll('div',attrs={'class':'cPHDOP col-12-12'}):
            image = bf.find('img',attrs={'class':'DByuf4'})['src'] if bf.find('img',attrs={'class':'DByuf4'}) else None
            name =  bf.find('div',attrs={'class':'KzDlHZ'}).text.strip() if bf.find('div',attrs={'class':'KzDlHZ'}) else None
            stars = bf.find('div',attrs={'class':'XQDdHH'}).text.strip() if bf.find('div',attrs={'class':'XQDdHH'}) else None
            rating = bf.find('span',attrs={'class':'Wphh3N'}).text.strip() if bf.find('span',attrs={'class':'Wphh3N'}) else None
            price = bf.find('div',attrs={'class':'Nx9bqj _4b5DiR'}).text.strip() if bf.find('div',attrs={'class':'Nx9bqj _4b5DiR'}) else None
            merchant = 'Flipkart'
            
                   
            if image != None and name != None and rating != None and stars!=None:
                 products.append({'image':image,'name':name,'rating':rating,'rating_starts':stars,'price':price,'merchant':merchant})
        return products

    def scrape(self,product_name:str,merchant:str):
        if merchant == 'amazon':
            self.driver.get(f"https://www.amazon.in/s?k={product_name}")
            response = self.driver.page_source if self.driver.page_source is not None else  None
            result = self._amazon_scraper(response) if response is not None else None
            return result
            
        elif merchant =='flipkart':
            self.driver.get(f"https://www.flipkart.com/search?q={product_name}")
            response = self.driver.page_source if self.driver.page_source is not None else None
            result = self._flipkart_scraper(response) if response is not None else None
            return result
        self.driver.quit()






