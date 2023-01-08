from django.shortcuts import render

from rest_framework import viewsets

from .models import Place,Branch
from utils.permissions import IsTechnicianDevice
from .serializers import PlaceViewsetSerializers




class PlaceViewset(viewsets.ModelViewSet):

    queryset = Place.objects.all()
    permission_classes = [IsTechnicianDevice]
    serializer_class = PlaceViewsetSerializers




