from django.urls import path
from . import views


urlpatterns = [
    path('', views.order_create, name='order_created'),
    path('create', views.order_create, name='order_create'),
]