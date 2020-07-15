from django.contrib import admin
from django.utils.timezone import now

from .models import Category, Size, MenuItem, MenuItemAddon, Address, Order, \
                    OrderItem, OrderItemAddon, Payment

class OrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name_plural = 'Orders Dashboard'
    def __str__(self):
        time_since_created = now() - self.creation_datetime
        return f'''Placed {str(time_since_created).split(".")[0]} ago |
            payment_method: {self.payment_method} | paid: {self.is_paid} 
            | by: {self.customer}'''


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False


class OrderProxyAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = [
        'creation_datetime', 'customer', 'delivery_address', 'notes',
        'total_price', 'payment_method', 'is_paid',
        ]

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(MenuItem)
admin.site.register(MenuItemAddon)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderProxy, OrderProxyAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderItemAddon)
admin.site.register(Payment)
