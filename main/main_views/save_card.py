from rest_framework import generics
from main.main_models.save_card import SaveCard
from main.serializers import SaveCardSerializer


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SaveCardSerializer

    def get_object(self, *args, **kwargs):
        # self.request.user is going to be the logged in user
        # we are filtering all the saved card objects, that have a user
        # field that match the logged in user.
        card_qs = SaveCard.objects.filter(user=self.request.user)
        return card_qs


class CardList():
    pass


class DeleteCard():
    pass