from django.db import IntegrityError
from django.db.models import Value,CharField
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework import exceptions

from place.models import Place
from .models import Category,BrandCategory,Part,Device,BrandPart,WorkOrder
from utils.message_handler.handler import get_message,msg
from place.serializers import BranchViewsetSerializers, DetailPlaceViewsetSerializers,PlaceViewsetSerializers
from .validators import chech_required_brandpart



class DetailCategoryViewsetSerializers(serializers.ModelSerializer):

    brands = serializers.SerializerMethodField()
    parts = serializers.SerializerMethodField()
    number_connected_devices = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"
    
    def get_brands(self,obj):
        return BrandCategory.objects.filter(category=obj).values('id','name')

    def get_parts(self,obj):
        return Part.objects.filter(category=obj).values('id','name')
    
    def get_number_connected_devices(self,obj):
        return Device.objects.filter(brandcategory__category=obj).count()
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['brands'].count() is 0 :
            response['brands'] = None   
        return response


class CategoryViewsetSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class BrandCategoryViewsetSerializers(serializers.ModelSerializer):

    class Meta:
        model = BrandCategory
        fields = "__all__"

        
class DetailPartViewsetSerializers(serializers.ModelSerializer):

    brands = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Part
        fields = "__all__"

    def get_brands(self,obj):
        return BrandPart.objects.filter(part=obj).values('name','id')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['brands'].count() is 0 :
            response['brands'] = None   
        return response


class PartViewsetSerializers(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='part-detail',read_only=True)
    

    class Meta: 
        model = Part
        fields = "__all__"
        extra_kwargs = {
            'visible_in_device':{'write_only':True},
            'category':{'write_only':True}
        }


class BrandPartViewsetSerializers(serializers.ModelSerializer):

    class Meta: 
        model = BrandPart
        exclude = ["number"]


class BrandCategorySerializers(BrandCategoryViewsetSerializers):

    category = serializers.CharField(source='category.name')


class PlaceSerializers(serializers.ModelSerializer):

    storekeeper = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = "__all__"
    
    def get_storekeeper(self,obj):
        return f'{obj.storekeeper.first_name} {obj.storekeeper.last_name} - {obj.storekeeper.personnel_id}' 


class BranchSerializers(BranchViewsetSerializers):

    place = PlaceSerializers()


class BrandPartSerializers(BrandPartViewsetSerializers):

    part = serializers.CharField(source='part.name')


class DetailDeviceViewsetSerializers(serializers.ModelSerializer):

    brandcategory = BrandCategorySerializers()
    branch = BranchSerializers()
    brandpart = BrandPartSerializers(many=True)

    class Meta:
        model = Device
        exclude = ['have_seal_number','have_part']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if len(response['brandpart'])<1:
           del response['brandpart']
        if response['seal_number'] is None:
           del response['seal_number']
        return response


class DeviceStorekepeerViewsetSerializers(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='device-detail',read_only=True)
    category = serializers.CharField(source='brandcategory.category.name',read_only=True)

    class Meta:
        model = Device
        fields = ['url','serial','category','brandcategory']


class DeviceViewsetSerializers(DeviceStorekepeerViewsetSerializers):

    brandpart = serializers.PrimaryKeyRelatedField(queryset=BrandPart.objects.
                                                   filter(part__visible_in_device=True),
                                                   many=True,write_only=True)
                                           
    class Meta:
        model = Device
        fields = ['url','serial','category','brandcategory','branch',
                  'brandpart','have_seal_number','seal_number','have_part']
        extra_kwargs = {
            "branch":{'write_only':True},
            "brandpart":{'write_only':True},
            "have_part":{'write_only':True},
            "seal_number":{'write_only':True},
            "have_seal_number":{'write_only':True},
        }

    def validate(self, attrs):

        if len(attrs['brandpart']) is 0 and attrs['have_part']:
            raise exceptions.ParseError(get_message(msg.ERROR_FIELD_IS_REQUIRED,field='brandpart'))

        if len(attrs['brandpart'])>0 and not attrs['have_part'] :
            raise exceptions.ParseError(get_message(msg.ERROR_FIELD_IS_NULL,field='brandpart'))

        return attrs

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError:
            raise exceptions.ParseError(get_message(msg.ERROR_CHECK_HAVE_SEAL_NUMBER))

    def create(self, validated_data):
        brandpart=validated_data.pop('brandpart')
        device:Device = Device.objects.create(**validated_data,user=self.context['user'])
        device.brandpart.set(brandpart)
        return device


class WatingWorkOrderSerializers(serializers.ModelSerializer):

    serial = serializers.CharField(write_only=True,max_length=12)
    device = serializers.CharField(source ='device.serial',read_only=True)
    brandcategory = serializers.CharField(source ='device.brandcategory.name',read_only=True)
    category = serializers.CharField(source ='device.brandcategory.category.name',read_only=True)

    class Meta:
        model = WorkOrder
        fields = ['id','problem','serial','create_time','category','device','brandcategory']

    def validate(self, attrs):
        user = self.context['user']

        try:
            self.device = Device.objects.get(serial=attrs['serial'])
        except Device.DoesNotExist:
            raise exceptions.ParseError(get_message(msg.ERROR_DEVICE_DOES_NOT_EXIST))

        if self.device.status == 'broken_down':
            raise exceptions.ParseError(get_message(msg.ERROR_DEVICE_USER_IS_BROKEN_DOWN))

        if self.device.branch.place.storekeeper.id == user.id or user.role == 'admin' :
            return attrs
        
        raise exceptions.ParseError(get_message(msg.ERROR_DEVICE_NOT_OWNER))

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError:
            raise exceptions.ParseError(get_message(msg.ERROR_WORKORDER_ALREADY_EXISTS))

    def create(self, validated_data):
        return WorkOrder.objects.create(problem=validated_data.get('problem'),device=self.device)
        

class DetailWorkOrderTechnicianViewsetSerializers(serializers.ModelSerializer):

    device = DeviceViewsetSerializers()
    brandpart = serializers.SerializerMethodField()

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
    place = serializers.CharField(source='device.branch.place.name',read_only =True)
    branch = serializers.CharField(source='device.branch.name',read_only =True)

    class Meta:
        model = WorkOrder
        fields = ['url','number','create_time','device','place','branch','status']


class WorkOrderTechnicianViewsetSerializers(WorkOrderStorekepeerViewsetSerializers):

    class Meta:
        model = WorkOrder
        fields = ['url','number','create_time','device','place','branch',
                  'status','description_status_cancel','description',
                  'brandpart','delivery_user','transfere_user'] 
        extra_kwargs = {
            'number':{'read_only':True},
            'brandpart':{'write_only':True},
            'description':{'write_only':True},
            'delivery_user':{'write_only':True},
            'transfere_user':{'write_only':True},
            'description_status_cancel':{'write_only':True},
        }

    def validate(self, attrs):
        device = Device.objects.filter(id=attrs['device'].id)
 
        if attrs['status'] == 'unrepairable':
            device.update(status='broken_down')
        elif attrs['status'] == 'finished':
            attrs['delivery_operator'] = self.context['user']
            device.update(status='in_work')
        else:
            device.update(status='in_repair')
        
        if self.instance.transfere_oprator is None and attrs['status'] !='wating':
            setattr(self.instance,'transfere_oprator',self.context['user'])
        return attrs

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError :
            raise exceptions.ParseError(get_message(msg.ERROR_WORKORDER_ALREADY_EXISTS))
        




  

    
