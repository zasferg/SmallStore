
from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('',cache_page(60)(Main.as_view()),name='main'),
    path('add_prod',AddProd.as_view(),name='add_product_page'),
    path('login',LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('account',UserPage.as_view(),name='account'),
    # path('account',show_user_page,name='account'),
    # path('basket',basket,name='basket'),
    path('registration', RegisterUser.as_view(), name='registration'),
    path('<slug:cat_slug>',ShowProduct.as_view(),name='show_prod'),
    path('detail/<slug:prod_slug>', ProdDetailed.as_view(), name='prod_detailed'),

    # path('<slug:cat_slug>/<slug:prod_slug>', prod_detailed, name='prod_detailed'),
]
#
#
