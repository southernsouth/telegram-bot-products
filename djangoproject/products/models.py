from django.db import models



class ProductsList(models.Model):
    product_name = models.CharField('Product name', max_length=124) 
    description = models.TextField('Description', max_length=900)
    price = models.FloatField('Price')
    image = models.ImageField('Image', max_length=500)
    status = models.BooleanField('Status')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'