
from django.urls import path
from .import views
urlpatterns = [
    path('common/', views.common, name="common"),
    path('', views.home, name="home"),
    path('single_product/<id>', views.single_product, name="single_product"),
    path('category_product/<int:id>/<slug:slug>/', views.category_product, name="category_product"),
    path('contact_page', views.contact_page, name="contact_page"),
    path('searchView/', views.searchView, name="searchView"),

]
