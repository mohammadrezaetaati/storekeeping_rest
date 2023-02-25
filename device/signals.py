from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import WorkOrder
from utils.common import create_work_order_number
from .utils import WorkOrderStatus
from phone_line.models import WorkOrder as PhoneLineWorkOrder

@receiver(pre_save,sender=PhoneLineWorkOrder)
@receiver(pre_save,sender=WorkOrder)
def check_for_create_number(sender,instance,**kwargs):
    status = getattr(instance,'status')
    
    try:
        if sender.__module__ == 'phone_line.models':
            number = PhoneLineWorkOrder.objects.first().number
        else:
            number = WorkOrder.objects.first().number
    except AttributeError:
        number = None

    if instance.number is None and status not in ('wating','cancel'):
        setattr(instance,'number',create_work_order_number(number))


@receiver(pre_save,sender=PhoneLineWorkOrder)
@receiver(pre_save,sender=WorkOrder)
def check_status(sender,instance,**kwargs): 
    WorkOrderStatus(instance).check_status()














    





