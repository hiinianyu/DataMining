import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime
import subprocess
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import ceil
from math import sqrt

Df = pd.read_csv('goldprice_08-May-2020 19-11-07.csv')
print(Df.head())

print(Df.isnull().any())

# Change the format of "Date"
Df["Date"] = pd.to_datetime(Df["Date"]).dt.strftime('%Y-%m-%d')

# Remove the "," in the "Price", "Open', 'Low', and 'High' column and change the "string" type to "float"
Df['Price']=Df['Price'].astype(str).str.replace(',', '').astype(float)
Df['Open']=Df['High'].astype(str).str.replace(',', '').astype(float)
Df['Low']=Df['Low'].astype(str).str.replace(',', '').astype(float)
Df['High']=Df['High'].astype(str).str.replace(',', '').astype(float)
Df['Volume']=Df['Volume'].replace({'K': '*1e3', '-': '1'}, regex=True).map(pd.eval)
Df['Change %']=Df['Change %'].replace({'%': '*1e-2'}, regex=True).map(pd.eval)
Df['Volume'] = Df['Volume'].replace(1.0,np.NaN)
print(Df.head())

# Change "Date" as index and sort the data
Df['Date'] =pd.to_datetime(Df.Date)
Df.sort_values('Date')

Df.plot(x='Date',y='Price')
plt.title('Gold')
plt.show()

# The statistical properties of data
print(Df.describe())

# Darw histgram of each column
plt.rcParams["figure.figsize"] = (20,8)
hist = Df[["Price","High","Low","Open", 'Volume', 'Change %']].hist(bins=50)
plt.show()

# calculate the correlation matrix
corr = Df[["Price","High","Low","Open",'Volume', 'Change %']].corr()

# plot the heatmap to show the correlations among different price columns 
sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)
plt.show()

# Check the correlation score
print (corr['Price'].sort_values(ascending=False), '\n')

#df.set_index('Date',inplace=True, drop=True)
# create two new columns with lagged terms with different moving window size 
Df['S_1'] = Df["Price"].shift(1).rolling(window=2, center = True).mean()
Df['S_2'] = Df["Price"].shift(1).rolling(window=5, center = True).mean()

# Define exploratory variables
# Finding moving average of past 2 day and 5 days 
Df = Df.dropna()
X = Df[['S_1','S_2']]
print(X.head())
plt.plot(Df['Date'], Df['Price'], color="blue", label = "Original")
plt.plot(Df['Date'], Df['S_1'], color="red", label= "Moving average with window = 2")
plt.plot(Df['Date'], Df["S_2"],color="green", label= "Moving average with window = 5")
plt.legend(loc='best')
plt.show()

# dependent variable
y = Df["Price"]
y.head()
print(Df.shape)

# Split into train and test

# training size 
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

print("Gold Price =", round(linear.coef_[0], 2), "* 2 Days Moving Average", 
     round(linear.coef_[1], 2), "* 5 Days Moving Average +",
      round(linear.intercept_, 2))

# Predict prices
predicted_price = linear.predict(X_test)

predicted_price = pd.DataFrame(
    predicted_price, index=y_test.index, columns=['price'])

predicted_price = pd.DataFrame(predicted_price,index=y_test.index,columns = ['price'])  
predicted_price.plot(figsize=(26,8)) 
y_test.plot()  
plt.legend(['predicted_price for the testing data (the last 20% of the data)','actual_price'])  
plt.ylabel("Gold Price")  
plt.show()

# Calculate R square and rmse to check goodness of fit
r2_score = linear.score(X_test, y_test)*100
print("R square for regression", float("{0:.2f}".format(r2_score)))
print("RMSE: ",sqrt(mean_squared_error(y_test,predicted_price)))

# Mean Absolute Percentage Error
MAPE = np.mean(np.abs((y_test - predicted_price['price']) / y_test))* 100
print('The Mean Absolute Percentage Error for the forecast is {:.2f}%'.format(MAPE))