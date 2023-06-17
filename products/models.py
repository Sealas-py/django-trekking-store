from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField()
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
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
    background_image = models.ImageField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
