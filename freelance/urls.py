"""freelance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.modules.pages.application_accept import ApplicationAcceptModule
from main.modules.pages.application_create import ApplicationCreateModule
from main.modules.pages.application_decline import ApplicationDeclineModule
from main.modules.pages.application_delete_page import ApplicationDeleteModule
from main.modules.pages.application_edit_page import ApplicationEditModule
from main.modules.pages.application_finish_page import ApplicationFinishModule
from main.modules.pages.change_spec_type_module import ChangeSpecTypePageModule
from main.modules.pages.index_module import IndexPageModule
from main.modules.pages.order_delete_page import OrderDeleteModule
from main.modules.pages.order_edit_page import OrderEditModule
from main.modules.pages.order_market_page import OrderMarketModule
from main.modules.pages.order_create_page import OrderCreateModule
from django.contrib.auth import views as auth_views
from main.modules.pages.profile_edit_module import ProfileEditPageModule
from main.modules.pages.profile_module import ProfilePageModule
from main.modules.pages.rate_delete_page import RateDeleteModule
from main.modules.pages.rate_edit_page import RateEditModule
from main.modules.pages.rate_page import RatePageModule
from main.modules.pages.registration_module import RegistrationPageModule
from main.modules.pages.your_applications_page import ApplicationListModule
from main.modules.pages.your_orders_page import OrderListModule
from main.modules.pages.your_rates_page import RatesListModule
from main.views import order_view, application_view, rate_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPageModule.as_view(), name='index'),
    path('order/create/', OrderCreateModule.as_view(), name='order_create'),
    path('order_market/', OrderMarketModule.as_view(), name='order_market'),
    path(
        'profile/login/',
        auth_views.LoginView.as_view(
            extra_context={
                'head_page_name': 'Login'
            },
            template_name='auth/login.html',
        ),
        name='login'
    ),
    path('profile/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/password-change', auth_views.PasswordChangeView.as_view(
        extra_context={
            'head_page_name': 'Password change',
        },
        template_name='pages/password_change.html',
    ), name='password_change'),
    path('profile/registration/', RegistrationPageModule.as_view(), name='registration'),
    path('your_orders/', OrderListModule.as_view(), name='your_orders'),
    path('order/edit/<int:order_id>/', OrderEditModule.as_view(), name='order_edit'),
    path('order/delete/<int:order_id>/', OrderDeleteModule.as_view(), name='order_delete'),
    path('profile/<int:user_id>', ProfilePageModule.as_view(), name='profile'),
    path('profile/edit/', ProfileEditPageModule.as_view(), name='profile_edit'),
    path('order/<int:order_id>/', order_view, name='order'),
    path('profile/change-role/', ChangeSpecTypePageModule.as_view(), name='change_spec_type'),
    path('application/create/<int:order_id>/', ApplicationCreateModule.as_view(), name='application_create'),
    path('your_applications/', ApplicationListModule.as_view(), name='your_applications'),
    path('application/<int:application_id>/', application_view, name='application'),
    path('application/edit/<int:application_id>/', ApplicationEditModule.as_view(), name='application_edit'),
    path('application/delete/<int:application_id>/', ApplicationDeleteModule.as_view(), name='application_delete'),
    path('application/accept/<int:application_id>/', ApplicationAcceptModule.as_view(), name='application_accept'),
    path('application/decline/<int:application_id>/', ApplicationDeclineModule.as_view(), name='application_decline'),
    path('application/finish/<int:application_id>/', ApplicationFinishModule.as_view(), name='application_finish'),
    path('order/<int:order_id>/rate/', RatePageModule.as_view(), name='order_rate'),
    path('rate/<int:rate_id>/', rate_view, name='rate'),
    path('rate/edit/<int:rate_id>/', RateEditModule.as_view(), name='rate_edit'),
    path('rate/delete/<int:rate_id>/', RateDeleteModule.as_view(), name='rate_delete'),
    path('your_rates/', RatesListModule.as_view(), name='your_rates'),
]
