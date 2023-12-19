from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .tasks import order_created

# Create your views here.

from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from basket.basket import Basket

@login_required()
def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST,user=request.user)
        if form.is_valid():
            order = form.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            basket.clear()
#            order_created.delay(order.id)
            return render(request, 'order_created.html',
                          {'order': order})
    else:
        form = OrderCreateForm(user=request.user)
    return render(request, 'order_create.html',
                  {'basket': basket, 'form': form})


