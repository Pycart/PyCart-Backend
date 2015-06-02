from rest_framework import serializers

from main_models.item import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
