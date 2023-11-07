from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug','description','price','time_add','time_update','is_available']
    list_display_links = ['title','id']
    list_editable = ['is_available']
    ordering = ['-time_add']
    list_per_page = 10


@admin.register(Category)
class CategoryAadmin(admin.ModelAdmin):
    list_display = ['id','name','slug']
    list_display_links = ['id','name']





