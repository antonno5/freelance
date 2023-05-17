from django.db import models

from main.models import User
from main.models.SpecTypes import CustomerType, ExecutorType


class Order(models.Model):
    title = models.CharField(
        max_length=32
    )

    activity = models.CharField(
        max_length=100
    )

    description = models.TextField(
        max_length=1024
    )

    stack = models.CharField(
        max_length=15
    )

    payment = models.PositiveIntegerField()

    customer = models.ForeignKey(
        to=CustomerType,
        on_delete=models.CASCADE
    )

    executor = models.ForeignKey(
        to=ExecutorType,
        null=True,
        on_delete=models.CASCADE
    )

    class OrderStates(models.IntegerChoices):
        OPEN = 1
        RUNNING = 2
        CLOSED = 3
        CANCELED = 4

    state = models.IntegerField(
        choices=OrderStates.choices,
        default=OrderStates.OPEN
    )

    def assign_executor(self, executor: ExecutorType) -> None:
        if self.state != self.OrderStates.OPEN or self.executor:
            cause = ""
            if self.state == self.OrderStates.CLOSED:
                cause = "your order is closed"
            if self.state == self.OrderStates.CANCELED:
                cause = "your order is canceled"
            if self.executor:
                cause = "your order has executor"
            raise RuntimeError('You can\'t assign executor because {}'.format(cause))
        self.executor = executor
        self.state = self.OrderStates.RUNNING
        self.save()

    def remove_executor(self) -> None:
        if self.state != self.OrderStates.RUNNING or not self.executor:
            cause = ""
            if self.state == self.OrderStates.CLOSED:
                cause = "your order is closed"
            if self.state == self.OrderStates.CANCELED:
                cause = "your order is canceled"
            if not self.executor:
                cause = "your order hasn\'t executor"
            raise RuntimeError('You can\'t remove executor because {}'.format(cause))
        self.executor = None
        self.state = self.OrderStates.OPEN
        self.save()

    def finish(self) -> None:
        if self.state != self.OrderStates.RUNNING:
            cause = ""
            if self.state == self.OrderStates.CLOSED:
                cause = "your order is closed"
            if self.state == self.OrderStates.CANCELED:
                cause = "your order is canceled"
            if not self.executor:
                cause = "your order hasn\'t executor"
            raise RuntimeError('You can\'t finish order because {}'.format(cause))
        self.state = self.OrderStates.CLOSED
        self.save()

    def cancel(self) -> None:
        if self.state == self.OrderStates.CLOSED:
            raise RuntimeError('Your order has already closed')
        self.state = self.OrderStates.CANCELED
        self.save()

    def is_owner_executor(self, user: User):
        return self.executor.get_down_class() == user.get_spec_type_object()

    def is_owner_customer(self, user: User):
        return self.customer.get_down_class() == user.get_spec_type_object()

    def is_owner(self, user: User):
        return self.is_owner_customer(user) or self.is_owner_executor(user)
