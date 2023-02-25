from django.db.models import ProtectedError
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework import mixins

from django_filters import rest_framework as django_filters

from .models import Category,BrandCategory,Part,Device,BrandPart,WorkOrder
from utils.message_handler.handler import get_message,msg
from utils.permissions import IsTechnicianDevice,IsInspector,IsStorekepeer
from phone_line.views import WorkOrderTechnicianViewsetFilterSet as PhoneLineWorkOrderTechnicianViewsetFilterSet

from .serializers import (
    DetailWorkOrderTechnicianViewsetSerializers,
    WorkOrderStorekepeerViewsetSerializers,
    WorkOrderTechnicianViewsetSerializers,
    DeviceStorekepeerViewsetSerializers,
    DetailCategoryViewsetSerializers,
    BrandCategoryViewsetSerializers,
    DetailDeviceViewsetSerializers,
    DetailPartViewsetSerializers,
    WatingWorkOrderSerializers,
    BrandPartViewsetSerializers,
    CategoryViewsetSerializers,
    DeviceViewsetSerializers,
    PartViewsetSerializers,
)
                                    


class DeviceViewsetFilterSet(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['brandcategory__category'].label = 'Category'
        self.filters['branch__place'].label = 'Place'

    branch__place__storekeeper = django_filters.ModelChoiceFilter(queryset=get_user_model().
                                                                  objects.filter(role='storekeeper'),
                                                                  label='Storekeeper')
    
    class Meta:
        model = Device
        fields = ['brandcategory','brandcategory__category',
                 'branch','branch__place','branch__place__storekeeper']


class WorkOrderTechnicianViewsetFilterSet(PhoneLineWorkOrderTechnicianViewsetFilterSet):

    unrepairable_time = django_filters.DateFromToRangeFilter()
    repair_in_city_time = django_filters.DateFromToRangeFilter()
    provide_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = WorkOrder
        fields = ['status','create_time','finished_time',
                  'unrepairable_time','repair_in_city_time',
                  'provide_time','cancel_time','accept_time']


class CategoryViewset(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    permission_classes = [IsTechnicianDevice]
    serializer_class = CategoryViewsetSerializers
    search_fields = ['name']

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            raise exceptions.ParseError(get_message(msg.ERROR_PROTECTED_CANNOT_DELETE_FIELD))
            
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailCategoryViewsetSerializers
        return super().get_serializer_class()


class BrandCategoryViewset(viewsets.ModelViewSet):

    permission_classes = [IsTechnicianDevice]
    queryset = BrandCategory.objects.all()
    serializer_class = BrandCategoryViewsetSerializers
    filterset_fields = ['category']
    search_fields = ['name']


class PartViewset(viewsets.ModelViewSet):

    permission_classes = [IsTechnicianDevice]
    queryset = Part.objects.all()
    serializer_class = PartViewsetSerializers
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailPartViewsetSerializers
        return super().get_serializer_class()


class BrandPartViewset(viewsets.ModelViewSet):

    permission_classes = [IsTechnicianDevice]
    queryset = BrandPart.objects.all()
    serializer_class = BrandPartViewsetSerializers
    filterset_fields = ['part']
    search_fields = ['name']


class DeviceViewset(viewsets.ModelViewSet):
    
    permission_classes = [IsInspector]
    queryset = Device.objects.all()
    serializer_class = DeviceViewsetSerializers
    lookup_field = 'pk'
    filterset_class = DeviceViewsetFilterSet
    search_fields = ['serial']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user':f'{self.request.user.first_name} {self.request.user.last_name}'})
        return context

    def get_serializer_class(self):
        if self.action == 'retrieve' :
            return DetailDeviceViewsetSerializers
        return super().get_serializer_class()


class DeviceStorekepeerViewset(mixins.ListModelMixin,
                               viewsets.GenericViewSet,
                               mixins.RetrieveModelMixin):

    permission_classes = [IsStorekepeer]
    queryset = Device.objects.all()
    serializer_class = DeviceStorekepeerViewsetSerializers
    search_fields = ['serial']

    def get_queryset(self):
        return super().get_queryset().filter(
            branch__place__storekeeper__id=self.request.user.id
        )

    def get_serializer_class(self):
        if self.action == 'retrieve' :
            return DetailDeviceViewsetSerializers
        return super().get_serializer_class()

class WatingWorkOrderViewset(viewsets.ModelViewSet):

    permission_classes = [IsStorekepeer]
    queryset = WorkOrder.objects.all()
    serializer_class = WatingWorkOrderSerializers
    search_fields = ['device__brandcategory__category__name',
                     'device__brandcategory__name',
                     'device__serial']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user':self.request.user})
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(
            device__branch__place__storekeeper__id=self.request.user.id,
            status='wating'
        ).order_by('-create_time')


class WorkOrderStorekepeerViewset(mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet,
                                  mixins.ListModelMixin):

    permission_classes = [IsStorekepeer]
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderStorekepeerViewsetSerializers
    filterset_class = WorkOrderTechnicianViewsetFilterSet
    search_fields = ['device__brandcategory__category__name',
                     'device__brandcategory__name',
                     'device__branch__place__name',
                     'device__branch__name',
                     'device__serial','number']

    def get_queryset(self):
        qs = super().get_queryset().filter(
                device__branch__place__storekeeper__id=self.request.user.id
            )
        if self.request.query_params.get('status') in ('cancel','wating'):
            return qs.order_by('-create_time')
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailWorkOrderTechnicianViewsetSerializers
        return super().get_serializer_class()


class WorkOrderTechnicianViewset(mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 WorkOrderStorekepeerViewset):
                                 
    permission_classes = [IsTechnicianDevice]
    serializer_class = WorkOrderTechnicianViewsetSerializers
 
    def get_queryset(self):
        qs = self.queryset
        if self.request.query_params.get('status') in ('cancel','wating'):
            return qs.order_by('-create_time')
        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user':f'{self.request.user.first_name} {self.request.user.last_name}'})
        return context
        




    


 
