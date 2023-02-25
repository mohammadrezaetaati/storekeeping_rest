from django.db.models.signals import pre_save
from django.dispatch import receiver

from device.signals import check_for_create_number
from .models import WorkOrder

# @receiver(pre_save,sender=WorkOrder)
# check_for_create_number