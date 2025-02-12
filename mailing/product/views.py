from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import OrderForm
from .tasks import order_created

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order_created.apply_async(args=[order.id])
            return HttpResponse("Order created and email sent!")
    else:
        form = OrderForm()
    return render(request, 'includes/create_order.html', {'form': form})
