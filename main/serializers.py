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
    option = OptionSerializer()

    class Meta:
        model = Item

    def create(self, validated_data):
        option_data = validated_data.pop('option')
        tag_data = validated_data.pop('tags')
        instance = Item()
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.price = validated_data.get('price', instance.price)

        option_instance, created = Option.objects.get_or_create(name=option_data['name'])
        instance.option = option_instance

        # TODO: Implement tag finding/creation
        instance.save()
        return instance


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
