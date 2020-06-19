from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
from Milestone5 import getRegressionFunction

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("home.html")
    elif request.method == 'POST':
        if 'file' not in request.files:
            print('failed, no file in request')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            print('failed, no file name')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print('file read')
            dataFrame = pd.read_csv(file)
            newFunction = getRegressionFunction(dataFrame)
            return render_template("input.html", data = newFunction)

@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        
        result = float(request.form.get('M1')) * float(request.form.get('X1')) + float(request.form.get('M2')) * float(request.form.get('X2')) + float(request.form.get('C'))
        
        return render_template("result.html", X1=request.form.get('X1'), X2=request.form.get('X2'), M1=request.form.get('M1') , M2=request.form.get('M2'), C=request.form.get('C'), result = result)
    
class DependentVariable:
    def __init__(self, X1, X2):
        self.X1 = X1
        self.X2 = X2


if __name__ == "__main__":
    app.run()