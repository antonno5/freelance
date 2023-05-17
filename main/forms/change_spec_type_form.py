from django import forms
from django.db.models import Choices

from main.models import BaseSpecType, ExecutorType, PrivateCustomerType, CorporateCustomerType


class ChangeSpecTypeForm(forms.Form):
    class SpecTypes(Choices):
        EXECUTOR = 1
        PRIVATE_CUSTOMER = 2
        CORPORATE_CUSTOMER = 3

        @classmethod
        def spec_type_to_value(cls, spec_type: BaseSpecType):
            if spec_type.is_executor():
                return cls.EXECUTOR
            elif spec_type.is_private_customer():
                return cls.PRIVATE_CUSTOMER
            elif spec_type.is_corporate_customer():
                return cls.CORPORATE_CUSTOMER

        @classmethod
        def value_to_spec_type(cls, value):
            value = cls(value)
            if value == cls.EXECUTOR:
                return ExecutorType
            elif value == cls.PRIVATE_CUSTOMER:
                return PrivateCustomerType
            elif value == cls.CORPORATE_CUSTOMER:
                return CorporateCustomerType

    spec_type = forms.ChoiceField(
        choices=SpecTypes.choices,
        label='Role',
    )
