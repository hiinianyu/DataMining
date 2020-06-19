from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
from math import ceil
from sklearn.linear_model import LinearRegression

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getRegressionFunction(dataFrame):
    Df = dataFrame
    
    Df["Date"] = pd.to_datetime(Df["Date"]).dt.strftime('%Y-%m-%d')
    Df['Price']=Df['Price'].astype(str).str.replace(',', '').astype(float)
    Df['S_1'] = Df["Price"].shift(1).rolling(window=2, center = True).mean()
    Df['S_2'] = Df["Price"].shift(1).rolling(window=5, center = True).mean()
    Df = Df.dropna()
    X = Df[['S_1','S_2']]
    y = Df["Price"]
    
    t = 0.9
    count = int(ceil(X.shape[0]*t))
    X = X.iloc[::-1]
    y = y.iloc[::-1]
    X_train = X[:count]
    X_test = X[count:]
    y_train = y[:count]
    y_test = y[count:]
    # Performing linear regression
    linear = LinearRegression().fit(X_train, y_train)
    result = Coefficient(round(linear.coef_[0], 2), round(linear.coef_[1], 2), round(linear.intercept_, 2))
    # Predict prices
    predicted_price = linear.predict(X_test)
    predicted_price = pd.DataFrame(predicted_price, index=y_test.index, columns=['price'])
    return result

class Coefficient:
    def __init__(self, M1, M2, C):
        self.M1 = M1
        self.M2 = M2
        self.C = C

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