from django.conf import settings

class Config():
    def __init__(self, path_config_file:str):
        with open(path_config_file) as file:
            self.config_data = file.readlines()
        
        for idx, line in enumerate(self.config_data):
            self.config_data[idx] = line.strip()

        self.url_weather = self.config_data[1].split(": ")[1]
        self.url_forecast = self.config_data[0].split(": ")[1]
        self.path_prot = self.config_data[2].split(": ")[1]
        self.api_key = self.config_data[3].split(": ")[1]
        self.path_log = self.config_data[4].split(": ")[1]


    def __str__(self):
        string = ""
        for line in self.config_data:
            string += line
        return string


    def get_url_weather(self):
        return self.url_weather.replace("{API key}", self.api_key)
    

    def get_url_forecast(self):
        return self.url_forecast.replace("{API key}", self.api_key)
    

    def get_path_prot(self):
        return self.path_prot
    

    def get_path_log(self):
        return self.path_log

config = Config(getattr(settings, 'CONFIG_PATH'))