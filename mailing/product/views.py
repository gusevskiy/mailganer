from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MailingForm
from .tasks import order_created

def create_order(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save()
            # print('1/1', mailing.__dict__)
            order_created.apply_async(args=[mailing.id])
            return HttpResponse("Order created and email sent!")
    else:
        form = MailingForm()
    return render(request, 'includes/create_order.html', {'form': form})
