from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from main.models.Order import Order
from main.models.User import User


class BaseRate(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='rates_sent',
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='rates_received',
    )

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE
    )

    comment = models.CharField(
        max_length=256,
        default=""
    )

    @classmethod
    def is_order_rated(cls, order: Order, user: User) -> bool:
        return cls.objects.filter(order=order, author=user).exists()

    @classmethod
    def count_all_rates(cls, user: User):
        rates = cls.objects.filter(user=user)
        if not rates.exists():
            return 0
        rate_sum = 0
        for rate in rates:
            rate_sum += rate.count_rate()
        return rate_sum / rates.count()

    def count_rate(self):
        return 0.0


class CustomerRate(BaseRate):
    generosity = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    certainty = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    positivity = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    politeness = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    def count_rate(self):
        rate_sum = 0
        rate_sum += self.generosity
        rate_sum += self.certainty
        rate_sum += self.positivity
        rate_sum += self.politeness
        return rate_sum / 4


class ExecutorRate(BaseRate):
    speed = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    politeness = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    reliability = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    competence = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        null=True
    )

    def count_rate(self):
        rate_sum = 0
        rate_sum += self.speed
        rate_sum += self.politeness
        rate_sum += self.reliability
        rate_sum += self.competence
        return rate_sum / 4
