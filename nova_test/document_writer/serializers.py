from rest_framework import serializers

class CreateFileSerializer(serializers.Serializer):
    data = serializers.CharField()
    name = serializers.CharField()