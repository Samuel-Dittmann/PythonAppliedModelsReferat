import LoadCleanData as LCD
import pandas as pd
import os
from datetime import datetime

c = LCD.readConfig()
currDateTime = datetime.now()
runPath = c['resultPath']+"/Run "+str(currDateTime.strftime("%Y-%m-%d %H-%M-%S.%f"))[:-3]

os.makedirs(runPath, exist_ok=True)

data = LCD.loadData(runPath)

