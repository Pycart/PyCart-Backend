from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from main.main_models.stock_record import StockRecord
from main.serializers import StockRecordSerializer
from rest_framework import authentication, permissions
from django.conf import settings



class StockRecords(ListAPIView):
    queryset = StockRecord.objects.all()

    serializer_class = StockRecordSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    permission_classes = (permissions.IsAuthenticated,)
