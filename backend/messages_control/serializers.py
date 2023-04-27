from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField("get_sender_data")
    sender_id = serializers.IntegerField(write_only=True)
    receiver = serializers.SerializerMethodField("get_receiver_data")
    receiver_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Message
        fields = "__all__"

    def get_receiver_data(self, obj):
        from user_control.serializers import UserSerializer
        return UserSerializer(obj.receiver.email).data

    def get_sender_data(self, obj):
        from user_control.serializers import UserSerializer
        return UserSerializer(obj.sender.email).data
