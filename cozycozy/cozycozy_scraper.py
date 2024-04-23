import os
import json
import logging
from selenium_utils import SeleniumUtility
from monsterapi.nextGenLLMClient import LLMClient, GenerateRequest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
CITY_URLS = {
    "Firenze": "https://www.cozycozy.com/gb/search/Firenze%2C%20Italia/2024-04-27/2024-04-28/1-1-0/results",
    "Milano": "https://www.cozycozy.com/gb/search/Milan%2C%20Italy/2024-04-27/2024-04-28/1-1-0/results",
    "Rome": "https://www.cozycozy.com/gb/search/Rome%2C%20Italy/2024-04-27/2024-04-28/1-1-0/progress",
}
MONSTER_API_KEY = os.environ['MONSTER_API_KEY']

def scrape_hotel_listings():
    selenium_util = SeleniumUtility()
    client = LLMClient(api_key=MONSTER_API_KEY)
    model = "mistralai/Mistral-7B-Instruct-v0.2"
    parameters = {
        'top_k': 50,
        'top_p': 0.9,
        'temperature': 0.6,
        'max_length': 300,
        'beam_size': 1
    }
    results = {}
    for city, url in CITY_URLS.items():
        try:
            page_content = selenium_util.get_page_content(url)
            input_data = {
                'messages': [
                    {"role": "user", "content": f"Extract hotel listing information from the following HTML: {page_content}"}
                ]
            }
            request = GenerateRequest(model=model, messages=input_data['messages'], **parameters)
            response = client.generate(request)
            results[city] = response
        except Exception as e:
            logging.error(f"Failed to scrape data for {city}: {e}")
            results[city] = str(e)
    return results

if __name__ == "__main__":
    results = scrape_hotel_listings()
    print(json.dumps(results, indent=4))
