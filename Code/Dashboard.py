import LoadCleanData as LCD
import pandas as pd
import os
from datetime import datetime

c = LCD.readConfig() #Die Config wird hier eingelesen und kann mit c["Attributsname"] verwendet werden
currDateTime = datetime.now()
runPath = c['resultPath']+"/Run "+str(currDateTime.strftime("%Y-%m-%d %H-%M-%S.%f"))[:-3] #Hier wird der Run Path festgelegt aus dem Config-Pfad und der aktuellen DateTime

os.makedirs(runPath, exist_ok=True) #Hier wird der Run-Pfad erstellt, falls er noch nicht existiert

data = LCD.loadData(runPath) #Hier werden die Daten geladen, aufbereitet und dem Programm zur Verfügung gestellt


'''

HIER BEGINNT DIE REGRESSION!!!
Bitte alle abzulegenden Dateien im runPath ablegen
Bitte das Dataset "data" verwenden

'''

