
""" Success message codes: Range [2000 - 2999] """


SUCCESS_MESSAGE_CODES = {
  
}


""" Error message codes: Range [4000 - 4999] """
ERROR_UNKNOWN = 4000
ERROR_PROTECTED_CANNOT_DELETE_FIELD = 4001


ERROR_MESSAGE_CODES = {
    ERROR_UNKNOWN: ("Error occurred, something went wrong."),
    ERROR_PROTECTED_CANNOT_DELETE_FIELD: ("Cannot delete some instances of model because they are referenced through protected foreign keys"),
  
}

""" All message codes are merged together in this section """
MESSAGE_CODES = {**SUCCESS_MESSAGE_CODES, **ERROR_MESSAGE_CODES}
