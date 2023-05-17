from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect

from main.models import ExecutorType, PrivateCustomerType, CorporateCustomerType


def type_check(function, check_cls_list, redirect_url='index', error_message=None):
    @login_required()
    @wraps(function)
    def wrap(request: HttpRequest, *args, **kwargs):
        is_ok = False
        for cls in check_cls_list:
            if isinstance(request.user.get_spec_type_object(), cls):
                is_ok = True
                break

        if is_ok:
            return function(request, *args, **kwargs)
        else:
            if error_message is not None:
                messages.add_message(request, messages.ERROR, error_message)
            return redirect(redirect_url)

    return wrap


def executor_only(function, redirect_url='index', error_message='You are not executor'):
    return type_check(function, [ExecutorType],
                      redirect_url=redirect_url, error_message=error_message)


def private_customer_only(function, redirect_url='index', error_message='You are not private customer'):
    return type_check(function, [PrivateCustomerType],
                      redirect_url=redirect_url, error_message=error_message)


def corporate_customer_only(function, redirect_url='index', error_message='You are not corporate customer'):
    return type_check(function, [CorporateCustomerType],
                      redirect_url=redirect_url, error_message=error_message)


def customer_only(function, redirect_url='index', error_message='You are not customer'):
    return type_check(function, [PrivateCustomerType, CorporateCustomerType],
                      redirect_url=redirect_url, error_message=error_message)
