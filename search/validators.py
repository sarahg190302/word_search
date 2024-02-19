from rest_framework import serializers

class AddParagraphValidator(serializers.Serializer):
    text = serializers.CharField(min_length=1)

class ListTopParagraphValidator(serializers.Serializer):
    word = serializers.CharField(min_length=1)
    top_n = serializers.IntegerField()