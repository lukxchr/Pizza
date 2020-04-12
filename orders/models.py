from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
	name = models.CharField(max_length=64)

	class Meta:
		verbose_name_plural = 'Categories'
	
	def __str__(self):
		return f'{self.name}'

class Size(models.Model):
	name = models.CharField(max_length=64)
	
	def __str__(self):
		return f'{self.name}'

class MenuItem(models.Model):
	name = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	n_addons = models.IntegerField(default=0)
	is_special = models.BooleanField(default=False)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
	size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True, related_name='menu_items')

	def __str__(self):
		return f'{self.category}: {self.name} | {self.price}'
	

class MenuItemAddon(models.Model):
	name = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	allowed_for = models.ManyToManyField(MenuItem, blank=True, related_name='allowed_addons')
	

	def __str__(self):
		return f'{self.name}'




# SIZE_CHOICES = [
# 	('S', 'Small'),
# 	('L', 'Large'),
# ]

# PIZZA_CRUST_CHOICES = [
# 	('Regular', 'Regular'),
# 	('Sicilian', 'Sicilian'),
# ]

# MENU_ITEM_CATEGORY_CHOICES = [
# 	('Sub', 'Sub'),
# 	('SubExtra', 'SubExtra'),
# 	('Salad', 'Salad'),
# 	('Pasta', 'Pasta'),
# 	('Platter', 'DinnerPlatter'),
# ]

# ORDER_STATUS_CHOICES = [
# 	('Pending', 'Pending'),
# 	('Placed', 'Placed'),
# 	('Making', 'Making'),
# 	('Delivery', 'On the Way'),
# 	('Delivered', 'Delivered'),
# 	('Cancelled', 'Cancelled'),
# ]

# class Pizza(models.Model):
# 	crust = models.CharField(max_length=8, choices=PIZZA_CRUST_CHOICES, default='Regular')
# 	size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='L')
# 	n_toppings = models.IntegerField(default=0)
# 	is_special = models.BooleanField(default=False)
# 	price = models.DecimalField(max_digits=5, decimal_places=2)

# 	def __str__(self):
# 		return f'Pizza: {self.crust} | {self.size} | {self.n_toppings} | Special: {self.is_special} | {self.price}'

# class PizzaTopping(models.Model):
# 	name = models.CharField(max_length=64)

# 	def __str__(self):
# 		return f'Pizza Topping: {self.name}'

# class StandardMenuItem(models.Model):
# 	category = models.CharField(max_length=15, choices=MENU_ITEM_CATEGORY_CHOICES, default='Sub')
# 	name = models.CharField(max_length=64)
# 	size = models.CharField(max_length=1, choices=SIZE_CHOICES, blank=True)
# 	price = models.DecimalField(max_digits=5, decimal_places=2)

# 	def __str__(self):
# 		return f'{self.category}: {self.name} | {self.size} | {self.price}'

# class Extra(models.Model):
# 	name = models.CharField(max_length=64)
# 	price = models.DecimalField(max_digits=5, decimal_places=2)
# 	def __str__(self):
# 		return f'{self.category}: {self.name} | {self.price}'


# class Order(models.Model):
# 	status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='Pending')
# 	customer = models.ForeignKey(User, on_delete=models.CASCADE)

# 	@property
# 	def items(self):
# 		return {'pizzas' : self.pizzas, 'other_items': self.standard_items}

# 	@property
# 	def total_price(self):
# 		return sum(item.price for item in self.items) + sum(pizza.menu_pizza.price for pizza in self.pizzas)

# class OrderPizza(models.Model):
# 	menu_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
# 	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pizzas')

# class OrderPizzaTopping(models.Model):
# 	menu_topping = models.ForeignKey(PizzaTopping, on_delete=models.CASCADE)
# 	order_pizza = models.ForeignKey(OrderPizza, on_delete=models.CASCADE, related_name='toppings')

# class StandardOrderItem(models.Model):
# 	menu_item = models.ForeignKey(StandardMenuItem, on_delete=models.CASCADE)
# 	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='standard_items')

# 	@property
# 	def price(self):
# 		return self.menu_item.price + sum(e.menu_extra.price for e in self.extras)
	
# class OrderExtra(models.Model):
# 	menu_extra = models.ForeignKey(Extra, on_delete=models.CASCADE)
# 	order_item = models.ForeignKey(StandardOrderItem, on_delete=models.CASCADE, related_name='extras')