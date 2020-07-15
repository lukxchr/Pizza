from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('menu/<slug:slug>', views.menu, name='menu'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('addresses/new/', views.AddressCreateView.as_view(), name='create_address'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/place-order/', views.PlaceOrderView.as_view(), name='place_order'),
    path('orders/<int:pk>', views.track_order, name='track_order'),
    path('get-cart', views.cart, name='get_cart'),
    path('remove-cart-item', views.remove_from_cart, name='remove_from_cart'),
    path('order-payment/<int:pk>', views.order_payment, name='order_payment'),
    path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
]
