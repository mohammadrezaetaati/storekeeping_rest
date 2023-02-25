from django.core.exceptions import ValidationError

from rest_framework import exceptions

from utils.message_handler.handler import get_message,msg


def chech_required_brandpart(bool,value):
    if isinstance(value,list):
        if len(value) is 0 and bool:
            raise exceptions.ParseError(get_message(msg.ERROR_FIELD_IS_REQUIRED,field='brandpart'))
        elif len(value)>0 and not bool :
            raise exceptions.ParseError(get_message(msg.ERROR_FIELD_IS_NULL,field='brandpart'))
    elif isinstance(value,str):
        pass
        
 
  

    
    



