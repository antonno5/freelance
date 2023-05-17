from django.db import models

from main.models.Order import Order
from main.models.User import User


class Application(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='applications_sent'
    )

    receiver = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='applications_received'
    )

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE
    )

    comment = models.TextField(
        max_length=256
    )

    class AppStates(models.IntegerChoices):
        PENDING = 1
        DECLINED = 2
        ACCEPTED = 3
        FINISHED = 4

    state = models.IntegerField(
        choices=AppStates.choices,
        default=AppStates.PENDING
    )

    def accept(self) -> None:
        if self.state != self.AppStates.PENDING:
            cause = ""
            if self.state == self.AppStates.DECLINED:
                cause = "your application was declined"
            if self.state == self.AppStates.ACCEPTED:
                cause = "your application was accepted"
            raise RuntimeError('You can\'t accept application because {}'.format(cause))
        self.state = self.AppStates.ACCEPTED
        self.order.state = Order.OrderStates.RUNNING
        self.order.executor = self.author.get_spec_type_object()
        self.order.save()
        self.save()

    def decline(self) -> None:
        if self.state != self.AppStates.PENDING:
            cause = ""
            if self.state == self.AppStates.DECLINED:
                cause = "your application was declined"
            if self.state == self.AppStates.ACCEPTED:
                cause = "your application was accepted"
            raise RuntimeError('You can\'t decline application because {}'.format(cause))
        self.state = self.AppStates.DECLINED
        self.save()

    def finish(self) ->None:
        if self.state != self.AppStates.ACCEPTED:
            cause = ""
            if self.state == self.AppStates.PENDING:
                cause = "your application was pending"
            if self.state == self.AppStates.DECLINED:
                cause = "your application was declined"
            if self.state == self.AppStates.FINISHED:
                cause = "your application was already finished"
            raise RuntimeError('You can\'t finish application because {}'.format(cause))
        self.state = self.AppStates.FINISHED
        self.save()
