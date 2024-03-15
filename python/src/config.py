import json

config_file = "./config.json"

def getConfig():
    f = open(config_file)
    data = json.load(f)
    return data
