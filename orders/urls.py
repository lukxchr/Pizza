from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('menu/<int:category_id>', views.menu, name='menu'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
  	path('logout/', views.logout_view, name='logout'),
  	path('addToCart', views.add_to_cart, name='add_to_cart')
]


