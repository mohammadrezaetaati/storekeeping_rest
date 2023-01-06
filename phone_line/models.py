from django.db import models

from utils.base_models import BaseWorkOrder,BasePartModel
from place.models import Place


class Part(BasePartModel):

    def __str__(self) -> str:
        return self.name


class WorkOrder(BaseWorkOrder):

    TYPE_PHONE_CHOICES=[
        ('internal','Internal'),
        ('city','City')
    ]

    place = models.ForeignKey(Place,on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)
    part = models.ForeignKey(Part,on_delete=models.PROTECT)
    type_phone =models.CharField(max_length=8,choices=TYPE_PHONE_CHOICES)

    
