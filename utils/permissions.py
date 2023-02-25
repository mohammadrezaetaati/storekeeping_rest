from rest_framework.permissions import IsAuthenticated


                

class IsTechnicianPhoneline(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
            request.user.role == 'technician_phoneline' or\
            request.user.role == 'admin'



class IsTechnicianDevice(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
                request.user.role == 'technician_device' or\
                request.user.role == 'admin'


class IsStorekepeer(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
                    request.user.role == 'storekeeper' or\
                    request.user.role == 'admin'


class IsInspector(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
                        request.user.role == 'inspector' or\
                        request.user.role == 'admin'