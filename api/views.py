from rest_framework import generics 
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

from orders.models import *
from .permissions import IsAddressUser, IsOrderCustomer
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

#delete? or add permission
class AddressView(generics.ListCreateAPIView):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer
	#enable filtering by any exposed field
	filterset_fields = serializer_class.Meta.fields

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAddressUser,)
	queryset = Address.objects.all()
	serializer_class = AddressSerializer

class OrderView(generics.ListCreateAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	filterset_fields = ['id', 'status', 'creation_datetime', 'delivery_address', 'customer']

class OrderDetailView(generics.RetrieveDestroyAPIView):
	permission_classes = (IsOrderCustomer,)
	queryset = Order.objects.all()
	serializer_class = OrderDetailSerializer

class OrderItemView(generics.ListCreateAPIView):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
	filterset_fields = ['id', 'menu_item', 'order']

class OrderItemDetailView(generics.RetrieveDestroyAPIView):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer

class OrderItemAddonView(generics.ListCreateAPIView):
	queryset = OrderItemAddon.objects.all()
	serializer_class = OrderItemAddonSerializer
	filterset_fields = ['id', 'menu_item_addon', 'order_item',]

class OrderItemAddonDetailView(generics.RetrieveDestroyAPIView):
	queryset = OrderItemAddon.objects.all()
	serializer_class = OrderItemAddonSerializer