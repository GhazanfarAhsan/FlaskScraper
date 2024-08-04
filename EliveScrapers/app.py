import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from controllers.MarchentizedName import Marchentizing
from controllers.ScraperController import ScraperController
from controllers.prediict import Prediction
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
def fiverr_store():
    if request.method == 'POST':
        scraper = ScraperController();
        message = scraper.scraper(request.form)
        return message 
# FOOTBALL PREDICTOR
@app.route("/football/predict",methods=["GET"])
def predictorView():
    return render_template('prediction_view.html')

@app.route("/football/predict/store",methods=["POST"])
def predict():
    predObj = Prediction()
    print(request.json)
    result = predObj.prediction(request.json['homeTeam'],request.json['awayTeam'],request.json['venue'])
    return result 
