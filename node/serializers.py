# serializers.py
from rest_framework import serializers

class RelationCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    data = serializers.CharField()
