from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.conf import settings
import stripe
from main.main_models.order import Order
from main.serializers import OrderSerializer


class PlaceOrder(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
 
    def get(self, request):
        return Response({"error":"not a valid request"})
 
    def post(self, request):
        stripe.api_key = settings.STRIPE_API_KEY
        try:
            order = Order.objects.get(user=self.request.user, placed=False)
        except ObjectDoesNotExist:
            return Response("no open orders")

        card = request.POST['card']
        try:
            stripe_token = stripe.Token.create(
                card={
                    "number": card.get('number'),
                    "exp_month": card.get('expMonth'),
                    "exp_year": card.get('expYear'),
                    "cvc": card.get('cvc')
                },
            )

            charge = stripe.Charge.create(
                amount=order.total_price,
                currency="usd",
                source=stripe_token.get('id'),
                description="Order Number: {}".format(order.id)
            )
 
            response = charge
 
        except stripe.error.CardError, e:
            response = {
                'status': 'failed',
                'error': e
            }
            return Response(response)

        if response.get('status') == 'succeeded':
            order.place_order()
            order.save()
            if order.placed:
                order = OrderSerializer(order).data
                return Response({'charge': response, 'order': order})
            return Response({'error': 'order could not be placed!', 'details': response})

        return Response("Unknown error")
