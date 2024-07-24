from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

class Category(models.Model):
    shops = models.ManyToManyField(Shop, related_name='categories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.shop.name}'

class Parameter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, related_name='product_parameters', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.parameter.name}: {self.value}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        
    ]
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    product = models.ForeignKey(Product,related_name='order', on_delete=models.CASCADE)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class Contact(models.Model):
    address = models.CharField(max_length=255, default='Адрес', verbose_name='Адрес доставки:', null=True, blank=True)
    phone = models.CharField(max_length=255, default='Номер телефона', verbose_name='Номер телефона:', null=True, blank=True)
    email = models.CharField(max_length=255, default='Email', verbose_name='Email:', null=True, blank=True)
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.address}: {self.phone}: {self.email}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    adress = models.ForeignKey(Contact, related_name='order_items', on_delete=models.CASCADE )

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'