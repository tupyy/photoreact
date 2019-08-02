from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class IDSerializerMixin:
    def get_object(self, validated_data):
        pk = int(validated_data)
        if pk != validated_data:
            raise ValueError('Value must be an int')
        return get_object_or_404(self.Meta.model, pk=pk)


class UserIDSerializer(IDSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

    def validate(self, data):
        return data


class GroupIDSerializer(IDSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'