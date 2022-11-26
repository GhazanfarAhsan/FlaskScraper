
from pickle import TRUE
from flask import Flask
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from controllers.BaseController import BaseController;
from controllers.AmazonController import AmazonController;

class ScraperController(BaseController):

    
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        self.cookies = {};
        self.baseUrl = "";
        self.requestType = "selenium";   
    def setBaseUrl(self,baseUrl):
        self.baseUrl = baseUrl;
    
    def getBaseUrl(self): 
        return self.baseUrl;

    def redirect(self,data):
            if(data['market'] =="amazon"):
                amazon = AmazonController();
                return amazon.scrapAmazonBestSellerProducts(data);
            
    def setupDriver(self):
        # Set your driver here
        print("Setting up the driver")
        driverPath = os.path.abspath('chromedriver.exe') 
        return driverPath

    def makeRequest(self,url):
        if  self.requestType == "selenium":
            driver = webdriver.Chrome(self.setupDriver())
            response = driver.get(self.baseUrl+url)

        elif self.requestType == "requests":
            response = requests.get(self.baseUrl+url);
        else:
            response = "You have to decide response type"

        return response
            
    

    