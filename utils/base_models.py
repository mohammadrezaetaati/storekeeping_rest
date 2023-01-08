from django.db import models






class BasePlaceModel(models.Model):

    name = models.CharField(max_length=40,unique=True)
    boss = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class BasePartModel(models.Model):

    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    number = models.JSONField(dict,null=True,blank=True)

    class Meta:
        abstract = True


class BaseWorkOrder(models.Model):

    STATUS_CHOICES = [
        ('finished','Finished'),
        ('wating','Wating'),
        ('accept','Accept'),
        ('cancel','Cancel'),
    ]

    number = models.CharField(max_length=30)
    problem = models.TextField()
    description_status_cancel = models.TextField()
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    accept_time = models.DateTimeField()
    finished_time = models.DateTimeField()
    cancel_time = models.DateTimeField()
    status = models.CharField(max_length=14,choices=STATUS_CHOICES)


    class Meta:
        abstract = True
