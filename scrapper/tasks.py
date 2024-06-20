from celery import shared_task
from .models import Brand
from .scrapper_utils import scrape_amazon_brand
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def scrape_all_brands():
    start_time = datetime.now()
    logger.info(f"Task started at {start_time}")

    brands = Brand.objects.all()
    for brand in brands:
        scrape_amazon_brand(brand)

    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Task ended at {end_time}. Duration: {duration}")
