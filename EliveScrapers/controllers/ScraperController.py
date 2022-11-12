
from pickle import TRUE
from flask import Flask
import requests
from bs4 import BeautifulSoup
from db import database

from controllers.BaseController import BaseController;
from controllers.AmazonController import AmazonController;

class ScraperController(BaseController):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        self.cookies = {};
    
    def scraper(self,data):
            if(data['market'] =="amazon"):
                amazon = AmazonController();
                return amazon.scrapAmazonBestSellerProducts(data);
            

    
    
    

    