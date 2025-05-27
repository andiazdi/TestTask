from django.db import models
from apps.users.models import TelegramUser


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        to_field='telegram_id',
        db_column='user_id'
    )
    address = models.TextField()

    def __str__(self):
        return f"Order #{self.id} from {self.user}"

    class Meta:
        db_table = 'orders'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.TextField(blank=True)
    category_id = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'products'
        ordering = ['title']


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product.name} x{self.quantity}"

    class Meta:
        db_table = 'order_items'
        unique_together = ('order', 'product_id')