from django.shortcuts import render

from rest_framework import viewsets

from .models import Place,Branch
from utils.permissions import IsTechnicianDevice
from .serializers import PlaceViewsetSerializers,BranchViewsetSerializers,DetailPlaceViewsetSerializers




class PlaceViewset(viewsets.ModelViewSet):

    queryset = Place.objects.all()
    permission_classes = [IsTechnicianDevice]
    serializer_class = PlaceViewsetSerializers
    search_fields = ['name','boss']


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailPlaceViewsetSerializers
        return super().get_serializer_class()


class BranchViweset(viewsets.ModelViewSet):

    queryset = Branch.objects.all()
    serializer_class = BranchViewsetSerializers
    permission_classes = [IsTechnicianDevice]
    filterset_fields = ['place']
    search_fields = ['name','boss','place__name']
    

    
