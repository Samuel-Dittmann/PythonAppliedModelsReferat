import LoadCleanData as LCD

import os
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import tree
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

c = LCD.readConfig() #Die Config wird hier eingelesen und kann mit c["Attributsname"] verwendet werden
currDateTime = datetime.now()
runPath = c['resultPath']+"/Run "+str(currDateTime.strftime("%Y-%m-%d %H-%M-%S.%f"))[:-3] #Hier wird der Run Path festgelegt aus dem Config-Pfad und der aktuellen DateTime

os.makedirs(runPath, exist_ok=True) #Hier wird der Run-Pfad erstellt, falls er noch nicht existiert

data = LCD.loadData(runPath) #Hier werden die Daten geladen, aufbereitet und dem Programm zur Verfügung gestellt


def linear_reg_analysis_on(dataset): 
    print(dataset)
    x = dataset[['co2emissions']] 
    y = dataset[['temperature']] 
    x_train , x_val, y_train, y_val = train_test_split(x,y,test_size = 0.1, random_state=2)
    reg = LinearRegression()
    reg.fit(x_train,y_train) # Model wird trainiert 
    beta_1 = reg.coef_[0,0]
    beta_0 = reg.intercept_[0]
    temperature_predict = reg.predict(x)
    #print('predicted_temperature =', temperature_predict)
    score = reg.score(x_val , y_val )
    reg_result_array = [[beta_0, beta_1, score]]
    df_result = pd.DataFrame(reg_result_array, columns=['Beta_0', 'Beta_1', 'R_squared']).set_index('Beta_0')
    print("\nRegressionsergebnisse:\n", df_result)
    return df_result



""" Regressionsanalyse mit Validierungssample und ß0"""
print("\n*** Regressionsanalyse mit Validierungssample und ß0 ***\n")
result = linear_reg_analysis_on(data)
result.to_csv(runPath+'/reg_analysis_with_sample_and_beta0.csv')


""" Regressionsanalyse ohne Validierungssample und ß0"""
# Die Konstante ß0 ist im Gegensatz zu Sklearn nicht standardmäßig bei statsmodels.api vorhanden 
print("\n*** Regressionsanalyse ohne Validierungssample und ohne ß0 ***\n")
x = data[['co2emissions']] 
y = data[['temperature']] 
model = sm.OLS(y, x).fit()
predictions = model.predict(x)
# Print out the statistics
print(model.summary())

""" Regressionsanalyse von 1880 bis 1980 """
data_1880_1980 = (data.loc['1880':'1980',:])
print("\n*** Regressionsanalyse von 1880 bis 1980 ***\n")
result = linear_reg_analysis_on(data_1880_1980)
result.to_csv(runPath+'/regression_analysis_1880_1980.csv')

""" Regressionsanalyse von 1970 bis 2014 """
data_1970_2014 = (data.loc['1970':'2014',:])
print("\n*** Regressionsanalyse von 1970 bis 2014 ***\n")
result = linear_reg_analysis_on(data_1970_2014)
result.to_csv(runPath+'/regression_analysis_1970_2014.csv')


