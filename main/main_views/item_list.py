from django.db.models import Q
import operator

from rest_framework import generics
from rest_framework import mixins
from main.models import Item
from main.paginators import CustomPageNumberPagination
from main.serializers import ItemSerializer


class ItemList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ItemSearch(generics.ListAPIView):

    serializer_class = ItemSerializer

    def get_queryset(self):
        search_terms = self.request.GET.getlist('search', None)
        print search_terms
        if not search_terms or '' in search_terms or ' ' in search_terms:
            return []
        results = reduce(operator.or_,
                         (Item.objects.filter
                          (Q(name__icontains=term) | Q(description__icontains=term) | Q(option__name__icontains=term))
                          for term in search_terms))
        return results
