import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from controllers.MarchentizedName import Marchentizing

# UPLOAD_FOLDER ='\uplaods'

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = ''
@app.route("/")
def uploadUpcFile():
    return render_template("upc_file_upload.html")

@app.route("/marchentize_name",methods=["GET","POST"])
def supplierMerchantizedName():
      if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path,'uploads',filename))
            marchentize = Marchentizing()
            TotRecord = marchentize.AddisonScraper()
            return TotRecord

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS