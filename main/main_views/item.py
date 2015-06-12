import operator

from django.db.models import Q
from rest_framework import generics
from rest_framework import mixins

from main.main_models.item import Option
from main.models import Item
from main.paginators import CustomPageNumberPagination
from main.serializers import ItemSerializer, OptionSerializer, ItemDetailSerializer


class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class OptionList(generics.ListAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


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
        # Probably poorly performing algorithms ahead. May need performance review.
        # This was built purely for my own educational purposes and will probably be replaced with elastic search.

        search_terms = self.request.GET.getlist('search', None)

        if not search_terms:
            return []

        # removing trailing slash on restangular calls
        search_terms[0] = search_terms[0].lower().replace('/', '')

        terms = [term.split(" ") for term in search_terms][0]

        # Query that will go through each item to see if their name, description or options match contain the search terms
        results = reduce(operator.or_,
                         (Item.objects.filter
                          (Q(name__icontains=term) | Q(description__icontains=term))
                          for term in terms))

        # Using enumerate so I can get the index, storing index at end of list for future reference
        # Concats the item name and the item description into one list, using that for the items weight in the result
        results_split = [list(set(item.name.lower().split() + item.description.lower().split() + list((index,))))
                         for index, item in enumerate(results)]

        item = Item()
        # <magic>
        # Builds weight for each term
        # Example: The search has 3 terms, Red, Shoes, Pants
        # Red would have a weight of 3 since it is the first word, shoes would be 2 and pants would be 1
        query_with_weights = [(term, len(search_terms[0].split()) - search_terms[0].split().index(term))
                              for term in terms]

        # This section will go through and weigh each item based on name and description weight.
        # This may be problematic if the description uses the key word multiple times.
        #  It could result in things being weighed incorrectly. See the example below for more details.
        # Example 2: 'red pants' is the query.
        # We have, in no particular order, a red shoe item, a blue pants item, a red pants item, a red swim trunks item.
        # Each items description is sweet {{ item.name }} bro
        # The resulting weight would be Red: 2, Pants: 1
        # However, the returned result would be, in this order, [Red Pants, Red Shoe, Red Swim Trunks, Blue Pants]
        get_weight = lambda x: ([weight for y, weight in query_with_weights if y == x] or [0])[0]
        sorted_results = sorted([(item, sum([(get_weight(term)) for term in item])) for item in results_split],
                                key=lambda lst: lst[1], reverse=True)
        # </magic>

        # Using the index stored from before I am able to access the original results list in order and
        #  create a new list that is now sorted based on the weight of each item in the search.
        # I am planning to expand this purely for educational purposes to include tags in the weighing and filtering process.
        all_results = [results[result[0][result[0].index(term)]] for result in sorted_results for term in result[0] if
                        type(term) is int]

        # Gets the top level item for each sub item that hit in the results. Then returns only the one top level item to prevent duplicates
        filtered_and_sorted = list(set([Item.objects.get(id=item.get_top_level_item().id) for item in all_results if item.is_variant]))
        return filtered_and_sorted
