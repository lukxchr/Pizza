from django.db import models
from django.contrib.auth.models import User

class StandardStrMixin():
	def __str__(self):
		fields = [f'{field.name}: {getattr(self, field.name)}' for field in self.__class__._meta.fields]
		return f"{type(self).__name__}: {', '.join(fields)}"

class Category(models.Model):
	name = models.CharField(max_length=64)
	is_pizza_category = models.BooleanField(default=False)
	sort_order = models.IntegerField()
	slug = models.SlugField(unique=True)
	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ['sort_order']
	def __str__(self):
		return self.name

class Size(models.Model):
	name = models.CharField(max_length=64)
	sort_order = models.IntegerField()
	class Meta:
		ordering = ['sort_order']
	def __str__(self):
		return self.name

class MenuItem(models.Model):
	name = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	n_addons = models.IntegerField(default=0)
	is_special = models.BooleanField(default=False)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
	size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True, related_name='menu_items')
	sort_order = models.IntegerField()
	class Meta:
		ordering = ['sort_order']
	def __str__(self):
		return f'{self.category}: {self.name} - {self.price}'
	
class MenuItemAddon(models.Model):
	name = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	allowed_for = models.ManyToManyField(MenuItem, blank=True, related_name='allowed_addons')
	sort_order = models.IntegerField()
	class Meta:
		ordering = ['sort_order']
	def __str__(self):
		return self.name

class Address(models.Model):
	name = models.CharField(max_length=64)
	address1 = models.CharField(max_length=64)
	address2 = models.CharField(max_length=64)
	zip_code = models.CharField(max_length=64)
	city = models.CharField(max_length=64)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
	class Meta:
		verbose_name_plural = 'Addresses'
	def __str__(self):
		return f' {self.user}\'s address: {self.name} {self.address1} {self.address2} {self.zip_code} {self.city}'

ORDER_STATUS_CHOICES = [
	('Placed', 'Placed'),
	('Confirmed', 'Confirmed'),
	('Making', 'Making'),
	('Delivery', 'On the Way'),
	('Delivered', 'Delivered'),
	('Cancelled', 'Cancelled'),
]

PAYMENT_METHOD_CHOICES = [
	('CardOnline', 'Online by Card'),
	('CashOnDelivery', 'Cash on Delivery'),
	('CardOnDelivery', 'Card on Delivery'),
]

class Order(models.Model):
	status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='Placed')
	creation_datetime = models.DateTimeField(auto_now_add=True)
	payment_method = models.CharField(max_length=16, choices=PAYMENT_METHOD_CHOICES)
	notes = models.CharField(max_length=128, blank=True, null=True)
	delivery_estimate  = models.DateTimeField()
	delivery_address = models.ForeignKey(Address, on_delete=models.PROTECT)
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	@property
	def total_price(self):
		return sum(order_item.price for order_item in self.order_items.all())
	@property
	def is_paid(self):
		return self.payments.filter(status='Completed').exists()
	def __str__(self):
		return f'{self.customer}\'s order, total: {self.total_price}, \
		status: {self.status}, payment: {self.payment_method} (paid: {self.is_paid}), \
		created: {self.creation_datetime}'

class OrderItem(models.Model):
	menu_item = models.ForeignKey(MenuItem, on_delete = models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
	@property
	def price(self):
		return self.menu_item.price + sum(addon.menu_item_addon.price for addon in self.addons.all())	
	def __str__(self):
		return f'OrderItem: {self.menu_item}, order: {self.order}'

class OrderItemAddon(models.Model):
	menu_item_addon = models.ForeignKey(MenuItemAddon, on_delete=models.CASCADE)
	order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='addons')
	def __str__(self):
		return f'OrderItemAddon: {self.menu_item_addon}, \
		OrderItem: {self.order_item.menu_item.name}, price: {self.menu_item_addon.price}'

PAYMENT_STATUS_CHOICES = [
	('Pending', 'Pending'),
	('Completed', 'Completed'),
	('Cancelled', 'Cancelled'),
]

class Payment(models.Model):
	creation_datetime = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=16, choices=PAYMENT_STATUS_CHOICES, default='Pending')
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	stripe_id = models.CharField(max_length=64, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
	def __str__(self):
		return f'Payment: status: {self.status}, amount: {self.amount}, order: {self.order}'
