from django.contrib import admin

from .models import Cart, CartItem, Category, OrderItem, Order, Product

admin.site.register(Category)
admin.site.register(Product)


class CartItemInline(admin.TabularInline):
    model = CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer']
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'status']
    inlines = [OrderItemInline]
