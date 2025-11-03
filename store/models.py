from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to='products/', null=True, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      
        return f"Order #{self.id}: {self.product.title} by {self.buyer.username}"