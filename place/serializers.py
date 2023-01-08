from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import exceptions

from utils.message_handler.handler import get_message,msg
from place.models import Place,Branch




class PlaceViewsetSerializers(serializers.ModelSerializer):

    storekeeper_name = serializers.SerializerMethodField()
    storekeeper = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.
                                                     filter(role = 'storekeeper'),
                                                      write_only =True)
    class Meta:
        model = Place
        fields = "__all__"

    def get_storekeeper_name(self,obj):
        return f'{obj.storekeeper.first_name}{obj.storekeeper.last_name} - {obj.storekeeper.personnel_id}' 


class BranchViewsetSerializers(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = "__all__"

