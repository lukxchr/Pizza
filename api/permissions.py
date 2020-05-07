from rest_framework import permissions

class IsAddressUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.user == request.user

class IsOrderCustomer(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.customer == request.user


