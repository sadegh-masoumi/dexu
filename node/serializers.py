# serializers.py
from rest_framework import serializers

class RelationCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    data = serializers.CharField()


class RelationCreateResponseSerializer(serializers.Serializer):
    origin = serializers.CharField()
    relations_created = serializers.ListField(
        child=serializers.CharField()
    )
    destination_count = serializers.IntegerField()