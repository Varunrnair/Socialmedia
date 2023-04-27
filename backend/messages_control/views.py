from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView


class Message(ModelViewSet):
    queryset=Message.objects.select_related("sender","receiver")
    serializer_class=MessageSerializer
    
    def list(self, request, *args, **kwargs):
        data = self.request.query_params.dict()
        user_id = data.get("user_id", None)
        if user_id:
            active_user_id = self.request.user.id
            return self.queryset.filter(sender_id=user_id, receiver_id=active_user_id).distinct()
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        if str(request.user.id) != str(request.data.get("sender_id", None)):
            raise Exception("only sender can create a message")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
    def update(self, request, *args, **kwargs):
        instance=self.get_object()
        serializer = self.serializer_class(
            data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()    

    def delete(self, instance):
        if self.request.user == instance.sender:
            instance.delete()