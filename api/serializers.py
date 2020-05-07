from rest_framework import serializers

from orders.models import *

class MenuItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = MenuItem
		fields = ['id', 'name', 'price', 'n_addons', 'is_special', 
			'category', 'size', 'sort_order', 'allowed_addons']

class MenuItemAddonSerializer(serializers.ModelSerializer):
	class Meta:
		model = MenuItemAddon
		fields = ['id', 'name', 'price', 'allowed_for', 'sort_order']

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'is_pizza_category', 'sort_order']

class SizeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Size 
		fields = ['id', 'name']

class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'name', 'address1', 'address2', 'zip_code', 'city', 'user']


class OrderItemAddonSerializer(serializers.ModelSerializer):
	price = serializers.ReadOnlyField()
	class Meta:
		model = OrderItemAddon
		fields = ['id', 'menu_item_addon', 'order_item', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
	price = serializers.ReadOnlyField()
	class Meta:
		model = OrderItem
		fields = ['id', 'menu_item', 'order', 'price']

class OrderSerializer(serializers.ModelSerializer):
	total_price = serializers.ReadOnlyField()
	class Meta:
		model = Order 
		fields = ['id', 'status', 'creation_datetime', 'delivery_address', 'customer', 'total_price']
	def validate(self, data):
		if data['status'] == 'Pending' and Order.objects.filter(customer=data['customer'], status='Pending').exists():
			raise serializers.ValidationError('Pending order already exists for this customer.')
		return data 

