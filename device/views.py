from django.shortcuts import render
from django.db.models import ProtectedError

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import exceptions

from .models import Category,BrandCategory
from utils.message_handler.handler import get_message,msg
from utils.permissions import IsTechnicianDevice
from .serializers import CategoryViewsetSerializers,\
                         BrandCategoryViewsetSerializers



class CategoryViewset(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    
    queryset = Category.objects.all()
    permission_classes = [IsTechnicianDevice]
    serializer_class = CategoryViewsetSerializers

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            raise exceptions.ParseError(get_message(msg.ERROR_PROTECTED_CANNOT_DELETE_FIELD))


class BrandCategoryViewset(CategoryViewset):

    queryset = BrandCategory.objects.all()
    serializer_class = BrandCategoryViewsetSerializers

