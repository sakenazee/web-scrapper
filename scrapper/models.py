from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    amazon_url = models.URLField(help_text="URL to the Amazon brand page")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    asin = models.CharField(max_length=10, unique=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    image = models.URLField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
