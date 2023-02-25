import re
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework import exceptions

from .models import WorkOrder,BrandPart,Part
from place.models import Branch
from utils.message_handler.handler import msg,get_message




class PartViewsetSerializers(serializers.ModelSerializer):

    brands = serializers.SerializerMethodField(read_only=True)
    
    class Meta: 
        model = Part
        fields = "__all__"

    def get_brands(self,obj):
        return BrandPart.objects.filter(part=obj).values('name','id')


class BrandPartViewsetSerializers(serializers.ModelSerializer):

    class Meta: 
        model = BrandPart
        exclude = ["number"]


class WatingWorkOrderSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = WorkOrder
        fields = ['type_phone','phone_number','problem','create_time']
        extra_kwargs = {
            "branch":{'read_only':True}
        }

    def validate(self, attrs):
        regex_phone = {'city':'^679[0-9]{5}','internal':'^33[0-9]{3}'}
        for status,regex in regex_phone.items():
            if attrs['type_phone'] == status and not re.match(regex,attrs['phone_number']):
                raise exceptions.ValidationError({'phone_number':'not valid'})
        return attrs

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError:
            raise exceptions.ParseError(get_message(msg.ERROR_WORKORDER_ALREADY_EXISTS))
        
    def create(self, validated_data):
        try:
            place = Branch.objects.get(place__storekeeper=self.context['user'])
            return WorkOrder.objects.create(**validated_data,branch=place)
        except Branch.DoesNotExist:
            raise exceptions.ParseError(get_message(msg.ERROR_NOT_SAVE_PLACE_FOR_YOU))
        

class DetailWorkOrderTechnicianViewsetSerializers(serializers.ModelSerializer):

    brandpart = serializers.SerializerMethodField()
    branch = serializers.CharField(source='branch.name',read_only =True)

    class Meta:
        model = WorkOrder
        fields = "__all__"
    
    def get_brandpart(self,obj):
        if obj.brandpart:
            brandparts = BrandPart.objects.filter(
                   id__in=obj.brandpart.keys()
            ).values('id','name','part__name')

            for brandpart in brandparts:
                brandpart['number'] = obj.brandpart[str(brandpart['id'])]
            return brandparts    


class WorkOrderStorekepeerViewsetSerializers(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='workorder-technician-detail',read_only=True)
    place = serializers.CharField(source='branch.place.name',read_only =True)
    branch = serializers.CharField(source='branch.name',read_only =True)

    class Meta:
        model = WorkOrder
        fields = ['url','number','create_time','phone_number','place','branch','status']


class WorkOrderTechnicianViewsetSerializers(WorkOrderStorekepeerViewsetSerializers):

    class Meta:
        model = WorkOrder
        fields = ['url','number','create_time','phone_number','place',
                  'branch','status','brandpart','description_status_cancel',
                  'type_phone','problem','description']
        extra_kwargs = {
            'problem':{'write_only':True},
            'brandpart':{'write_only':True},
            'type_phone':{'write_only':True},
            'description':{'write_only':True},
            'description_status_cancel':{'write_only':True}
        }

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError:
            raise exceptions.ParseError(get_message(msg.ERROR_WORKORDER_ALREADY_EXISTS))