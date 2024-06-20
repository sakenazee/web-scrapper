from bs4 import BeautifulSoup
from .models import Product
from fake_useragent import UserAgent
import time, random, requests
from django.db import IntegrityError
import logging


ua = UserAgent()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_random_headers():
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'DNT': '1',  # Do Not Track request header
        'Upgrade-Insecure-Requests': '1',
    }
    return headers


def scrape_amazon_brand(brand):
    base_url = brand.amazon_url
    page_number = 1
    next_page_url = base_url  # Start with the initial brand page URL

    while next_page_url:
        logger.info(f"Scraping page {page_number} for brand {brand.name}...")
        response = requests.get(next_page_url, headers=get_random_headers())

        # Check for CAPTCHA
        if "captcha" in response.url:
            logger.error("CAPTCHA encountered! Stopping scraping to avoid detection.")
            break

        # Check for rate limiting (check status code)
        if response.status_code == 429:
            logger.info("Rate limit hit! Backing off for a while before retrying.")
            time.sleep(random.uniform(30, 60))  # Sleep for 30-60 seconds before retrying
            continue

        time.sleep(random.uniform(1, 5))  # Random delay to avoid bot detection
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the product containers on the current page
            products = soup.find_all('div', {'data-component-type': 's-search-result'})

            # Loop through each product and extract details
            for product in products:
                try:

                    name_tag = product.find('span', class_='a-size-medium a-color-base a-text-normal')
                    asin = product.get('data-asin')
                    image_tag = product.find('img', class_='s-image')
                    image_url = image_tag['src'] if image_tag else None
                    try:

                        if name_tag:
                            product_name = name_tag.text.strip()
                            # Use update_or_create to either update the existing product or create a new one
                            Product.objects.update_or_create(
                                asin=asin,  # The lookup field (unique product name)
                                defaults={
                                    'name': product_name,
                                    'image': image_url,
                                    'brand': brand,
                                }
                            )
                    except IntegrityError as e:
                        logger.error(f"Database error encountered: {e}")

                except Exception as e:
                    logger.error(f"An error occurred while processing a product: {e}")

            # Find the "Next" page URL for pagination
            next_page = soup.select_one('a:contains("Next")')

            if next_page:
                next_page_url = "https://www.amazon.com" + next_page['href']
                page_number += 1
            else:
                next_page_url = None  # No more pages
        else:
            logger.error(f"Failed to fetch data. Status code: {response.status_code}")
            break

    logger.info(f"{brand.name} scraping completed.")

