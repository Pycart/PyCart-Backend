import operator

from django.db.models import Q
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
        # Probably poorly performing algorithms ahead. May need performance review.
        # This was built purely for my own educational purposes and will probably be replaced with elastic search.

        search_terms = self.request.GET.getlist('search', None)

        # removing trailing slash on restangular calls
        search_terms[0] = search_terms[0].lower().replace('/', '')

        if not search_terms:
            return []

        terms = [term.split(" ") for term in search_terms][0]

        # Query that will go through each item to see if their name, description or options match contain the search terms
        results = reduce(operator.or_,
                         (Item.objects.filter
                          (Q(name__icontains=term) | Q(description__icontains=term) | Q(option__name__icontains=term))
                          for term in terms))

        # creating a list so I can index later
        # Couldn't find an easy way to index on a generator/queryset
        results = list(results)

        # Using enumerate so I can get the index, storing index at end of list for future reference
        # Concats the item name and the item description into one list, using that for the items weight in the result
        # TODO: Remove duplicate words from result_split prior ot sorting
        results_split = [t.name.lower().split() + t.description.lower().split() + list((x,)) for x, t in enumerate(results)]

        # <magic>
        # Builds weight for each term
        # Example: The search has 3 terms, Red, Shoes, Pants
        # Red would have a weight of 3 since it is the first word, shoes would be 2 and pants would be 1
        query_with_weights = [(x, len(search_terms[0].split()) - search_terms[0].split().index(x)) for x in terms]

        # This section will go through and weigh each item based on name and description weight.
        # This may be problematic if the description uses the key word multiple times.
        #  It could result in things being weighed incorrectly. See the example below for more details.
        # Example 2: 'red pants' is the query.
        # We have, in no particular order, a red shoe item, a blue pants item, a red pants item, a red swim trunks item.
        # Each items description is sweet {{ item.name }} bro
        # The resulting weight would be Red: 2, Pants: 1
        # However, the returned result would be, in this order, [Red Pants, Red Shoe, Red Swim Trunks, Blue Pants]
        get_weight = lambda x: ([weight for y, weight in query_with_weights if y==x] or [0])[0]
        sorted_results = sorted([(l, sum([(get_weight(m)) for m in l])) for l in results_split], key=lambda lst: lst[1], reverse=True)
        # </magic>

        # Using the index stored from before I am able to access the original results list in order and
        #  create a new list that is now sorted based on the weight of each item in the search.
        # I am planning to expand this purely for educational purposes to include tags in the weighing and filtering process.
        final_sorted = [results[result[0][-1]] for result in sorted_results]
        return final_sorted
