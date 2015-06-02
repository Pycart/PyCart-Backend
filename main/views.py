from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from main.models import Item
from main.serializers import ItemSerializer
from rest_framework import status

# Create your views here.


class ItemList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        print request.DATA

        return self.create(request, *args, **kwargs)

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'items': reverse('items_list', request=request, format=format),
    })