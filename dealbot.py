import requests
from bs4 import BeautifulSoup
import yaml
import smtplib
from email.mime.text import MIMEText
import schedule
import time
import logging
import re
from oauth2 import get_oauth2_token
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load config
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Email Settings from .env
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))

# Search and Source Settings
SEARCH_TERMS = config['search_terms']
API_SOURCES = config['api_sources']

# Function to send email
def send_email(results):
    logging.info("Sending email with deals...")
    msg = MIMEText("\n".join(results))
    msg['Subject'] = '🤑 Online Deals Found!'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        logging.info("✅ Email sent successfully!")
    except Exception as e:
        logging.error(f"❌ Failed to send email: {e}")

# Function to query APIs securely
def query_api(source, term):
    try:
        logging.info(f"Querying {source['name']} for '{term}'...")

        if source['auth_type'] == 'oauth2':
            if source['name'] == 'Amazon':
                token = get_oauth2_token(
                    os.getenv('AMAZON_CLIENT_ID'),
                    os.getenv('AMAZON_CLIENT_SECRET'),
                    os.getenv('AMAZON_TOKEN_URL')
                )
            elif source['name'] == 'Target':
                token = get_oauth2_token(
                    os.getenv('TARGET_CLIENT_ID'),
                    os.getenv('TARGET_CLIENT_SECRET'),
                    os.getenv('TARGET_TOKEN_URL')
                )
            headers = {'Authorization': f'Bearer {token}'}

        elif source['auth_type'] == 'bearer':
            token = os.getenv(f"{source['name'].upper()}_TOKEN")
            headers = {'Authorization': f'Bearer {token}'}

        elif source['auth_type'] == 'key':
            api_key = os.getenv(f"{source['name'].upper()}_API_KEY")
            headers = {'apikey': api_key}

        else:
            headers = {}

        url = f"{source['endpoint']}?q={term}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'items' in data:
            return [
                f"💸 {item.get('title', 'Unknown Item')} - ${item.get('price', {}).get('value', 'Unknown Price')} → [Link]({item.get('link', '#')})"
                for item in data['items']
            ]
        elif 'results' in data:
            return [
                f"💸 {item.get('title', 'Unknown Item')} - ${item.get('price', 'Unknown Price')} → [Link]({item.get('url', '#')})"
                for item in data['results']
            ]
        else:
            return []
    
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error querying {source['name']}: {e}")
        return []

# Function to scrape all sources
def scrape_apis():
    results = []
    for source in API_SOURCES:
        for term in SEARCH_TERMS:
            results += query_api(source, term)
    return results

# Function to run scraper
def run_scraper():
    logging.info("🔎 Running deal scraper...")
    results = scrape_apis()
    
    if results:
        logging.info(f"✅ Found {len(results)} new deals")
        send_email(results)
    else:
        logging.info("ℹ️ No new deals found.")

# Schedule to run every hour
schedule.every(1).hours.do(run_scraper)

# Run loop
if __name__ == "__main__":
    logging.info("Starting deal scraper...")
    run_scraper()
    while True:
        schedule.run_pending()
        time.sleep(1)
