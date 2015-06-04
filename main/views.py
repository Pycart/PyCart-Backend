from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    response = {}
    if request.user.is_authenticated():
        response['all-orders'] = reverse('all_orders', request=request, format=format)
        response['recent-orders'] = reverse('recent_orders', request=request, format=format)
    response['items'] = reverse('items_list', request=request, format=format)
    return Response(response)
