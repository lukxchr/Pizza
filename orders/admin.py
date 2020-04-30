from django.contrib import admin

# Register your models here.

from .models import Category, Size, MenuItem, MenuItemAddon, Address, Order, OrderItem, OrderItemAddon

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(MenuItem)
admin.site.register(MenuItemAddon)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemAddon)

