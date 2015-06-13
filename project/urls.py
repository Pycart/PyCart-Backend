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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from main.main_views.order_detail import OrderDetail
from main.main_views.user_dashboard import UserDetail
from main.main_views.item import ItemList, ItemSearch, ItemDetail
from main.main_views.order import OrdersView, RecentOrdersView, AddItemToOrderView, GetCart
from main.main_views.tags import TagList, HeaderTagList, SubheaderTagList
from main.main_views.admin_dashboard import *
from main.main_views.user_account import UserView
from main.main_views.user_list import ShopUserList
from main.main_views.save_card import CardDetail
from main.main_views.user_address import *
from main.main_views.stock_record_views import StockRecords


urlpatterns = [
    url(r'^$', 'main.views.api_root', name="api-root"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'auth/me/', UserView.as_view(), name='user_details'),
    url(r'auth/', include('djoser.urls')),

    # TODO: Remove these urls
    url(r'^items_list/$', ItemList.as_view(), name="items_list"),
    url(r'^items_detail/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='item_detail'),
    url(r'^items_search/$', ItemSearch.as_view(), name="items_search"),

    # TODO: Change front end to go to these urls instead
    # url(r'^items/$', ItemList.as_view(), name="items_list"),
    # url(r'^items/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='item_detail'),
    # url(r'^items/search/$', ItemSearch.as_view(), name="items_search"),


    # TODO: Remove these urls
    url(r'^tags_list/$', TagList.as_view(), name="tags_list"),
    url(r'^header_tags/$', HeaderTagList.as_view(), name="header_tags"),
    url(r'^subheader_tags/$', SubheaderTagList.as_view(), name="subheader_tags"),

    # TODO: Change front end to go to these urls instead
    # url(r'^tags/$', TagList.as_view(), name="tags_list"),
    # url(r'^tags/headers/$', HeaderTagList.as_view(), name="header_tags"),
    # url(r'^tags/subheaders/$', SubheaderTagList.as_view(), name="subheader_tags"),

    url(r'^admin_dashboard/items/$', AdminListCreateItem.as_view(), name="create_item"),
    url(r'^admin_dashboard/items/(?P<pk>[0-9]+)/$', AdminItemDetail.as_view(), name="item_detail_update"),
    url(r'^admin_dashboard/options/$', AdminListCreateOption.as_view(), name="create_option"),
    url(r'^admin_dashboard/options/(?P<pk>[0-9]+)/$', AdminOptionDetail.as_view(), name="option_detail_update"),
    url(r'^admin_dashboard/status/$', AdminListCreateStatus.as_view(), name="create_status"),
    url(r'^admin_dashboard/status/(?P<pk>[0-9]+)/$', AdminStatusDetail.as_view(), name="status_detail_update"),

    # TODO: Remove these urls
    url(r'^add_to_cart/$', AddItemToOrderView.as_view(), name="add_to_cart"),
    url(r'^get_cart/$', GetCart.as_view(), name="get_cart"),

    # TODO: Change front end to go to these urls instead
    # url(r'^cart/$', GetCart.as_view(), name="get_cart"),
    # url(r'^cart/add/$', AddItemToOrderView.as_view(), name="add_to_cart"),


    # TODO: Remove these urls
    url(r'^user_dashboard/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name="user_dashboard"),
    url(r'^allOrdersList/', OrdersView.as_view(), name="all_orders"),
    url(r'^recentOrdersList/', RecentOrdersView.as_view(), name="recent_orders"),
    url(r'^order_detail/(?P<pk>[0-9]+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^ShopUserList/', ShopUserList.as_view(), name="user_list"),


    # TODO: Change front end to go to these urls instead
    # url(r'^user/user_dashboard/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name="user_dashboard"),
    # url(r'^user/orders/$', OrdersView.as_view(), name="all_orders"),
    # url(r'^user/orders/recent/$', RecentOrdersView.as_view(), name="recent_orders"),
    # url(r'^user/orders/(?P<pk>[0-9]+)/$', OrderDetail.as_view(), name='order_detail'),


    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^saved_card/', CardDetail.as_view(), name="saved_card"),

    url(r'^user_adss/', UserAddress.as_view(), name='user_address'),
    url(r'^stock_record/$', StockRecords.as_view(), name="stock_record"),
]
