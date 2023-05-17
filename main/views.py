from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from typing import Dict, List, Type

from django.shortcuts import render

from main.models import Order, Application, BaseRate, ExecutorRate, CustomerRate


def order_view(request: HttpRequest, order_id):
    #process_logic
    context: Dict = {}
    order = Order.objects.get(pk=order_id)
    try:
        application = Application.objects.get(order=order, state=Application.AppStates.ACCEPTED)
    except Application.DoesNotExist:
        application = None
        pass
    #process_context
    context['order'] = order
    context['application'] = application
    #process_view
    return render(request, "pages/order_view.html", context)

def application_view(request:HttpRequest, application_id):
    # process_logic
    context: Dict = {}
    application = Application.objects.get(pk=application_id)
    # process_context
    context['application'] = application
    # process_view
    return render(request, "pages/application_view.html", context)

def rate_view(request:HttpRequest, rate_id):
    # process_logic
    context: Dict = {}
    rate = None
    try:
        rate = ExecutorRate.objects.get(baserate_ptr_id=rate_id)
    except ExecutorRate.DoesNotExist:
        pass
    try:
        rate = CustomerRate.objects.get(baserate_ptr_id=rate_id)
    except CustomerRate.DoesNotExist:
        pass
    # process_context
    context['rate'] = rate
    # process_view
    return render(request, "pages/rate_view.html", context)
