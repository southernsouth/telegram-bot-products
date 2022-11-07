
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()
from django.core.management.base import BaseCommand
from products.models import ProductsList

import asyncio
from asgiref.sync import sync_to_async



async def get_products_count():
    count = await sync_to_async(ProductsList.objects.filter)(status=True)
    count = await sync_to_async(len)(count)
    return count

async def get_product_name(id):
    product = await sync_to_async(ProductsList.objects.get)(id=id)
    product_name = product.product_name
    return product_name

async def get_products_id():
    products = await sync_to_async(ProductsList.objects.filter)(status=True)
    products = await sync_to_async(products.values_list)('id', flat=True)
    return products
