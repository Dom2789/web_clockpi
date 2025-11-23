from _lib.API_handler import API_handler
from datetime import datetime
import logging
import json

# parse for openweather specific JSON 
# move it form API_handler.py parse-function

class Openweather(API_handler):

    def __init__(self, url:str):
        super().__init__()
        self.parsed_data = {}
        self.url = url
        self.keys = ["now", "+3h", "+6h", "+9h"]


    def parse_data(self):
        # get data 
        self.data = self.get_posts(self.url)

        if self.data is not None:  
            # parsing data
            self.parsed_data['city'] = self.data['city']
            for idx, key in enumerate(self.keys):
                self.parsed_data[key] = self.data["list"][idx]


    def __str__(self):
        if self.parsed_data == {}:
            if self.data == None:
                return "No data availible yet"
            
            else: 
                return self.data
        
        else:
            return self.print_parsed_data()
        

    def print_parsed_data(self, de_en = False) -> str:
        if self.parsed_data == {}:
            return "No parsed data availible yet"

        else:
            city:dict = self.parsed_data["city"]
            string = "Parsed data:\n\n"
            string +=f"City: {city['name']}\n"
            
            string += f"Sunrise: {self.str_from_timestamp(city['sunrise'])}\n"

            string += f"Sunrise: {self.str_from_timestamp(city['sunset'])}\n"

            for key in self.keys:
                string += f"\n{key}\n"

                main = self.parsed_data[key]["main"]
                weather = self.parsed_data[key]["weather"][0]
                wind = self.parsed_data[key]["wind"]

                string += f"Temperature: {main['temp']}°C\n"
                string += f"Feels like: {main['feels_like']}\n"

                if de_en:
                    string += f"Description: {weather['description']}\n"
                else:
                    string += f"Description: {weather['main']}\n"

                string += f"Wind speed: {wind['speed']}m/s\n"
                string += f"Wind direction: {self.degree_to_direction(float(wind['deg']), long_string= True)}\n"

                string += "\n"

            return string


    def save_parsed_data_to_json_file(self, path:str):
        if self.parsed_data == {}:
            
            logging.info("Tried to save parsed data to file, when no data is available.")
        else:
            file = path + "parsed_data.json" 
            with open(file, "w") as f:
                json.dump(self.parsed_data, f)
            logging.info(f"Saved parsed data to {file}")
        


    @staticmethod
    def str_from_timestamp(ts:str) -> str:
        return datetime.fromtimestamp(int(ts)).strftime('%H:%M:%S')
    

    @staticmethod
    def degree_to_direction(degree:float, long_string:bool = False, de_en:bool = False) -> str:
        wind_direction_long_de = {
            "N": "Norden",
            "NO": "Nordosten",
            "O": "Osten",
            "SO": "Südosten",
            "S": "Süden",
            "SW": "Südwesten",
            "W": "Westen",
            "NW": "Nordwesten"
        }
        
        wind_direction_long_en = {
            "N": "North",
            "NO": "Northeast",
            "O": "East",
            "SO": "Southeast",
            "S": "South",
            "SW": "Southwest",
            "W": "West",
            "NW": "Northwest"
        }
        
        if (degree >= 337.5 or degree < 22.5): 
            direction = "N"  
        elif (degree >= 22.5 and degree < 67.5):
            direction = "NO"
        elif (degree >= 67.5 and degree < 112.5):
            direction = "O"
        elif (degree >= 112.5 and degree < 157.5):
            direction = "SO"
        elif (degree >= 157.5 and degree < 202.5):
            direction = "S"
        elif (degree >= 202.5 and degree < 247.5):
            direction = "SW"
        elif (degree >= 247.5 and degree < 292.5):
            direction = "W"
        elif (degree >= 292.5 and degree < 337.5):
            direction = "NW"
        else:
            direction = "N/A"
            return direction
        
        if long_string:
            if de_en:
                direction = wind_direction_long_de[direction]
            else:
                direction = wind_direction_long_en[direction]
        
        return direction
    

    # ----- getters -----
    def get_parsed_data_valid(self) -> bool:
        if self.parsed_data == {}:
            return False
        else:
            return True

    def get_keys_time_data(self) -> list[str]:
        return self.keys

    def get_keys_parsed_data(self) -> list[str]:
        keys = self.parsed_data.keys()
        return keys

    def get_city(self) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return self.parsed_data["city"]["name"]

    def get_sunset(self) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return self.str_from_timestamp(self.parsed_data["city"]["sunset"])
        
    def get_sunrise(self) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return self.str_from_timestamp(self.parsed_data["city"]["sunrise"])
    
    def get_temperature(self, key:str) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return self.parsed_data[key]["main"]["temp"]
        
    def get_feels_like(self, key:str) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return self.parsed_data[key]["main"]["feels_like"]
        
    def get_weather_description(self, key:str, de_en = False) -> str:
        if self.parsed_data == {}:
            return "no data"
        elif de_en:
            return self.parsed_data[key]["weather"][0]["description"]
        else:
            return self.parsed_data[key]["weather"][0]["main"]
        
    def get_weather_icon(self, key:str) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return  self.parsed_data[key]["weather"][0]["icon"]
        
    def get_wind_speed(self, key:str) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return self.parsed_data[key]["wind"]["speed"]
        
    def get_wind_direction(self, key:str, de_en:bool = False) -> str:
        if self.parsed_data == {}:
            return "no data"
        else:
            return self.degree_to_direction(float(self.parsed_data[key]["wind"]["deg"]), long_string= True, de_en= de_en)