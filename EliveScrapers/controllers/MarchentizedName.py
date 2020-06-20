from flask import Flask
import csv
import requests
from bs4 import BeautifulSoup
import mysql.connector
from db import database
import os
import time
from random import seed
from random import randint


class Marchentizing:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        self.baseurl ="https://www.barcodelookup.com/"
#Scrap the url
    def AddisonScraper(self):
        count = 0
        response = ""
        seed(1)
        # response = requests.get(self.baseurl, headers = self.headers)
        try:
            with open('uploads/addison_products.csv', mode='r') as file:
               csv_reader = csv.DictReader(file)
               
               for rsCsvreader in csv_reader:
                    # print(self.baseurl+rsCsvreader["upc"])
                    response = requests.get(self.baseurl+rsCsvreader["upc"], headers = self.headers)                   
                    
                    data = BeautifulSoup(response.content, 'html.parser') 
                    ProdInfoCon = data.find('div',{'class':'mid-inner'})
                    print(response)
                    upc = ProdInfoCon.h1.text
                    name = ProdInfoCon.h4.text
                    imgCon = data.find('div',{'class':'col-md-6'})
                    img = imgCon.find('div',{'id':'images'})
                    imgUrl = img.img['src']
                    self.saveProductUpc(rsCsvreader["PID"],rsCsvreader["Name"],name,upc,imgUrl,57)
                    time.sleep(randint(1,5))
                    count+=1
        except:
            print(" There is an error occurs while inserting ")
        return str(count)
    
#   Insert in Database
    def saveProductUpc(self,pid,name,org_name,upc,img,supid):
        try:
            db = database()
            con = db.connection()
            # print(con)
            # exit()
            statement = "INSERT INTO marchetize_name (pid,name,org_name,upc,img,supid) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (pid, name,org_name,upc,img,supid)
            con[0].execute(statement, val)
            con[1].commit()
            print(con[0].rowcount, "record inserted.")
        except:
            print("Error in Saving Data")
       
