from .views import *
from django.urls import path


urlpatterns = [
    path('',basket_detail,name='basket_detail'),
    path('add/<slug:prod_slug>',basket_add,name='basket_add'),
    path('remove/<slug:prod_slug>',basket_remove,name='basket_remove')

]