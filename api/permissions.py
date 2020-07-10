from rest_framework import permissions

class IsAddressUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.user == request.user

class IsOrderCustomer(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.customer == request.user

class IsOrderItemCustomer(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.order.customer == request.user

class IsOrderItemAddonCustomer(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.order_item.order.customer == request.user