from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from main.main_models.user import ShopUser
from main_models.item import Item, Option
from main_models.tag import Shop_Item_Tag
from main_models.order import Order, Status, OrderItem
from main_models.save_card import SaveCard
from main_models.address import Address
from main_models.stock_record import StockRecord


class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_staff')
        read_only_fields = ('email',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ('email', 'first_name', 'last_name',)
        # should 'password' be a field they can update?


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order


class StockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRecord


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Item

    def create(self, validated_data):
        # option_data = validated_data.pop('options')
        tag_data = validated_data.pop('tags')
        item = Item.objects.create(**validated_data)

        # for option in option_data:
        #     option, created = Option.objects.get_or_create(name=option['name'])
        #     item.options.add(option)

        for tag in tag_data:
            item.tags.add("%s" % tag["name"])

        # TODO: Implement tag finding/creation
        # instance.save()
        return item


class NestedItemField(serializers.RelatedField):
    def to_representation(self, value):
        items = []
        for item in self.root.instance.variants.all():
            data = ItemDetailSerializer(item).data
            items.append(data)
        return items


class ItemDetailSerializer(serializers.ModelSerializer):
    variants = NestedItemField(read_only=True)
    top_level_item = serializers.IntegerField()

    class Meta:
        model = Item


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status


class OrderItemField(serializers.RelatedField):
    def to_representation(self, value):
        if type(self.root.instance) == list:
            self.root.instance = self.root.instance[0]
        order_item = OrderItem.objects.filter(item=value, order=self.root.instance).first()
        quantity = order_item.quantity
        value = ItemSerializer(value).data
        value['quantity'] = quantity
        return value

    def to_internal_value(self, data):
        pass


class OrderSerializer(serializers.ModelSerializer):
    _current_status = StatusSerializer(required=False, many=False)
    items = OrderItemField(many=True, read_only=True)

    class Meta:
        model = Order
        exclude = ('user',)


class AddToOrderSerializer(serializers.Serializer):
    items = serializers.ListField()
    quantity = serializers.ListField()

    class Meta:
        fields = ('items', 'quantity')

    def validate(self, attrs):
        for item in attrs['items']:
            try:
                Item.objects.get(id=item)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Item must exist to add it to an order!")
        return attrs

    def update(self, instance, validated_data):
        items = validated_data['items']
        quantities = validated_data['quantity']
        for index, item in enumerate(items):
            item = Item.objects.get(id=item)
            quantity = quantities[index]
            order_item, created = OrderItem.objects.get_or_create(order=instance, item=item)

            if quantity > 0 and created:
                order_item.quantity = quantity
                order_item.save()
            elif quantity >= 0 and not created:
                order_item.quantity += quantity
                order_item.save()
            else:
                order_item.delete()
        return instance

    def create(self, validated_data):
        raise NotImplementedError("Create method not supported on Add To Order Serializer")


class TagSerializer(TaggitSerializer, serializers.ModelSerializer):
    class Meta:
        model = Shop_Item_Tag


class SaveCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveCard


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('name', 'street', 'apt', 'city', 'state', 'zip')
        read_only_fields = ('type', 'user')

