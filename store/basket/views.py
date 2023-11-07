from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from storeapp.models import Product
from .basket import Basket
from .forms import BasketAddProductForm

# Create your views here.

@require_POST
def basket_add(request,prod_slug):
    basket = Basket(request)
    product = get_object_or_404(Product,slug= prod_slug)
    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        quantity_data = form.cleaned_data['quantity']
        update_quantity_data = form.cleaned_data['update']
        # cd = form.cleaned_data()
        basket.add(product,quantity_data,update_quantity_data)
    return redirect('basket_detail')


def basket_remove(request,prod_slug):
    basket = Basket(request)
    product = get_object_or_404(Product,slug=prod_slug)
    basket.remove(product)
    return redirect('basket_detail')


def basket_detail(request):
    basket = Basket(request)
    bp_form = BasketAddProductForm()
    return render(request,'basket.html',{'bp_form':bp_form,'basket':basket})