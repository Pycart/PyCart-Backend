class AddOrRemoveItem(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def put(self, request, pk, format=None):
        pass
        #puts item into order, creates order object if it doesn't exsist

    def delete(self, request, pk, format=None):
        pass
        #removes items from order if order exists