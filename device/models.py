from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

from place.models import Branch
from utils.base_models import BaseBrandPartModel,BaseWorkOrder
from utils.message_handler.handler import get_message,msg




User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=30,unique=True)


    def __str__(self) -> str:
        return self.name


class BrandCategory(models.Model):

    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name','category',)

    def __str__(self) -> str:
        return f'{self.name} - {self.category.name}'


class Part(models.Model):

    name = models.CharField(max_length=40)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    visible_in_device = models.BooleanField()

    class Meta:
        unique_together = ('name','category')

    def __str__(self) -> str:
        return f'{self.name} - {self.category.name}'


class BrandPart(BaseBrandPartModel):

    part = models.ForeignKey(Part,on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name','part')
    
    def __str__(self) -> str:
        return f'{self.name} {self.part.name}'



class Device(models.Model):

    STATUS_CHOICES = [
        ('broken_down','Broken_down'),
        ('in_repair','In_repair'),
        ('in_work','In_work')
    ]

    serial = models.CharField(max_length=12,unique=True)
    brandcategory = models.ForeignKey(BrandCategory,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.PROTECT)
    have_part =  models.BooleanField()
    brandpart = models.ManyToManyField(BrandPart,null=True)
    user = models.CharField(max_length=30)
    have_seal_number = models.BooleanField()
    seal_number = models.CharField(max_length=20,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=11,choices=STATUS_CHOICES,default='in_work')

    def __str__(self) -> str:
        return f'{self.brandcategory.category.name} - {self.brandcategory.name} - {self.branch.place.storekeeper}'
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(have_seal_number=True,seal_number__isnull=False)| 
                                         Q(have_seal_number=False,seal_number__isnull=True),
                                         name='check have_seal_number')
        ]
        

class WorkOrder(BaseWorkOrder):

    STATUS_CHOICES = [
        ('repair_in_city','Repair_In_City'),
        ('unrepairable','Unrepairable'),
        ('finished','Finished'),
        ('provide','Provide'),
        ('wating','Wating'),
        ('cancel','Cancel')
    ]

    device = models.ForeignKey(Device,on_delete=models.PROTECT)
    brandpart = models.JSONField(dict,null=True)
    delivery_user = models.CharField(max_length=20,null=True)
    transfere_user = models.CharField(max_length=20,null=True)
    delivery_operator = models.CharField(max_length=20,null=True,blank=True)
    transfere_oprator = models.CharField(max_length=20,null=True,blank=True)
    unrepairable_time = models.DateTimeField(null=True,blank=True)
    repair_in_city_time = models.DateTimeField(null=True,blank=True)    
    provide_time = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=14,choices=STATUS_CHOICES,default='wating')

    class Meta:
        ordering = ('-number',)
        constraints = [
            models.UniqueConstraint(fields=['device'],condition=~Q(status='finished') &
                                    ~Q(status='cancel'),name='unique with status')
        ]







