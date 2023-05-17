from django.contrib import admin

from main.models import User
from main.models import Order
from main.models import BaseRate
from main.models import CustomerRate
from main.models import ExecutorRate
from main.models import Application


def make_users_active(model_admin, request, queryset):
    queryset.update(is_active=True)


def make_users_inactive(model_admin, request, queryset):
    queryset.update(is_active=False)


make_users_active.short_description = 'Make selected active'
make_users_inactive.short_description = 'Make selected inactive'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    base_model = User
    fieldsets = [
        ('General', {
            'fields': [
                ('email', 'is_active'),
            ]
        }),
        ('Permissions', {
            'fields': [
                ('is_staff', 'is_superuser'),
                'groups',
                'user_permissions'
            ]
        }),
        ('Timings', {
            'fields': [
                'last_login',
                'date_joined'
            ]
        })
    ]
    actions = [make_users_active, make_users_inactive]
    save_on_top = True
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['email']
    filter_horizontal = ['groups', 'user_permissions']
    readonly_fields = ['date_joined']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    base_model = Order
    fieldsets = [
        ('General', {
            'fields': [
                ('customer', 'title', 'state'),
            ]
        }),
        ('Execution Data', {
            'fields': [
                'executor',
                'payment'
            ]
        }),
        ('Description', {
            'fields': [
                'description',
                'activity',
                'stack'
            ]
        })
    ]
    save_on_top = True
    list_display = ['state', 'customer', 'executor']
    list_filter = ['state']
    search_fields = ['customer']


class BaseRateAdmin(admin.ModelAdmin):
    base_model = BaseRate
    fieldsets = [
        ('General', {
            'fields': [
                ('author', 'user', 'order'),
            ]
        }),
        ('Comment', {
            'fields': [
                'comment'
            ]
        })
    ]
    save_on_top = True
    list_display = ['author', 'user', 'order']
    search_fields = ['author', 'user']


@admin.register(CustomerRate)
class CustomerRateAdmin(BaseRateAdmin):
    fieldsets = [
             ('Rates', {
                 'fields': [
                     'generosity',
                     'certainty',
                     'positivity',
                     'politeness'
                 ]
             }),
    ]
    fieldsets.insert(0, BaseRateAdmin.fieldsets[0])


@admin.register(ExecutorRate)
class ExecutorRateAdmin(BaseRateAdmin):
    fieldsets = [
             ('Rates', {
                 'fields': [
                     'speed',
                     'politeness',
                     'reliability',
                     'competence'
                 ]
             }),
    ]
    fieldsets.insert(0, BaseRateAdmin.fieldsets[0])


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    base_model = Application
    fieldsets = [
        ('General', {
            'fields': [
                ('receiver', 'state'),
            ]
        }),
        ('Description', {
            'fields': [
                ('author', 'comment')
            ]
        })
    ]
    save_on_top = True
    list_display = ['state', 'author', 'receiver']
    list_filter = ['state']
    search_fields = ['author', 'receiver']
