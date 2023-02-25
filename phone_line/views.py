from rest_framework import viewsets
from rest_framework import mixins

from django_filters import rest_framework as django_filters

from .models import WorkOrder,Part,BrandPart
from utils.permissions import IsStorekepeer,IsTechnicianPhoneline
from .serializers import (
    DetailWorkOrderTechnicianViewsetSerializers,
    WorkOrderStorekepeerViewsetSerializers,
    WorkOrderTechnicianViewsetSerializers,
    BrandPartViewsetSerializers,
    WatingWorkOrderSerializers, 
    PartViewsetSerializers,
)




class WorkOrderTechnicianViewsetFilterSet(django_filters.FilterSet):

    create_time = django_filters.DateFromToRangeFilter()
    finished_time = django_filters.DateFromToRangeFilter()
    cancel_time = django_filters.DateFromToRangeFilter()
    accept_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = WorkOrder
        fields = ['status','type_phone','create_time','finished_time',
                  'cancel_time','accept_time']
        

class PartViewset(viewsets.ModelViewSet):

    permission_classes = [IsTechnicianPhoneline]
    queryset = Part.objects.all()
    serializer_class = PartViewsetSerializers
    search_fields = ['name']


class BrandPartViewset(viewsets.ModelViewSet):

    permission_classes = [IsTechnicianPhoneline]
    queryset = BrandPart.objects.all()
    serializer_class = BrandPartViewsetSerializers
    filterset_fields = ['part']
    search_fields = ['name']


class WatingWorkOrderViewset(viewsets.ModelViewSet):

    permission_classes = [IsStorekepeer]
    queryset = WorkOrder.objects.all()
    serializer_class = WatingWorkOrderSerializers
    filterset_fields = ['type_phone']
    search_fields = ['phone_number']

    def get_queryset(self):
        return super().get_queryset().filter(
            place__storekeeper__id=self.request.user.id,
            status='wating'
        ).order_by('-create_time')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user':self.request.user})
        return context
    

class WorkOrderStorekepeerViewset(mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet,
                                  mixins.ListModelMixin):
    
    permission_classes = [IsStorekepeer]
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderStorekepeerViewsetSerializers
    filterset_class = WorkOrderTechnicianViewsetFilterSet
    search_fields = ['phone_number','branch__name','branch__place__name','number']

    def get_queryset(self):
        qs = super().get_queryset().filter(
                branch__place__storekeeper__id=self.request.user.id
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

    permission_classes = [IsTechnicianPhoneline]
    serializer_class = WorkOrderTechnicianViewsetSerializers

    def get_queryset(self):
        qs = self.queryset
        if self.request.query_params.get('status') in ('cancel','wating'):
            return qs.order_by('-create_time')
        return qs
    




    

