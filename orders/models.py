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

	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ['sort_order']
	
	def __str__(self):
		return f'{self.name}'

class Size(models.Model):
	name = models.CharField(max_length=64)
	sort_order = models.IntegerField()

	class Meta:
		ordering = ['sort_order']
	
	def __str__(self):
		return f'{self.name}'

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
		return f'{self.category}: {self.name} | {self.price}'
	

class MenuItemAddon(models.Model):
	name = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	allowed_for = models.ManyToManyField(MenuItem, blank=True, related_name='allowed_addons')
	sort_order = models.IntegerField()

	class Meta:
		ordering = ['sort_order']
	

	def __str__(self):
		return f'{self.name}'



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
	('Pending', 'Pending'),
	('Placed', 'Placed'),
	('Making', 'Making'),
	('Delivery', 'On the Way'),
	('Delivered', 'Delivered'),
	('Cancelled', 'Cancelled'),
]



class Order(models.Model):
	status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='Pending')
	creation_datetime = models.DateTimeField(auto_now_add=True)
	delivery_address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
	customer = models.ForeignKey(User, on_delete=models.CASCADE)

	@property
	def total_price(self):
		return sum(order_item.price for order_item in self.order_items.all())
	

	def __str__(self):
		return f'Order created at {self.creation_datetime} by customer {self.customer}.'


class OrderItem(StandardStrMixin, models.Model):
	menu_item = models.ForeignKey(MenuItem, on_delete = models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')

	@property
	def price(self):
		return self.menu_item.price + sum(addon.menu_item_addon.price for addon in self.addons.all())	

	# def __str__(self):
	# 	return f'OrderItem: {self.menu_item} | price: {self.price}'

class OrderItemAddon(StandardStrMixin, models.Model):
	menu_item_addon = models.ForeignKey(MenuItemAddon, on_delete=models.CASCADE)
	order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='addons')
	
	@property
	def price(self):
		return self.menu_item_addon.price

	@property
	def order(self):
		return self.order_item.order

	# def __str__(self):
	# 	return f'OrderItemAddon: {self.menu_item_addon}'


