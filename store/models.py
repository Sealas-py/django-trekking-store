from django.conf import settings
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    name = models.CharField(max_length=64)
    short_description = models.TextField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField()
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category', related_name='store', on_delete=models.CASCADE)
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='parent_products')
    root_category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='store_products')

    def save(self, *args, **kwargs):
        self.parent_category = self.category.parent
        self.root_category = self.category.get_root()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=64)
    parent = TreeForeignKey('self',
                            blank=True,
                            null=True,
                            related_name='children',
                            on_delete=models.CASCADE
                            )
    slug = models.SlugField(unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "Przyjęte"
        PAID = "Opłacone"
        PREPARING = "W przygotowaniu"
        SENT = "Wysłane"
        FINISHED = "Zakończone"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.CREATED)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
