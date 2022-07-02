from numpy import diff
import pandas as pd
import json
from scipy.stats import zscore
import matplotlib.pyplot as plt

def readConfig():
    with open('Code/Config.json') as config_file: #Config Datei lesen
        c = json.load(config_file)
        return c

def loadData(resultPath):

    c = readConfig()

    filterCountries = c["filterCountries"] #Liste an zu filternden Ländern aus der Config lesen
    filterSource = c["filterSource"] #Liste an zu filternden Quellen aus der Config lesen

    co2emissions = pd.read_csv(c['dataPath'] + '/fossil-fuel-co2-emissions-by-nation.csv') #Lesen der co2emissionen
    temperature = pd.read_json(c['dataPath'] + '/TemperaturZeitreihe.json') #Lesen der Temperatur

    booleanFilter = co2emissions.Country.isin(filterCountries) #Filter nach Land
    co2emissionsCountry = co2emissions[booleanFilter] #Filter nach Land
    co2emissionsCountryYearly = co2emissionsCountry.groupby(['Year']).sum() #Jahressumme aller selektierten Länder
    co2emissionsFinal = co2emissionsCountryYearly["Total"] #Spalte isolieren

    booleanFilter = temperature.Source.isin(filterSource) #Filter nach Quellen
    temperatureSource = temperature[booleanFilter] #Filter nach Quellen
    temperatureSource['Year'] = temperatureSource['Date'].dt.year #Jahr aus Datum extrahieren
    temperatureSourceYear = temperatureSource.groupby(['Year']).mean() #Arithmetisches Mittel der Temperature pro Jahr
    temperatureFinal = temperatureSourceYear["Mean"] #Spalte isolieren

    concatenatedTable = pd.concat([co2emissionsFinal, temperatureFinal], axis=1)
    concatenatedTable.rename(columns={"Total": 'co2emissions', "Mean": 'temperature'}, inplace=True)
    concatenatedTable.dropna(inplace=True)

    concatZScore = concatenatedTable.apply(lambda x: zscore(x))
    concatZScore = concatZScore < c["zScoreThreshold"]


    concatFlats = concatenatedTable.copy()
    concatFlats['co2FlatValue'] = concatFlats.co2emissions - concatFlats.co2emissions.shift()
    concatFlats['tempFlatValue'] = concatFlats.temperature - concatFlats.temperature.shift()
    concatFlats['co2Flat'] = concatFlats['co2FlatValue'] != 0
    concatFlats['tempFlat'] = concatFlats['tempFlatValue'] != 0
    concatFlats = concatFlats[['co2Flat', 'tempFlat']]
    concatFlats = concatFlats.rename(columns={'co2Flat': 'co2emissions', 'tempFlat': 'temperature'})

    concatenatedTableWOOutliers = concatenatedTable[concatZScore] #Filter nach Z-Score
    concatenatedTableWOOutliers = concatenatedTableWOOutliers[concatFlats] #Filter nach Flats
    concatenatedTableWOOutliers = concatenatedTableWOOutliers.dropna()

    print(str(len(concatenatedTable) - len(concatenatedTableWOOutliers))+" Outliers were removed")

    concatenatedTableWOOutliers.to_csv(resultPath + "/dataSet.csv")

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(concatenatedTableWOOutliers['co2emissions'], 'g-')
    ax2.plot(concatenatedTableWOOutliers['temperature'], 'b-')

    ax1.set_xlabel('Jahre')
    ax1.set_ylabel('CO2 Emissionen', color='g')
    ax2.set_ylabel('Durschnittstemperatur', color='b')

    plt.savefig(resultPath+"/Visualisierung.png")

    return concatenatedTableWOOutliers



