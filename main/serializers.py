from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
<<<<<<< HEAD

=======
from main.main_models.user import ShopUser
>>>>>>> b6c9bf6c499494c1ee460ad65b9a36cac422b8d1
from main_models.item import Item
from main.main_models.order import Order, Status


class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ('email', )


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Item


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(required=True, many=True)
    _current_status = StatusSerializer(required=True, many=False)

    class Meta:
        model = Order
        exclude = ('user',)
