
""" Success message codes: Range [2000 - 2999] """


SUCCESS_MESSAGE_CODES = {
  
}


""" Error message codes: Range [4000 - 4999] """
ERROR_UNKNOWN = 4000
ERROR_PROTECTED_CANNOT_DELETE_FIELD = 4001
ERROR_INCORRECT_TYPE_EXPECTED_PK_VALUE = 4002
ERROR_USER_MUST_ROLE_STOREKEEPER = 4003
ERROR_FIELD_IS_REQUIRED = 4004
ERROR_FIELD_IS_NULL  = 4005
ERROR_PART_IS_NOT_FOR_DEVICE = 4006
ERROR_CHECK_HAVE_SEAL_NUMBER = 4007
ERROR_DEVICE_DOES_NOT_EXIST = 4008
ERROR_DEVICE_NOT_OWNER = 4009
ERROR_WORKORDER_ALREADY_EXISTS = 4010
ERROR_DESCRIPTION_STATUS_CANCEL_IS_REQUIRED = 4011
ERROR_DELIVERY_USER_IS_REQUIRED = 4012
ERROR_TRANSFEREE_USER_IS_REQUIRED = 4013
ERROR_DEVICE_USER_IS_BROKEN_DOWN = 4014
ERROR_DESCRIPTION_IS_REQUIRED = 4015
ERROR_DESCRIPTION_OR_BRANDPART_IS_REQUIRED = 4016
ERROR_NOT_SAVE_PLACE_FOR_YOU = 4017



ERROR_MESSAGE_CODES = {
    ERROR_UNKNOWN: ("Error occurred, something went wrong."),
    ERROR_PROTECTED_CANNOT_DELETE_FIELD: ("Cannot delete some instances of model because they are referenced through protected foreign keys"),
    ERROR_INCORRECT_TYPE_EXPECTED_PK_VALUE : ("Incorrect type. Expected pk value, received str."),
    ERROR_USER_MUST_ROLE_STOREKEEPER : ("Error User role must be storekeeper"),
    ERROR_FIELD_IS_REQUIRED : ("This field is requierd")  ,
    ERROR_FIELD_IS_NULL  : ('This field must be null'),
    ERROR_PART_IS_NOT_FOR_DEVICE : ('This part is not for this device'),
    ERROR_CHECK_HAVE_SEAL_NUMBER : ('If the check is have_seal_number, it should not be seal_number It should be null, otherwise it should be null'),
    ERROR_DEVICE_DOES_NOT_EXIST : ('This device is not registered'),
    ERROR_DEVICE_NOT_OWNER : ('You do not own this device'),
    ERROR_WORKORDER_ALREADY_EXISTS :('This work order exists and is being reviewed'),
    ERROR_DESCRIPTION_STATUS_CANCEL_IS_REQUIRED : ('field description_status_cancel is required'),    
    ERROR_DELIVERY_USER_IS_REQUIRED : ('field delivery_user is required'),    
    ERROR_TRANSFEREE_USER_IS_REQUIRED : ('field transfere_user is required'),    
    ERROR_DEVICE_USER_IS_BROKEN_DOWN : ('This device is broken down,not allow create workorder'),    
    ERROR_DESCRIPTION_IS_REQUIRED : ('field description is required'),    
    ERROR_DESCRIPTION_OR_BRANDPART_IS_REQUIRED : ('field description or brandpart is required'),  
    ERROR_NOT_SAVE_PLACE_FOR_YOU : ('for you not save place.please first save place')  
 
}

""" All message codes are merged together in this section """
MESSAGE_CODES = {**SUCCESS_MESSAGE_CODES, **ERROR_MESSAGE_CODES}
