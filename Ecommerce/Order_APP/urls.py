from django.urls import path
from .import views
urlpatterns = [
  path('Add_to_Shoping_cart/<int:id>', views.Add_to_Shoping_cart, name="Add_to_Shoping_cart"),
  path('Cart_details', views.Cart_details, name="Cart_details"),
  path('cart_delete/<int:id>', views.cart_delete, name="cart_delete"),
  path('OrderCart', views.OrderCart, name="OrderCart"),
  path('Order_showing', views.Order_showing, name="Order_showing"),
  path('Order_Product_showing', views.Order_Product_showing, name="Order_Product_showing"),
  path('user_oder_details/<int:id>', views.user_oder_details, name="user_oder_details"),
  path('useroderproduct_details/<int:id>/<int:oid>/', views.useroderproduct_details, name="useroderproduct_details"),
]