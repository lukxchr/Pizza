from django.urls import path

from .views import *

urlpatterns = [
	path('menu_items/', MenuItemView.as_view()),
	path('menu_items/<int:pk>', DetailMenuItemView.as_view()),
	path('menu_item_addons/', MenuItemAddonView.as_view()),
	path('menu_item_addons/<int:pk>', DetailMenuItemAddonView.as_view()),
	path('categories/', CategoryView.as_view()),
	path('categories/<int:pk>', DetailCategoryView.as_view()),
	path('sizes/', SizeView.as_view()),
	path('sizes/<int:pk>', DetailSizeView.as_view()),
	path('addresses/', AddressView.as_view()),
	path('addresses/<int:pk>', AddressDetailView.as_view()),
	path('orders/', OrderView.as_view()),
	path('orders/<int:pk>', OrderDetailView.as_view()),
	path('order_items/', OrderItemView.as_view()),
	path('order_items/<int:pk>', OrderItemDetailView.as_view()),
	path('order_item_addons/', OrderItemAddonView.as_view()),
	path('order_item_addons/<int:pk>', OrderItemAddonDetailView.as_view()),
]