from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, CreateView
from basket.forms import BasketAddProductForm
from orders.models import OrderItem,Order
from .utils  import *
from django.views.generic import ListView
from braces.views import GroupRequiredMixin
from storeapp.models import *
from .forms import *




# Create your views here.

class Main(DataMixin,ListView):
    model = Product
    template_name = 'html/product.html'
    context_object_name = 'prods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главное меню')
        return dict(list(context.items()) + list(c_def.items()))




class ShowProduct(DataMixin,ListView):
    model = Product
    template_name = 'html/product.html'
    context_object_name = 'prods'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["prods"])
        return dict(list(context.items()) + list(c_def.items()))



class ProdDetailed(DataMixin,ListView):
    model = Product
    template_name = 'html/detailed.html'
    context_object_name = 'product'
    slug_url_kwarg = 'prod_slug'

    def get_queryset(self):
        return Product.objects.get(slug=self.kwargs['prod_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(form = BasketAddProductForm())
        return dict(list(context.items()) + list(c_def.items()))
        return context


class AddProd(LoginRequiredMixin,GroupRequiredMixin, DataMixin,CreateView):
    form_class = ProductAddForm
    template_name = 'html/add_prod.html'
    group_required = u'moderators'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Добавление товара')
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin,LoginView):
    form_class = LoginForm
    template_name = 'html/login_user.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('account')


def logout_user(request):
    logout(request)
    return redirect('/')

class RegisterUser(DataMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'html/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('registration')


class UserPage(DataMixin,LoginRequiredMixin,ListView):
    model = OrderItem
    template_name = 'html/user_account.html'
    context_object_name = 'order_item'
    login_url = 'login'
    def get_queryset(self,):
        return OrderItem.objects.filter(order__email=self.request.user.email).select_related('order','product')


    def get_context_data(self,*, object_list=None, **kwargs):
        context= super().get_context_data()
        c_def = self.get_user_context(order=Order.objects.filter(email=self.request.user.email),
                                      title=f'Личная страница {self.request.user.username}')
        return dict(list(context.items()) + list(c_def.items()))
# @login_required(login_url='login')
# def show_user_page(request):
#         order_item=OrderItem.objects.filter(order__email=request.user.email).select_related('order','product')
#         order= Order.objects.filter(email=request.user.email)
#         context = {
#             'order':order,
#             'user_name':request.user.username,
#             'order_item':order_item,
#             'title': f'Личная страница {request.user.username}',
#             'menu': main_menu,
#             'menu_right': main_menu_right,
#         }
#
#         return render(request,'html/user_account.html',context=context)


#
# def main(request):
#     prod = Product.objects.all()
#     content = {
#         'title': 'Категории',
#         'menu': main_menu,
#         'menu_right': main_menu_right,
#         'prods': prod,
#     }
#
#     return render(request,'html/product.html',context=content)


# def show_prod(request,cat_slug):
#     category = get_object_or_404(Category,slug=cat_slug)
#     prod = Product.objects.filter(cat__slug=cat_slug)
#     content = {
#         'title': f'Категория: {category.name}',
#         'menu': main_menu,
#         'menu_right': main_menu_right,
#         # 'db_cat': db_cat,
#         'prods': prod,
#         # 'cat_selected':category.pk
#     }
#
#     return render(request,'html/product.html',context=content)

# def prod_detailed(request,prod_slug):
#     product = get_object_or_404(Product, slug=prod_slug)
#     basket_product_form = BasketAddProductForm()
#     context = {
#         'basket_product_form':basket_product_form,
#         'menu': main_menu,
#         'menu_right': main_menu_right,
#         'product': product
#     }
#
#     return render(request,'html/detailed.html',context=context)

# def basket(request):
#      return HttpResponse('basket page')/



# def add_prod(request):
#
#     if request.method == 'POST':
#         form = ProductAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = ProductAddForm()
#     context = {
#         'form':form,
#         'title': 'Добавление товара',
#         'menu': main_menu,
#         'menu_right': main_menu_right,
#     }
#     return render(request,'html/add_prod.html',context=context)

#
# def login_user(request):
#     if request.method =="POST":
#         log_form = LoginForm(request.POST)
#         if log_form.is_valid():
#             cd = log_form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('/')
#     else:
#         log_form = LoginForm()
#
# def registration(request):
#     if request.method == 'POST':
#         reg_form = RegistrationForm(request.POST)
#         if reg_form.is_valid():
#             user = reg_form.save()
#             user.username = user.username.lower()
#             user.save()
#             # messages.success(request, 'You have singed up successfully.')
#             login(request, user)
#             return redirect('/')
#     else:
#         reg_form = RegistrationForm()
#
#     context = {
#         'reg_form':reg_form,
#         'title': 'Регистрация',
#         'menu': main_menu,
#         'menu_right': main_menu_right,
#     }
#
#
#     return render(request,'html/registration.html',context=context)
#
