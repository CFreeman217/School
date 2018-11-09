import pandas as pd
<<<<<<< HEAD
import quandl
import math, datetime
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
# from matplotlib import style
import pickle
# style.use('ggplot')

# Gather google stock price information
df = quandl.get('WIKI/GOOGL')

# Collect and filter the data set and columns. Generate calculations for whatever we want
df = df[['Adj. Open','Adj. High','Adj. Low', 'Adj. Close','Adj. Volume',]]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

# Generate formed columns of the data we are intereested in
df = df[['Adj. Close','HL_PCT','PCT_change','Adj. Volume']]

# print(df.head())

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

# Try to predict out 10% out of the dataframe. Predicting the price 10 days from now using 10% of the dataframe (1/10)
forecast_out = int(math.ceil(0.01*len(df)))
print(forecast_out)
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)
print(df.tail())

# Store new array generated from the df.drop command
x_1 = np.array(df.drop(['label'],1))
x_3 = preprocessing.scale(x_1)
y = np.array(df['label'])
x_2 = x_3[:-forecast_out]
x_lately = x_3[-forecast_out:]
# New values need to be scaled alongside the other values

x_train, x_test, y_train, y_test = model_selection.train_test_split(x_3, y, test_size=0.2)

# # Algorithm to run
# clf = LinearRegression(n_jobs=-1)
# # clf = svm.SVR()
# clf.fit(x_train, y_train)
# with open('linearregression.pickle','wb') as f:
#     pickle.dump(clf, f)

pickle_in = open('linearregression.pickle','rb')
clf = pickle.load(pickle_in)

accuracy = clf.score(x_test, y_test)
# print(accuracy)

forecast_set = clf.predict(x_lately)

print(forecast_set, accuracy, forecast_out)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
=======
import Quandl

df = Quandl.get('WIKI/GOOGL')
print(df.head)
>>>>>>> ac9985a49526b59bfb453ac445964cd534d8aa64
