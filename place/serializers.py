from rest_framework import serializers
from rest_framework import exceptions

from utils.message_handler.handler import get_message,msg
from place.models import Place




class PlaceViewsetSerializers(serializers.ModelSerializer):
    storekeeper_name = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = "__all__"
        extra_kwargs = {
            'storekeeper':{'write_only':True}
        }

    def validate(self, attrs):
        if attrs['storekeeper'].role != 'storekeeper':
            raise exceptions.ParseError(get_message(msg.ERROR_USER_MUST_ROLE_STOREKEEPER))
        return attrs
    
    def get_storekeeper_name(self,obj):
        return f'{obj.storekeeper.first_name}{obj.storekeeper.last_name} - {obj.storekeeper.personnel_id}' 