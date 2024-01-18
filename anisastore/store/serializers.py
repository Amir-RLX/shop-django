from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TestSerializer(Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()


class ProductSerializer(ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    user = CommentUserSerializer()

    class Meta:
        model = models.Comment
        fields = '__all__'


class SubmitCommentSerializer(ModelSerializer):
    user = CommentUserSerializer()

    class Meta:
        model = models.Comment
        fields = ['description']
