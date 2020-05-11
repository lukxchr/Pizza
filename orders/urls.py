from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('menu/<int:category_id>', views.menu, name='menu'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
  	path('logout/', views.logout_view, name='logout'),
  	path('addToCart', views.add_to_cart, name='add_to_cart'),
  	path('addresses/add', views.AddressCreateView.as_view(), name='create_address'),
  	path('orders/place_order', views.update_order, name='update_order'),
  	path('orders/<int:pk>', views.track_order, name='track_order'),
]


