from django.contrib import admin

# Register your models here.

from .models import Category, Size, MenuItem, MenuItemAddon

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(MenuItem)
admin.site.register(MenuItemAddon)
