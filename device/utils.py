from django.utils import timezone

from rest_framework import exceptions

from .models import BrandPart
from utils.message_handler.handler import get_message,msg
from phone_line.models import BrandPart as PhoneLineBrandPart



class WorkOrderStatus:

    default_error_message = {
        'description_status_cancel': get_message(msg.ERROR_DESCRIPTION_STATUS_CANCEL_IS_REQUIRED),
        'delivery_user': get_message(msg.ERROR_DELIVERY_USER_IS_REQUIRED),
        'description': get_message(msg.ERROR_DESCRIPTION_IS_REQUIRED),
        'transfere_user' : get_message(msg.ERROR_TRANSFEREE_USER_IS_REQUIRED),
    }
    
    def __init__(self,instance) -> None:
        self.instance = instance
        self.status = instance.status

    def cancel(self):
        self.return_errors('description_status_cancel')
        self.set_null('description','finished_time','delivery_user','transfere_user',
                      'unrepairable_time','repair_in_city_time','provide_time','brandpart','accept_time','number')
        self.set_time('cancel_time')  

    def wating(self):
        if self.instance.__module__ == 'phone_line.models':
            self.set_null('id','_state','problem','create_time','branch_id','status','phone_number','type_phone')
        else:
            self.set_null('id','_state','problem','create_time','device_id','status','accept_time')

        
    def accept(self):
        if self.instance.__module__ == 'phone_line.models':
            self.set_null('id','_state','problem','create_time','branch_id','status','accept_time','phone_number','type_phone','number')
        else:
            self.set_null('id','_state','problem','create_time',
                          'device_id','status','number','accept_time','delivery_user')
            self.return_errors('delivery_user')
        self.set_time('accept_time')

    def unrepairable(self):
        self.return_errors('description','delivery_user','transfere_user')
        self.set_null('brandpart','repair_in_city_time','provide_time',
                      'description_status_cancel','finished_time','cancel_time')
        self.set_time('unrepairable_time')  
    
    def repair_in_city(self):
        self.return_errors('delivery_user')
        self.set_null('description_status_cancel','finished_time','cancel_time',
                      'transfere_user','unrepairable_time','provide_time')
        self.set_time('repair_in_city_time')
     
    def provide(self):
        if getattr(self.instance,'brandpart') is None and \
            getattr(self.instance,'description') is None:
            raise exceptions.ParseError(get_message(msg.ERROR_DESCRIPTION_OR_BRANDPART_IS_REQUIRED))

        self.return_errors('delivery_user')
        if getattr(self.instance,'brandpart') or getattr(self.instance,'brandpart') == {}:
            valid_field_brandpart(self.instance)

        self.set_null('description_status_cancel','finished_time','cancel_time',
                      'transfere_user','unrepairable_time')
        self.set_time('provide_time') 

    def finished(self):
        if getattr(self.instance,'brandpart') is None and \
            getattr(self.instance,'description') is None:
            raise exceptions.ParseError(get_message(msg.ERROR_DESCRIPTION_OR_BRANDPART_IS_REQUIRED))
        if self.instance.__module__ != 'phone_line.models':

            self.return_errors('delivery_user','transfere_user')
        if getattr(self.instance,'brandpart') or getattr(self.instance,'brandpart') == {}:
            valid_field_brandpart(self.instance)

        self.set_null('description_status_cancel','cancel_time','unrepairable_time')
        self.set_time('finished_time')

    def set_null(self,*fields):
        if self.status in ('wating','accept'):
            for field in self.instance.__dict__.keys():
                if field not in fields:
                    setattr(self.instance,field,None)
            return
        for field in fields:
            setattr(self.instance,field,None)
            
    def set_time(self,field:str):
        return setattr(self.instance,field,timezone.now())

    def return_errors(self,*names):
        for name in names:
            if getattr(self.instance,name) is None:
                print(name)
                raise exceptions.ParseError(
                    WorkOrderStatus.default_error_message.get(name)
                ) 

    def check_status(self):
        if self.status == 'cancel':
            return self.cancel()
        if self.status == 'accept':
            return self.accept()
        if self.status == 'wating':
            return self.wating()
        if self.status == 'unrepairable':
            return self.unrepairable() 
        if self.status == 'repair_in_city':
            return self.repair_in_city()
        if self.status == 'provide' :
            return self.provide()
        if self.status == 'finished' :
            return self.finished()


def valid_field_brandpart(instance):
    brandpart = getattr(instance,'brandpart')

    if not isinstance(brandpart,dict):
        raise exceptions.ValidationError(
            {'brandpart':[f"Expected a dict of items but got type \"{type(brandpart)}\"."]}
        )

    if len(brandpart)<1:
        raise exceptions.ValidationError(
            {'brandpart':'This field may not be blank.'}
        )

    id = []
    for pk,number in brandpart.items():
        if isinstance(number,int) and pk.isnumeric():
            id.append(int(pk))
        else:
            raise exceptions.ValidationError(
                    {'brandpart':['Incorrect type. Expected pk value, received str']}
                ) 
    if instance.__module__ == 'phone_line.models':
        qs = PhoneLineBrandPart.objects.filter(id__in=id).values_list('id',flat=True)
    else:
        qs = BrandPart.objects.filter(id__in=id,part__category=instance.device.brandcategory.category).values_list('id',flat=True)
    difference = set(qs) ^ set(id)
    if difference:
        raise exceptions.ValidationError(
                {'brandpart':[f'Invalid pk \"{next(iter(difference))}\" - object does not exist.']}
            )


    

