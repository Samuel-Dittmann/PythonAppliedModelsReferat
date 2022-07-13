import LoadCleanData as LCD
import Config as cfg

import os
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import tree
from sklearn.model_selection import train_test_split
import statsmodels.api as sm


def linear_reg_analysis_on(dataset, percentage_of_testdata): 
    print(dataset)
    x = dataset[['co2emissions']] 
    y = dataset[['temperature']] 
    x_train , x_val, y_train, y_val = train_test_split(x,y,test_size = percentage_of_testdata, random_state=2)
    reg = LinearRegression()
    reg.fit(x_train,y_train) # Train the model
    beta_1 = reg.coef_[0,0]
    beta_0 = reg.intercept_[0]
    temperature_predict = reg.predict(x)
    score = reg.score(x_val , y_val )
    reg_result_array = [[beta_0, beta_1, score]]
    df_result = pd.DataFrame(reg_result_array, columns=['Beta_0', 'Beta_1', 'R_squared'])#.set_index('Beta_0')
    print("\nRegressionsergebnisse:\n", df_result)
    return { 'x':x, 'y':y,'predict':temperature_predict, 'result':df_result}

def create_regression_graph(regression_obj, title):
    result = regression_obj['result']
    plt.plot(regression_obj['x'].values.reshape(-1,1), regression_obj['predict'],color='k')
    plt.scatter(regression_obj['x'], regression_obj['y'],color='g')
    plt.title(title +"\nß0="+str(round(result.iloc[0,0],6))+", ß1="+str(round(result.iloc[0,1],6))+\
              ", R²="+str(round(result.iloc[0,2],6)), color="y")
    plt.xlabel('CO2 Emissionen')
    plt.ylabel('Temperatur')
    plt.show()


c = cfg.readConfig() #Die Config wird hier eingelesen und kann mit c["Attributsname"] verwendet werden
currDateTime = datetime.now()
runPath = c['resultPath']+"/Run "+str(currDateTime.strftime("%Y-%m-%d %H-%M-%S.%f"))[:-3] #Hier wird der Run Path festgelegt aus dem Config-Pfad und der aktuellen DateTime

os.makedirs(runPath, exist_ok=True) #Hier wird der Run-Pfad erstellt, falls er noch nicht existiert

data = LCD.loadData(runPath) #Hier werden die Daten geladen, aufbereitet und dem Programm zur Verfügung gestellt


""" Regressionsanalyse mit Validierungssample und ß0"""
print("\n*** Regressionsanalyse mit Validierungssample und ß0 ***\n")
regression = linear_reg_analysis_on(data, 0.2)
result = regression['result']
result.to_csv(runPath+'/reg_analysis_with_sample_and_beta0.csv')
create_regression_graph(regression, \
    "Regressionsanalyse mit Validierungssample und ß0")




""" Regressionsanalyse ohne Validierungssample und ß0"""
# In contrast to Sklearn, the constant ß0 is not available by default in statsmodels.api
print("\n*** Regressionsanalyse ohne Validierungssample und ohne ß0 ***\n")
x = data[['co2emissions']] 
y = data[['temperature']] 
model = sm.OLS(y, x).fit()
predictions = model.predict(x)
# Print out the statistics
print(model.summary())
# Plot a graph
fig, ax = plt.subplots()
fig = sm.graphics.plot_fit(model, 0, ax=ax)
ax.set_ylabel("Temperatur")
ax.set_xlabel("CO2 Emissionen")
ax.set_title("Regressionsanalyse ohne Validierungssample und ohne ß0\n"\
             + str(model.params)+", R²="+str(model.rsquared), color="y")
plt.show()

""" Regressionsanalyse von 1880 bis 1980 """
data_1880_1980 = (data.loc['1880':'1980',:])
print("\n*** Regressionsanalyse von 1880 bis 1980 ***\n")
regression = linear_reg_analysis_on(data_1880_1980, 0.3)
result = regression['result']
result.to_csv(runPath+'/regression_analysis_1880_1980.csv')
create_regression_graph(regression, "Regressionsanalyse von 1880 bis 1980")

""" Regressionsanalyse von 1970 bis 2014 """
data_1970_2014 = (data.loc['1970':'2014',:])
print("\n*** Regressionsanalyse von 1970 bis 2014 ***\n")
regression = linear_reg_analysis_on(data_1970_2014, 0.1)
result = regression['result']
result.to_csv(runPath+'/regression_analysis_1970_2014.csv')
create_regression_graph(regression, "Regressionsanalyse von 1970 bis 2014")


