from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from model_utils.managers import InheritanceManager

from main.models import User


class PassportInfo(models.Model):
    passport_series = models.PositiveSmallIntegerField(
        _('passport series'),
        validators=[
            MaxValueValidator(9999),
            MinValueValidator(1000),
        ],
        null=True,
        blank=True,
    )

    passport_number = models.PositiveSmallIntegerField(
        _('passport number'),
        validators=[
            MaxValueValidator(999999),
            MinValueValidator(100000),
        ],
        null=True,
        blank=True,
    )

    passport_issue_date = models.DateField(
        _('passport issue date'),
        null=True,
        blank=True,
    )

    passport_issue_place = models.CharField(
        _('passport issue place'),
        null=True,
        max_length=100,
        blank=True,
    )


class BaseSpecType(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    person_prefix = ''

    first_name = models.CharField(
        _(person_prefix + 'first name'),
        max_length=30,
        blank=True,
    )

    last_name = models.CharField(
        _(person_prefix + 'last name'),
        max_length=150,
        blank=True,
    )

    phone_number = models.CharField(
        _(person_prefix + 'phone number'),
        max_length=20,
        blank=True,
    )

    objects = InheritanceManager()

    def get_down_class(self):
        return BaseSpecType.objects.get_subclass(pk=self.pk)

    @classmethod
    def change_spec_type(cls, user: User, new_spec_type_class):
        if isinstance(user.get_spec_type_object(), new_spec_type_class):
            return
        user.get_spec_type_object().delete()
        new_spec_type_class(user=user).save()


    @staticmethod
    def is_executor() -> bool:
        return False

    @staticmethod
    def is_customer() -> bool:
        return False

    @staticmethod
    def is_private_customer() -> bool:
        return False

    @staticmethod
    def is_corporate_customer() -> bool:
        return False


class ExecutorType(BaseSpecType, PassportInfo):
    activity = models.CharField(
        _('activity'),
        blank=True,
        max_length=100,
    )

    resume = models.TextField(
        _('resume'),
        max_length=3000,
        blank=True,
    )

    def accept_application(self, application: 'Application') -> None:
        if application.receiver != self:
            raise RuntimeError('You can\'t accept not your application')
        application.accept()

    def decline_application(self, application: 'Application') -> None:
        if application.receiver != self:
            raise RuntimeError('You can\'t decline not your application')
        application.decline()

    def delete_rate(self, rate: 'ExecutorRate') -> None:
        if rate.author != self:
            raise RuntimeError('You can\'t delete not your rate')
        rate.delete()

    def delete_application(self, application: 'Application') -> None:
        if application.receiver != self:
            raise RuntimeError('You can\'t delete not your application')
        application.delete()

    @staticmethod
    def is_executor() -> bool:
        return True


class CustomerType(BaseSpecType):
    def cancel_order(self, order: 'Order') -> None:
        if order.customer != self:
            raise RuntimeError('You can\'t cancel not your order')
        order.cancel()

    def finish_order(self, order: 'Order') -> None:
        if order.customer != self:
            raise RuntimeError('You can\'t finish not your order')
        order.finish()

    def assign_executor(self, order: 'Order', executor: ExecutorType) -> None:
        if order.customer != self:
            raise RuntimeError('You can\'t assign executor in not your order')
        order.assign_executor(executor)

    def remove_executor(self, order: 'Order') -> None:
        if order.customer != self:
            raise RuntimeError('You can\'t remove executor in not your order')
        order.remove_executor()

    def delete_order(self, order: 'Order') -> None:
        if order.customer != self:
            raise RuntimeError('You can\'t delete not your order')
        order.delete()

    def delete_rate(self, rate: 'CustomerRate') -> None:
        if rate.author != self:
            raise RuntimeError('You can\'t delete not your rate')
        rate.delete()

    def accept_application(self, application: 'Application') -> None:
        if application.author != self:
            raise RuntimeError('You can\'t accept not your application')
        application.accept()

    def decline_application(self, application: 'Application') -> None:
        if application.receiver != self:
            raise RuntimeError('You can\'t decline not your application')
        application.decline()

    def delete_application(self, application: 'Application') -> None:
        if application.receiver != self:
            raise RuntimeError('You can\'t delete not your application')
        application.delete()

    @staticmethod
    def is_customer() -> bool:
        return True


class PrivateCustomerType(CustomerType, PassportInfo):
    @staticmethod
    def is_private_customer() -> bool:
        return True


class CorporateCustomerType(CustomerType):
    person_prefix = 'contact person'

    company_name = models.CharField(
        _('company name'),
        max_length=100,
        blank=False,
    )

    creation_date = models.DateField(
        _('company creation date'),
        blank=True,
        null=True,
    )

    registration_number = models.CharField(
        _('registration number'),
        max_length=100,
        blank=True,
    )

    @staticmethod
    def is_corporate_customer() -> bool:
        return True
