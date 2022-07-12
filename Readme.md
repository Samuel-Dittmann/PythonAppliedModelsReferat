# Konfiguratiosanweisungen:

Der Dateipfad zu den Datenquellen und dem Result-Ordner muss in der JSON File "Code/Config.json" angegeben werden. </br>
In dieser Datei können auch alle weiteren Parameter bearbeitet werden. Diese sind jedoch optional.

## Obligatorische Libraries:
- numpy
- scipy
- pandas
- matplotlib
- statsmodels

## Bekannte Fehler:
In der Datei "Code/LoadCleanData.py" wird in der Fuktion "ReadConfig" auf die Konfigurationsdatei verwiesen. </br>
Unter MacOSX muss hier 'Code/Config.json' stehen und unter Windows 'Config.json'. </br>
Ist das nicht richtig Konfiguriert, wird ein Fehler ausgegeben!