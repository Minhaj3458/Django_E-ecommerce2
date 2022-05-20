from django.urls import path
from .import views
urlpatterns = [
path('user_logout', views.user_logout, name="user_logout"),
path('user_login', views.user_login, name="user_login"),
path('user_register', views.user_register, name="user_register"),
path('userprofile', views.userprofile, name="userprofile"),
path('user_update', views.user_update, name="user_update"),
path('user_password', views.user_password, name="user_password"),
path('usercomment', views.usercomment, name="usercomment"),
path('comment_delete/<int:id>/', views.comment_delete, name="comment_delete"),
]
