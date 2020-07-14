from rest_framework import serializers

from orders.models import MenuItem, MenuItemAddon, Category, Size, Address, \
                          Order, OrderItem, OrderItemAddon


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

    def validate(self, data):
        if data['user'] != self.context['request'].user:
            raise serializers.ValidationError(
                'You are not allowed to create address for this user.')
        return data


class OrderItemAddonSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItemAddon
        fields = ['id', 'menu_item_addon', 'order_item', 'price']

    def validate(self, data):
        if data['order_item'].order.customer != self.context['request'].user:
            raise serializers.ValidationError(
                'You are not allowed to create order item addon for this order item.')
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'order', 'price']

    def validate(self, data):
        if data['order'].customer != self.context['request'].user:
            raise serializers.ValidationError(
                'You are not allowed to create order item for this order.')
        return data


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = ['id', 'status', 'creation_datetime', 'delivery_address',
                  'customer', 'total_price']

    def validate(self, data):
        user = self.context['request'].user
        if data['customer'] != user:
            raise serializers.ValidationError(
                'You are not allowed to create order for this user.')
        elif data['delivery_address'].user != user:
            raise serializers.ValidationError(
                'You are not allowed to create order for this address.')
        return data


#serializers used by OrderDetailSerializer to represent nested objects
class CategoryBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class MenuItemBasicSerializer(serializers.ModelSerializer):
    category = CategoryBasicSerializer()
    size = SizeSerializer()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'category', 'size', 'price']


class MenuItemAddonBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemAddon
        fields = ['id', 'name', 'price']


class OrderItemAddonBasicSerializer(serializers.ModelSerializer):
    menu_item_addon = MenuItemAddonBasicSerializer()

    class Meta:
        model = OrderItemAddon
        fields = ['id', 'menu_item_addon']


class OrderItemDetailSerializer(serializers.ModelSerializer):
    addons = OrderItemAddonBasicSerializer(many=True)
    menu_item = MenuItemBasicSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'order', 'price', 'addons']


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemDetailSerializer(many=True)
     
    class Meta:
        model = Order
        fields = ['id', 'status', 'creation_datetime', 'notes', 'payment_method',
                  'is_paid', 'delivery_estimate', 'delivery_address', 'customer',
                  'total_price', 'order_items']
        read_only_fields = ['order_items']
