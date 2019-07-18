from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from safedelete import DELETED_VISIBLE_BY_PK
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


class Hotel(SafeDeleteModel):
    """docstring for Hotel."""
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=255, unique=True)
    stars = models.PositiveSmallIntegerField(default = 3, validators=[MinValueValidator(1), MaxValueValidator(5)])

    # def __init__(self, arg):
    #     super(Hotel, self).__init__(arg)
    #     self.arg = arg

    def __str__(self):
        return self.name



class Classification(SafeDeleteModel):
    """docstring for Classification."""
    _safedelete_policy = SOFT_DELETE_CASCADE

    CLASS_CHOICES = [
        ('royal', 'Royal'),
        ('grand', 'Grand'),
        ('ambassador', 'Ambassador'),
    ]

    name = models.CharField(max_length=255, choices=CLASS_CHOICES, default='grand', unique=True)
    price = models.PositiveIntegerField(default = 100, validators=[MinValueValidator(70), MaxValueValidator(150)])

    def __str__(self):
        return self.name


class Room(SafeDeleteModel):
    """docstring for Room."""
    _safedelete_policy = SOFT_DELETE_CASCADE

    number = models.CharField(max_length=255)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name="rooms")
    is_avaliable = models.BooleanField(default = True)
    price = models.PositiveIntegerField(default=None, blank=True, null=True)
    user = models.ManyToManyField(get_user_model(), through='Reservation',blank=True)

    class Meta:
        unique_together = ('number', 'hotel',)

    # def __init__(self, arg):
    #     super(Room, self).__init__()
    #     self.arg = arg

    def __str__(self):
        return f'{self.hotel}/{self.number}'

    def get_price(self):
        price = self.price if self.price != Null else self.classification.price
        return price


class Reservation(SafeDeleteModel):
    """docstring for Room."""
    _safedelete_policy = SOFT_DELETE_CASCADE
    _safedelete_visibility = DELETED_VISIBLE_BY_PK

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    paid = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    expired_at = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'room',)

    def __str__(self):
        return f'{self.user} - {self.room}'
