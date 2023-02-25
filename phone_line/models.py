from django.db import models
from django.db.models import Q
from utils.base_models import BaseWorkOrder,BaseBrandPartModel
from place.models import Branch


class Part(models.Model):

    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.name


class BrandPart(BaseBrandPartModel):

    part = models.ForeignKey(Part,on_delete=models.PROTECT)


class WorkOrder(BaseWorkOrder):

    TYPE_PHONE_CHOICES=[
        ('internal','Internal'),
        ('city','City')
    ]

    STATUS_CHOICES = [
        ('finished','Finished'),
        ('accept','Accept'),
        ('wating','Wating'),
        ('cancel','Cancel'),
    ]

    branch = models.ForeignKey(Branch,on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)
    brandpart = models.JSONField(dict,null=True)
    type_phone =models.CharField(max_length=8,choices=TYPE_PHONE_CHOICES)
    status = models.CharField(max_length=8,choices=STATUS_CHOICES,default='wating')
    
    class Meta:
        ordering = ('-number',)
        constraints = [
            models.UniqueConstraint(fields=['phone_number'],condition=~Q(status='finished') & ~Q(status='cancel'),name='uniqe with status')
        ]
