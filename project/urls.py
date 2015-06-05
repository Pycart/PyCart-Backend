"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main.main_views.item_list import ItemList, ItemSearch
from main.main_views.item_detail import ItemDetail
from main.main_views.order import OrdersView, RecentOrdersView
from main.main_views.tags import TagList, HeaderTagList, SubheaderTagList
from main.main_views.admin_dashboard import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'auth/', include('djoser.urls')),

    url(r'^$','main.views.api_root', name="api-root"),

    url(r'^items_list/$', ItemList.as_view(), name="items_list"),
    url(r'^items_search/$', ItemSearch.as_view(), name="items_search"),
    url(r'^items_detail/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='item-detail'),

    url(r'^tags_list/$', TagList.as_view(), name="tags_list"),
    url(r'^header_tags/$', HeaderTagList.as_view(), name="header_tags"),
    url(r'^subheader_tags/$', SubheaderTagList.as_view(), name="subheader_tags"),

    url(r'^admin_create_item/$', AdminCreateItem.as_view(), name="admin_create_item"),
    url(r'^admin_list_item/$', AdminItemList.as_view(), name="admin_list_item"),
    url(r'^admin_item_detail/$', AdminItemDetail.as_view(), name="admin_item_detail"),
    url(r'^admin_create_option/$', AdminCreateOption.as_view(), name="admin_create_option"),
    url(r'^admin_list_option/$', AdminOptionList.as_view(), name="admin_list_option"),
    url(r'^admin_item_option/$', AdminOptionDetail.as_view(), name="admin_item_option"),

    url(r'^allOrdersList/', OrdersView.as_view(), name="all_orders"),
    url(r'^recentOrdersList/', RecentOrdersView.as_view(), name="recent_orders"),
]
