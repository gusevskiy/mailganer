import pytz
import sys
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse

from product.models import MailingEmails
from .forms import MailingForm
from .tasks import order_created
from django.shortcuts import get_object_or_404

def create_order(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save()
            order_created.apply_async(args=[mailing.id])
            return HttpResponse("Order created and email sent!")
    else:
        form = MailingForm()
    return render(request, 'includes/create_order.html', {'form': form})


def track_email_open(request, tracking_id):
    mailing_log = get_object_or_404(MailingEmails, tracking_id=tracking_id)
    tz = pytz.timezone('UTC')
    mailing_log.is_opened = True
    mailing_log.opened_at  = datetime.now(tz)
    mailing_log.save()

    response = HttpResponse(content_type="image/png")
    response['Content-Disposition'] = 'inline; filename="tracking_pixel.png"'
    response.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x89\x67\x64\x39\x00\x00\x00\x0AIDAT8\x8D\x63\x60\x60\x60\x60\x60\x60\x60\x60\x60\x60\x60\x60\x60\x60\x60\x00\x00\x00\x00IEND\xaeB`\x82')
    print("Connect")
    return response