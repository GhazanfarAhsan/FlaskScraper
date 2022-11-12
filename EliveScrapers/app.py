import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from controllers.MarchentizedName import Marchentizing
from controllers.ScraperController import ScraperController
# UPLOAD_FOLDER ='\uplaods'

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = ''
@app.route("/")
def uploadUpcFile():
    return render_template("upc_file_upload.html")


@app.route("/scraper/<market>",methods=["GET","POST"])
def scraper(market):
    return render_template('scraper.html',market=market);

@app.route("/scraper/store",methods=["POST"])
def scraper_store():
    if request.method == 'POST':
        scraper = ScraperController();
        message = scraper.redirect(request.form)
        return message 
