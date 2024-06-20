
# Amazon Scrapper Project

This project is a Django-based Amazon product scraper that scrapes product details such as name, ASIN, image URL, and brand from Amazon. The application uses Celery for task management and Redis as the message broker.

## Features
- Scrapes Amazon products by brand.
- Stores product information in the database.
- Celery tasks for periodic scraping.
- Uses Redis for managing Celery tasks.
- Dockerized for easy setup and deployment.
- Django Admin interface for adding brands and managing Amazon URLs.
- Rest APIs to review the scrapped data.

## Technologies Used
- Django
- Django Rest Framework
- Celery
- Redis
- Docker

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the repository:

```bash
find in github action button
cd repo_folder
```

### 2. Build and run the Docker containers:

Run the following command to build the Docker images and start the containers:

```bash
docker-compose up --build
```

### 3. Access the application:

Once the containers are up and running, you can access the application in your browser at:

- Django app: `http://localhost:8000`
- Django Admin: `http://localhost:8000/admin/`

### 4. Adding Brands in Django Admin:

- Use the Django Admin interface to add brands and their respective Amazon URLs in the format: 
    ```
    https://www.amazon.com/s?k=<brand_name>
    ```
- Example brand names: Samsung, Apple, etc.

### 5. Run the scraper:

The Celery Beat service will automatically run the scraping task every 6 hours based on the configuration. You can adjust the frequency in `settings.py`.

To manually trigger the scraping task:

```bash
docker-compose exec web python manage.py scrape_all_brands
```

## Celery Task Management

- To view logs for the Celery worker:

```bash
docker-compose logs celery
```

- To view logs for Celery Beat (for periodic tasks):

```bash
docker-compose logs celery-beat
```

## Configuration

### Celery Configuration
- The periodic task configuration is located in `settings.py` under the `CELERY_BEAT_SCHEDULE` setting.
- Redis is used as the broker for Celery tasks.

```python
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
```

### Changing Scraping Frequency
By default, scraping is scheduled every 6 hours. You can change this in `settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'scrape-amazon-every-six-hours': {
        'task': 'scrapper.tasks.scrape_all_brands',
        'schedule': 6 * 60 * 60,  # Run every 6 hours
    },
}
```

## API Usage

- To view products under a specific brand, you can use the following API endpoint:
  ```bash
  GET /api/brands/products/
  ```

## Running Tests

To run tests inside the Docker container:

```bash
docker-compose exec web python manage.py test
```

## Troubleshooting

- **Issue**: `redis.exceptions.ConnectionError: Error 111 connecting to redis:6379`
  
  **Solution**: Make sure that the Redis container is running properly. You can restart the service by running:
  
  ```bash
  docker-compose up redis
  ```

- **Issue**: `sqlite3.IntegrityError: UNIQUE constraint failed`

  **Solution**: Make sure that you have proper handling for unique fields like `ASIN` in your models and scraping logic.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
