from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework import exceptions

from .models import Category,BrandCategory,Part
from utils.message_handler.handler import get_message,msg








class CategoryViewsetSerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class BrandCategoryViewsetSerializers(serializers.ModelSerializer):

    class Meta:
        model = BrandCategory
        fields = "__all__"


class CategoryCustomField(serializers.CharField):

    def to_internal_value(self, data):  
        try:
            category = get_object_or_404(Category,id=data)
            return category
        except ValueError:
            raise exceptions.ParseError(get_message(msg.ERROR_INCORRECT_TYPE_EXPECTED_PK_VALUE))
        

class PartViewsetSerializers(serializers.ModelSerializer):

    category = CategoryCustomField()

    class Meta:
        model = Part
        exclude =['number']

    
