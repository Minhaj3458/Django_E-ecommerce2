from django.urls import path
from .import views
urlpatterns = [
   path('Comment_Add/<int:id>', views.Comment_Add, name="Comment_Add"),
]
