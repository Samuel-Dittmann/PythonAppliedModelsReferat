import json

def readConfig():
    with open('Code/Config.json') as config_file: #Config Datei lesen
        c = json.load(config_file)
        return c
