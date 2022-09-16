
from pickle import TRUE
from flask import Flask
import requests
from bs4 import BeautifulSoup
from db import database
import os
import time
from random import seed
from random import randint
from controllers.BaseController import BaseController;

class ScraperController(BaseController):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        self.baseurl ='https://www.amazon.com'
    # scraping fiverr
    def scraper(self,data):
            if(data['market'] =="amazon"):
                return self.scrapAmazonBestSellerProducts(data)
    
    def scrapAmazonBestSellerProducts(self,data):
        count = 0
        response = "";
        message = ""
        page = 1;
        product_request = None;
        db_count = 0;
        seed(1)

        
        # response = requests.get(self.baseurl, headers = self.headers)
        try:
            for page in range(1,6):
                url = data['url'].replace('1',str(page));
                print(url)
                session = requests.Session();
                response = session.get(url, headers = self.headers,cookies=[]);
                    
                data = BeautifulSoup(response.content, 'html.parser');
                all_products_arr = data.find_all('a',class_='a-link-normal', href=True);
                
                count =len(all_products_arr);
                print(count);
                if(count > 0):
                    for link in all_products_arr:
                        print('GO TO PAGE----: '+self.baseurl + str(link['href']));
                        session_pro = requests.Session();
                        product_request = session_pro.get(self.baseurl + link['href'],headers = self.headers);
                        print(product_request.status_code);
                        
                        if(product_request.status_code != 200 or page > 5):
                            print('Service Not available--------')
                            message = "Service not available --------";
                            break;
                        else:
                            product_data = BeautifulSoup(product_request.content, 'html.parser');
                            caphtcha = product_data.find('p',{'class':'a-last'})
                            
                            if(caphtcha):
                                print("Captcha occurs your ip is temporarily block try again later");
                                print(product_data)
                                message = "Captcha occurs your ip is temporarily block try again later";
                                break;
                            else:
                                
                                name = product_data.find('span',{'id':'productTitle'}).text;
                                print(name);
                                
                                rating = product_data.find('span',{'id':'acrCustomerReviewText'}).text;
                                rating = rating.split(' ')[0];
                                print(rating);
                                tabular_buybox = product_data.find_all('div',{'class':'tabular-buybox-text'});
                                print(tabular_buybox);
                                

                                if(len(tabular_buybox) == 0):
                                    print('Product is out of stock ------');
                                    
                                else:
                                    price = product_data.find('span',{'class':'a-price-whole'}).text+product_data.find('span',{'class':'a-price-fraction'}).text;
                                    print(price);
                                    shipfrom = tabular_buybox[0].find('span',{'class':'a-size-small'}).text;
                                    seller = tabular_buybox[1].find('span',{'class':'a-size-small'}).text;
                                    print(seller,shipfrom);
                                    description = product_data.find('div',{'id':'productDescription-3_feature_div'});
                                    print(description);
                                    if(description):
                                        description = description.find('p').text;
                                    else:
                                        description = "";

                                    prodDes = product_data.find('div',{'id':'productDetails_detailBullets_sections1'});
                                    trs = prodDes.find_all('tr');
                                    bsr = trs[0].find('td').find_all('span')[1].text;
                                    db_count+=self.saveAmazonProducts((name,price,rating,shipfrom,seller,bsr,description))
                                
                                    time.sleep(randint(10,100))  
                else:
                    message = "Page not found"; 
                page+=1;
                    
                        
                    
                
        except Exception as e:
            print(e);
        if(message == ""):
            message = str(count)+' Products has been scraped successfully.'+ str(db_count) + ' Products successfully saved in database';
            
            return self.sendResponse(message,{
                'products_found':count,
                'products_saved':db_count,
                'missing':count-db_count,
            })
        else:
            return self.sendError(message);

    def saveAmazonProducts(self,values):
        # values = (name,price,rating,shipfrom,seller,bsr,description);
        columns = ('name','price','rating','shipfrom','seller','bsr','manufacturer');
        db = database();
        count = db.insert("amazon_products",columns,values);
        return count;
    

    