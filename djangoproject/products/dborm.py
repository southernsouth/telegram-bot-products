
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()
from django.core.management.base import BaseCommand
from products.models import ProductsList

import asyncio
from asgiref.sync import sync_to_async



async def get_product_count():
    return await sync_to_async(ProductList.objects.count)()

