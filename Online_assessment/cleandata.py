import pandas as pd
from sklearn import preprocessing

df = pd.read_csv('goldprice_08-May-2020 19-11-07.csv')

print(df.shape)
print(df.info())
print(df.describe())

print(df.isnull().sum())

#Remove data contain "-"
df_clean = df[df['Volume'] != ' -']
print(df_clean.head())

print(df.shape)
print(df_clean.shape)