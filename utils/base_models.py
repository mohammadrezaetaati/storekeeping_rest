from django.db import models






class BasePlaceModel(models.Model):

    name = models.CharField(max_length=40,unique=True)
    boss = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class BaseBrandPartModel(models.Model):

    name = models.CharField(max_length=40)
    number = models.JSONField(dict,null=True,blank=True)

    class Meta:
        abstract = True


class BaseWorkOrder(models.Model):

    number = models.CharField(max_length=30,null=True,blank=True)
    problem = models.TextField()
    description_status_cancel = models.TextField(null=True)
    description = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    finished_time = models.DateTimeField(null=True,blank=True)
    cancel_time = models.DateTimeField(null=True,blank=True)
    accept_time = models.DateTimeField(null=True)

    class Meta:
        abstract = True
