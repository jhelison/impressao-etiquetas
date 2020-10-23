import json
import os

class ConfigDB():
    def __init__(self):
        if not os.path.isdir('./config'):
            os.makedirs('./config')
            
        try:
            self.getConfig()
        except:
            self.config = {}
            self.init()
            
  
    def init(self):
        self.config['leDBFile'] = ""
        self.config['leLogin'] = "sysdba"
        self.config['lePassword'] = "masterkey"
        self.config['leOutuput'] = ""
           
        with open('./config/config.json', 'w') as f:     
            json.dump(self.config, f)
            f.close()
            
    def get(self, key):
        with open('./config/config.json', 'r') as f:
            text = f.read()
            config = json.loads(text)
            f.close()
        
        return config[key]
    
    def save(self, key, value):
        self.getConfig()
        self.config[key] = value
        
        with open('./config/config.json', 'w') as f:
            json.dump(self.config, f)
            f.close()
            
    def getConfig(self):
        with open('./config/config.json', 'r') as f:
            text = f.read()
            config = json.loads(text)
            f.close()
            
        self.config = config