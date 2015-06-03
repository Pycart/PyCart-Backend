from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from main_models.item import Item
from main.main_models.order import Order, Status


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Item
        fields = ('tags',)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(required=True, many=True)
    _current_status = StatusSerializer(required=True, many=False)

    class Meta:
        model = Order
        exclude = ('user',)
