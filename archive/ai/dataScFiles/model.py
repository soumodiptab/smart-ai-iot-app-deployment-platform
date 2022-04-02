import numpy as np 
import pandas as pd

from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split 

from xgboost import XGBClassifier
from sklearn.svm import SVC


import warnings 
import pickle

warnings.filterwarnings('ignore')

data=pd.read_csv("weather.csv")



"""Preprocessing"""
df=data.drop(["date", "temp_min", "wind"], axis=1)

Q1=df.quantile(0.25)
Q3=df.quantile(0.75)
IQR=Q3-Q1
df=df[~((df<(Q1-1.5*IQR))|(df>(Q3+1.5*IQR))).any(axis=1)]

df.precipitation=np.sqrt(df.precipitation)

lc=LabelEncoder()
df["weather"]=lc.fit_transform(df["weather"])


"""Input and output"""

x=((df.loc[:,df.columns!="weather"]).astype(int)).values[:,0:]
y=df["weather"].values

"""Train test split"""

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.1,random_state=2)

import warnings
warnings.filterwarnings('ignore')

"""
xgb = XGBClassifier()
xgb.fit(x_train,y_train)

input=[[10.9, 10.6]]

pred = xgb.predict(input)

# save the model to disk
filename = 'model.pkl'
pickle.dump(xgb, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))

pred = loaded_model.predict(input)
"""

svm=SVC()
svm.fit(x_train,y_train)

input=[[10.9, 10.6]]

pred = svm.predict(input)

# save the model to disk
filename = 'model.pkl'
pickle.dump(svm, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))

pred = loaded_model.predict(input)