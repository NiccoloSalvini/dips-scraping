import sys
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
from monsterapi.nextGenLLMClient import LLMClient, GenerateRequest

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# SQLAlchemy setup for PostgreSQL connection
DATABASE_URL = "postgresql://admin:f8JQp9B2Mg6EGcoiPE8DRdBW0mso4WVm@dpg-cojjogmd3nmc73bs47r0-a.oregon-postgres.render.com/dips"
engine = create_engine(DATABASE_URL)

# Function to compute dates for the upcoming week
def next_week_dates():
    today = datetime.now()
    next_week = today + timedelta(days=7)
    return today.strftime('%Y-%m-%d'), next_week.strftime('%Y-%m-%d')

# Function to build URL dynamically
def build_url(city, from_date, to_date):
    base_url = "https://www.cozycozy.com/it/search/"
    return f"{base_url}{city}/{from_date}/{to_date}/1-2-0/results"

# Selenium setup with headless option
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # this is must
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options=chrome_options)

def scrape_hotel_data(city):
    from_date, to_date = next_week_dates()
    url = build_url(city, from_date, to_date)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

  #   # Extract data from each listing
  #   data = []
  #   try:
  #       listings = soup.find_all('div', class_='listing-class')  # Placeholder class name
  #       for listing in listings:
  #           title = listing.find('h2').text if listing.find('h2') else 'No title available'
  #           print(title)
  #           price = listing.find('span', class_='price').text if listing.find('span', class_='price') else 'No price available'
  #           print(price)
  #           data.append({'title': title, 'price': price})
  #   except Exception as e:
  #       logging.error(f"Error occurred while extracting data: {e}")
  #   finally:
  #       driver.quit()
    
    return soup.get_text()

# Initialize LLM Client and Process Data
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImU2MDI1NTZkN2NlNzY5NDY1NTQyYzk2M2E2OTg0ZTczIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDQtMTlUMTA6NTg6MDMuMDAwNDQyIn0.OE2EaCPtaVOs9j-i6wKW-UYPzFk0e30YY46m4U0hLtk'  # Replace with your actual API key
client = LLMClient(api_key=api_key)

def process_data_with_llm(data):
    model = "mistralai/Mistral-7B-Instruct-v0.2"
    messages = [{"role": "user", "content": f"Extract structured data from this HTML content: {data}"}]
    request = GenerateRequest(
        model=model,
        messages=messages,
        top_k=50,
        top_p=0.9,
        temperature=0.9,
        max_length=300,
        beam_size=1
    )

    try:
        response = client.generate(request)
        return response
    except Exception as e:
        logging.error(f"Error occurred while generating LLM response: {e}")
        return None

def append_to_database(data_frame):
    try:
        data_frame.to_sql('hotel_listings', con=engine, index=False, if_exists='append')
        logging.info("Data appended to the database successfully")
    except Exception as e:
        logging.error(f"Failed to append data to the database: {e}")

# Example usage
city = 'Firenze'  # Can also be 'Milano' or 'Roma'
hotel_data = scrape_hotel_data(city)
# processed_data = process_data_with_llm(hotel_data)  # Assume this returns a DataFrame or modifies hotel_data
# append_to_database(hotel_data)  # Assuming hotel_data is a DataFrame
