import requests
import logging

class API_handler():

    def __init__(self):
        self.data = None     


    @staticmethod
    def get_posts(url:str, logger=logging):
        try:
            # Make a GET request to the API endpoint using requests.get()
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                posts = response.json()
                logger.info("API-call successfull")
                return posts
            else:
                logger.error(f"Satuscode after bad call:{response.status_code}")
                return None
            
        except requests.exceptions.RequestException as e:
            # Handle any network-related errors or exceptions
            logger.critical(e)
            return None
        

  