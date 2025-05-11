from functools import wraps
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from rest_framework.decorators import api_view
from .models import Order
# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')

def check_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.POST.get('token')
        if token != ACCEPTED_TOKEN:
            return HttpResponseBadRequest("Invalid token")
        return view_func(request, *args, **kwargs)
    return wrapper


@api_view(['POST'])
@check_token
def import_order(request):
    order_number = request.POST.get('order_number')
    total_price = request.POST.get('total_price')

    if not order_number or not total_price:
        return HttpResponseBadRequest("Missing order_number or total_price")    
    
    try:
        total_price = float(total_price)
    except ValueError:
        return HttpResponseBadRequest("Invalid total_price format")
    
    try:
        Order.objects.create(
            order_number=order_number,
            total_price=total_price,
            created_time=timezone.now()
        )
    except Exception as e:
        return HttpResponseBadRequest(f"Failed to create order: {str(e)}")

    return HttpResponse("Order created successfully", status=201)