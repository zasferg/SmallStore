from django.contrib.auth.models import User
from django.db import models,migrations

# Create your models here.
from django.urls import reverse


class Product(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Нет в наличии'
        PUBLISHED = 1, 'В наличии'


    title = models.CharField(max_length=255,verbose_name='Название товара')
    slug = models.SlugField(max_length=255,db_index=True,unique=True,verbose_name="URL")
    description= models.TextField(blank=True,verbose_name="Описание товара")
    price = models.FloatField(verbose_name="Цена")
    time_add = models.DateTimeField(auto_now_add=True,verbose_name="Добавлено")
    time_update = models.DateTimeField(auto_now=True,verbose_name="Обновлено")
    is_available = models.BooleanField(choices=Status.choices,default=Status.DRAFT,verbose_name="В наличии")
    photo = models.ImageField(upload_to="images/",verbose_name="Фото")
    cat = models.ForeignKey('Category',on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        ordering = ['-time_add']

    def get_absolute_url(self):
        return reverse('prod_detailed',kwargs={'prod_slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100,db_index=True,verbose_name="Название категории")
    slug = models.SlugField(unique=True,db_index=True,max_length=255,verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категории товаров"
        verbose_name_plural = "Категории товаров"


    def get_absolute_url(self):
        return reverse('show_prod',kwargs={'cat_slug': self.slug})

