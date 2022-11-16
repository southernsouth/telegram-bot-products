from django.contrib import admin
from .models import ProductsList
from faker import Faker



@admin.register(ProductsList)
class ProductsListAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'status')

    '''for i in range(1):
        faker = Faker('en_us')
        product_name = faker.name()
        description = 'Nigga'
        price = faker.random.randint(0, 1000)
        image = None
        status = True
        data = ProductsList(product_name=product_name, description=description, price=price, image=image, status=status)
        data.save()'''
