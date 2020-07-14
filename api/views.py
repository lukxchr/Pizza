from rest_framework import generics

from orders.models import MenuItem, MenuItemAddon, Category, Size, Address, \
                          Order, OrderItem, OrderItemAddon
from .permissions import IsAddressUser, IsOrderCustomer, IsOrderItemCustomer, \
                         IsOrderItemAddonCustomer
from .serializers import MenuItemSerializer, MenuItemAddonSerializer, \
                         CategorySerializer, SizeSerializer, AddressSerializer, \
                         OrderItemAddonSerializer, OrderItemSerializer, \
                         OrderSerializer, OrderDetailSerializer

class MenuItemView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    #enable filtering by any exposed field
    filterset_fields = serializer_class.Meta.fields


class DetailMenuItemView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


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
    permission_classes = (IsAddressUser,)
    serializer_class = AddressSerializer
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAddressUser,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class OrderView(generics.ListCreateAPIView):
    permission_classes = (IsOrderCustomer,)
    serializer_class = OrderSerializer
    filterset_fields = ['id', 'status', 'creation_datetime',
                        'delivery_address', 'customer']

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsOrderCustomer,)
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer


class CreateOrderItemView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer


class OrderItemDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsOrderItemCustomer,)
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CreateOrderItemAddonView(generics.CreateAPIView):
    serializer_class = OrderItemAddonSerializer


class OrderItemAddonDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsOrderItemAddonCustomer,)
    queryset = OrderItemAddon.objects.all()
    serializer_class = OrderItemAddonSerializer
