# -*- coding: utf-8 -*-
"""car prices.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z9gLjRLyCYFJ0Hw4z-jgciMZSYVl22Gu
"""

import numpy as np

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import pandas as pd

df = pd.read_csv('train.csv')

df.head()

df_data=df.copy()

df_data.info()

df_data.drop('New_Price',axis=1,inplace=True)

df_data.columns

l = ['Mileage', 'Engine', 'Power']
for c in l :
    print(c)
    print(df_data[c].str.split(' ').str[1].value_counts())
    print('***********************************')

df_data['Engine'].str[:-2]

df_data['Engine'] = df_data['Engine'].str.rstrip(' CC')
df_data['Power'] = df_data['Power'].str.rstrip(' bhp')

df_data.head()

def convert_mileage_int(mileage):
    try:
        new_mileage = float(mileage.split(' ')[0])
        if mileage.split(' ')[1] == 'km/kg':
            new_mileage = new_mileage * 0.74
        return new_mileage
    except :
        return np.nan

df_data['Mileage']=df_data['Mileage'].apply(convert_mileage_int)

df_data['Engine'] = df_data['Engine'].astype('float')

df_data['Power']=pd.to_numeric(df_data['Power'], errors = 'coerce')

df_data.isna().sum()

df_data.dropna(inplace=True)

df_data.describe()

df_data[df_data['Mileage']==0]

import plotly.express as px

px.histogram(df_data['Kilometers_Driven'])

df_data['brand'] = df_data['Name'].str.split(' ').str[0]

df_data['brand'].nunique()

df_data['Model'] = df_data['Name'].str.split().str[1]

df_data['Model'].nunique()

df_data.drop('Name' , axis =1 , inplace = True )

from sklearn.model_selection import train_test_split
X = df_data.drop('Price' , axis =1)
y = df_data['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

from sklearn.preprocessing import RobustScaler
num = ['Year', 'Kilometers_Driven','Mileage', 'Engine', 'Power', 'Seats']
sc = RobustScaler()
sc.fit(X_train[num])

X_train[num] = sc.transform(X_train[num])
X_test[num] = sc.transform(X_test[num])

df_data['Owner_Type'].value_counts()

transformation = {
    "First":3,
    "Second":2,
    "Third":1,
    "Fourth & Above":0
}

X_train['Owner_Type'] = X_train['Owner_Type'].map(transformation)
X_test['Owner_Type'] = X_test['Owner_Type'].map(transformation)

!pip install category_encoders

import category_encoders as ce
Nominal_data = ['Model','Location','Fuel_Type','Transmission','brand']
encoder = ce.BinaryEncoder(cols = Nominal_data )
encoder.fit(X_train)

X_train = encoder.transform(X_train)
X_test = encoder.transform(X_test)

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train , y_train)

reg.score(X_train , y_train)

reg.score(X_test , y_test)

reg.fit(X_train , np.log(y_train))

reg.score(X_train , np.log(y_train))
reg.score(X_test , np.log(y_test))

from sklearn.linear_model import Ridge

ridge=Ridge()

ridge.fit(X_train,y_train)

y_pre=ridge.predict(X_test)

from sklearn.metrics import mean_squared_error
print('RMSE:',np.sqrt(mean_squared_error(y_test,y_pre)))

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

poly=make_pipeline(PolynomialFeatures(2),Ridge())

poly.fit(X_train,y_train)

y_pre=poly.predict(X_test)

print('RMSE:',np.sqrt(mean_squared_error(y_test,y_pre)))

import pickle
pickle.dump(poly,open('model.pkl','wb'))

from sklearn.svm import LinearSVR

model = LinearSVR()
model.fit(X_train,y_train)

print('Accuracy: ', model.score(X_train,y_train))

from sklearn.ensemble import VotingClassifier

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import VotingRegressor

svr = SVR(kernel='linear')

voting_reg=VotingRegressor(estimators=[('lr',LinearRegression() ),('dt',DecisionTreeRegressor()),('svr',svr)])

voting_reg.fit(X_train,y_train)

voting_reg.score(X_train , y_train)

from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import  DecisionTreeRegressor

lin_re= LinearRegression()
ridge=Ridge()
lasso=Lasso()
dt_reg=DecisionTreeRegressor(max_depth=10)
bag_reg=BaggingRegressor(dt_reg,n_estimators=100,bootstrap=True,random_state=42,max_features=0.8)
bag_reg.fit(X_train,y_train)

print('training score:',bag_reg.score(X_train,y_train))

print('testing score:',bag_reg.score(X_test,y_test))

"""Random forest"""

from sklearn.ensemble import RandomForestRegressor

rf_reg= RandomForestRegressor (n_estimators=100,max_depth=10,random_state=42)

rf_reg.fit(X_train,y_train)

print('training score:',rf_reg.score(X_train,y_train))
print('testing score:',rf_reg.score(X_test,y_test))

rf_reg.feature_importances_

pd.DataFrame({'feature':X_train.columns,'Importance':rf_reg.feature_importances_.round(3)}).sort_values('Importance',ascending=False)

import matplotlib.pyplot as plt
import seaborn as sns
plt .figure(figsize=(12,8))
sns.barplot (x=rf_reg.feature_importances_,y=X_train.columns)

from sklearn.ensemble import AdaBoostRegressor
ada_reg=AdaBoostRegressor()
ada_reg.fit(X_train,y_train)
print('training score:',ada_reg.score(X_train,y_train))
print('testing score:',ada_reg.score(X_test,y_test))

pip install xgboost

from xgboost import XGBRegressor
xgb=XGBRegressor(n_estimators=100)
xgb.fit(X_train,y_train)
print('training score:',xgb.score(X_train,y_train))
print('testing score:',xgb.score(X_test,y_test))

from sklearn.ensemble import GradientBoostingRegressor
Grd=GradientBoostingRegressor()
Grd.fit(X_train,y_train)
print('training score:',Grd.score(X_train,y_train))
print('testing score:',Grd.score(X_test,y_test))

from sklearn.model_selection import cross_val_score
score=cross_val_score(LinearRegression(),X_train,y_train,cv=5)
score

print('mean score :' ,score.mean())

ridge_score=cross_val_score(Ridge(),X_train,y_train,cv=5)

ridge_score

print('ridge_score :' ,ridge_score.mean())

from sklearn.model_selection import GridSearchCV