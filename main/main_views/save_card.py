from rest_framework import generics
from main.models import SaveCard
from main.serializers import SavedCardSerializer
from rest_framework import authentication
from django.conf import settings


class CardDetail(generics.RetrieveUpdateAPIView):
    serializer_class = SavedCardSerializer
    queryset = SaveCard.objects.all()

    authentication_classes = (authentication.TokenAuthentication, )
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    # def get_object(self, *args, **kwargs):
    #     # self.request.user is going to be the logged in user
    #     # we are filtering all the saved card objects, that have a user
    #     # field that match the logged in user.
    #     card_qs = SaveCard.objects.filter(user=self.request.user).first()
    #     # card_qs = SaveCard.objects.get(user=self.request.user)
    #     return card_qs


class CardList(generics.ListAPIView):
    serializer_class = SavedCardSerializer

    def get_queryset(self):
        # Should return all cards that the user has saved successfully.
        return SaveCard.objects.filter(user=self.request.user)


class DeleteCard():
    pass