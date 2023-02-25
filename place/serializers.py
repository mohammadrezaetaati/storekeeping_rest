from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import exceptions

from utils.message_handler.handler import get_message,msg
from .models import Place,Branch




class DetailPlaceViewsetSerializers(serializers.ModelSerializer):

    storekeeper = serializers.SerializerMethodField()
    branchs = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = "__all__"

    def get_storekeeper(self,obj):
        return f'{obj.storekeeper.first_name} {obj.storekeeper.last_name} - {obj.storekeeper.personnel_id}' 
    
    def get_branchs(self,obj):
        return Branch.objects.filter(place=obj).values('id','name','boss','phone')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['branchs'].count() is 0 :
            response['branchs'] = None   
        return response
        

class PlaceViewsetSerializers(serializers.HyperlinkedModelSerializer):

    storekeeper = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.
                                                     filter(role = 'storekeeper'),
                                                     write_only =True)

    class Meta:
        model = Place
        fields = "__all__"
        extra_kwargs = {'boss':{'write_only':True}}



class BranchViewsetSerializers(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = "__all__"

