from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from main_models.item import Item


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Item
        fields = ('tags',)