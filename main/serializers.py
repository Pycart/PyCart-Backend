from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from main.main_models.user import ShopUser
from main_models.item import Item, Option
from main_models.tag import Shop_Item_Tag
from main_models.order import Order, Status


class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ('email', 'first_name', 'last_name', 'is_staff')
        read_only_fields = ('email', )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    options = OptionSerializer(many=True)

    class Meta:
        model = Item

    def create(self, validated_data):
        option_data = validated_data.pop('options')
        tag_data = validated_data.pop('tags')
        item = Item.objects.create(**validated_data)

        for option in option_data:
            option, created = Option.objects.get_or_create(name=option['name'])
            item.options.add(option)

        for tag in tag_data:
            item.tags.add("%s" % tag["name"])

        # TODO: Implement tag finding/creation
        # instance.save()
        return item


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
