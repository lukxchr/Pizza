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