from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from main.main_models.user import ShopUser
from main_models.item import Item, Option
from main_models.tag import Shop_Item_Tag
from main_models.order import Order, Status


class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ('email', )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option

class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    option = OptionSerializer()

    class Meta:
        model = Item


class ItemDetailSerializer(serializers.ModelSerializer):
    option = serializers.ReadOnlyField(source="option.name")
    tags = TagListSerializerField()

    class Meta:
        model = Item
        exclude = ('tags',)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(required=True, many=True)
    _current_status = StatusSerializer(required=True, many=False)

    class Meta:
        model = Order
        exclude = ('user',)


class TagSerializer(TaggitSerializer, serializers.ModelSerializer):
    # parent = TagListSerializerField()

    class Meta:
        model = Shop_Item_Tag




