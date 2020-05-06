from rest_framework import generics 
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

from orders.models import *
from .serializers import *

class MenuItemView(generics.ListAPIView):
	queryset = MenuItem.objects.all()
	serializer_class = MenuItemSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

	# def get_queryset(self):
	# 	queryset = MenuItem.objects.all()
	# 	filter_kwargs = {}
	# 	for field in self.serializer_class.Meta.fields:
	# 		value = self.request.query_params.get(field)
	# 		if value:
	# 			filter_kwargs[field] = value
	# 	return queryset.filter(**filter_kwargs)
		

# class MenuItemView(generics.ListCreateAPIView):
# 	queryset = MenuItem.objects.all()
# 	serializer_class = MenuItemSerializer

class DetailMenuItemView(generics.RetrieveAPIView):
	queryset = MenuItem.objects.all()
	serializer_class = MenuItemSerializer

# class DetailMenuItem(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = MenuItem.objects.all()
# 	serializer_class = MenuItemSerializer


class MenuItemAddonView(generics.ListAPIView):
	queryset = MenuItemAddon.objects.all()
	serializer_class = MenuItemAddonSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class DetailMenuItemAddonView(generics.RetrieveAPIView):
	queryset = MenuItemAddon.objects.all()
	serializer_class = MenuItemAddonSerializer


class CategoryView(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class DetailCategoryView(generics.RetrieveAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class SizeView(generics.ListAPIView):
	queryset = Size.objects.all()
	serializer_class = SizeSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class DetailSizeView(generics.RetrieveAPIView):
	queryset = Size.objects.all()
	serializer_class = SizeSerializer

class AddressView(generics.ListCreateAPIView):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer

class OrderView(generics.ListCreateAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer

class OrderItemView(generics.ListCreateAPIView):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer

class OrderItemAddonView(generics.ListCreateAPIView):
	queryset = OrderItemAddon.objects.all()
	serializer_class = OrderItemAddonSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class OrderItemAddonDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = OrderItemAddon.objects.all()
	serializer_class = OrderItemAddonSerializer