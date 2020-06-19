import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from math import ceil

def getRegressionFunction(dataFrame):
  Df = dataFrame
    
  Df["Date"] = pd.to_datetime(Df["Date"]).dt.strftime('%Y-%m-%d')
  Df['Price']=Df['Price'].astype(str).str.replace(',', '').astype(float)
  
  # create two new columns with lagged terms with different moving window size 
  Df['S_1'] = Df["Price"].shift(1).rolling(window=2, center = True).mean()
  Df['S_2'] = Df["Price"].shift(1).rolling(window=5, center = True).mean()
  Df = Df.dropna()
  X = Df[['S_1','S_2']]

  # dependent variable
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
