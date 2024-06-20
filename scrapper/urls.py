from django.urls import path
from .views import ProductViewSet, BrandProductListView


urlpatterns = [
    path('products/', ProductViewSet.as_view(), name="products-list"),
    path('brands/products/', BrandProductListView.as_view(), name='brand-product-list'),

]