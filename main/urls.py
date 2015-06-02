from django.conf.urls import include, url
from django.contrib import admin
from views import ItemList

urlpatterns = [
        url(r'^$', ),
        url(r'^tasks$', ItemList.as_view(), name="items_list"),
    ]