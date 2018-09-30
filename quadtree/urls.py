from . import views
from django.urls import path

urlpatterns = [
    path('index', views.index, name ='index'),
    path('create_random_user/<int:count>', views.create_random_user, name ='index'),
    path('clear_cache', views.clear_cache, name ='index'),
]
