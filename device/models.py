from django.db import models

from place.models import Place
from utils.base_models import BasePartModel,BaseWorkOrder




class Category(models.Model):

    name = models.CharField(max_length=30,unique=True)
    identification = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class BrandCategory(models.Model):

    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name','category',)

    def __str__(self) -> str:
        return f'{self.name} - {self.category.name}'


class Part(BasePartModel):

    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name','brand','category')

    def __str__(self) -> str:
        return f'{self.name} - {self.category.name}'


class Device(models.Model):

    serial = models.CharField(max_length=12)
    brandcategory = models.ForeignKey(BrandCategory,on_delete=models.CASCADE)
    place = models.ForeignKey(Place,on_delete=models.PROTECT)
    part = models.ForeignKey(Part,on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.brandcategory.category.name} - {self.brandcategory.name}'


class WorkOrder(BaseWorkOrder):

    STATUS_CHOICES = [
        ('repair_in_city','Repair_In_City'),
        ('unrepairable','Unrepairable'),
        ('finished','Finished'),
        ('provide','Provide'),
        ('wating','Wating'),
        ('accept','Accept'),
        ('cancel','Cancel')
    ]

    device = models.ForeignKey(Device,on_delete=models.PROTECT)
    delivery_user = models.CharField(max_length=20)
    transfere_user = models.CharField(max_length=20)
    delivery_operator = models.CharField(max_length=20)
    transfere_oprator = models.CharField(max_length=20)
    unrepairable_time = models.DateTimeField()
    repair_in_city_time = models.DateTimeField()
    provide_time = models.DateTimeField()
    status = models.CharField(max_length=14,choices=STATUS_CHOICES)







