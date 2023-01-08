from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

from utils.base_models import BasePlaceModel





User = get_user_model()


class Place(BasePlaceModel):

    storekeeper = models.ForeignKey(User,on_delete=models.PROTECT)


class Branch(BasePlaceModel):
    
    name = models.CharField(max_length=30)
    place = models.ForeignKey(Place,on_delete=models.PROTECT)
    phone = models.CharField(max_length=20)

    class Meta:
        unique_together = ('name','place')

    def __str__(self) -> str:
        return f'{self.name} - {self.place.name}'



