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
<<<<<<< HEAD
from main.main_views.tags import TagList, HeaderTagList, SubheaderTagList
from main.main_views.admin_dashboard import *
from main.main_views.user_account import UserView
=======
from main.main_views.authentication import ShopLoginView, ShopLogoutView, ShopPasswordResetView, ShopSetPasswordView, \
    ShopPasswordResetConfirmView, ShopActivationView, ShopSetUsernameView, ShopUserView
>>>>>>> 75121e9e93be2f14abfd7fe6a8230ab1617a8a24

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'auth/me/', UserView.as_view(), name='user_details'),
    url(r'auth/', include('djoser.urls')),

    url(r'^$','main.views.api_root', name="api-root"),

    url(r'^items_list/$', ItemList.as_view(), name="items_list"),
    url(r'^items_search/$', ItemSearch.as_view(), name="items_search"),
    url(r'^items_detail/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='item-detail'),

    url(r'^tags_list/$', TagList.as_view(), name="tags_list"),
    url(r'^header_tags/$', HeaderTagList.as_view(), name="header_tags"),
    url(r'^subheader_tags/$', SubheaderTagList.as_view(), name="subheader_tags"),

    url(r'^admin_dashboard/items/$', AdminListCreateItem.as_view(), name="create_item"),
    url(r'^admin_dashboard/items/(?P<pk>[0-9]+)/$', AdminItemDetail.as_view(), name="item_detail_update"),
    url(r'^admin_dashboard/options/$', AdminListCreateOption.as_view(), name="create_option"),
    url(r'^admin_dashboard/options/(?P<pk>[0-9]+)/$', AdminOptionDetail.as_view(), name="option_detail_update"),
    url(r'^admin_dashboard/status/$', AdminListCreateStatus.as_view(), name="create_status"),
    url(r'^admin_dashboard/status/(?P<pk>[0-9]+)/$', AdminStatusDetail.as_view(), name="status_detail_update"),

    url(r'^allOrdersList/', OrdersView.as_view(), name="all_orders"),
    url(r'^recentOrdersList/', RecentOrdersView.as_view(), name="recent_orders"),

    #auth views
    url(r'^register/$', views.ShopLoginView.as_view()),
    url(r'^logout/$', views.ShopLogoutView.as_view()),
    url(r'^password_reset/$', views.ShopPasswordResetView.as_view()),
    url(r'^set_password/$', views.ShopSetPasswordView.as_view()),
    url(r'^password_reset_confirm/$', views.ShopPasswordResetConfirmView.as_view()),
    url(r'^activation_view/$', views.ShopActivationView.as_view()),
    url(r'^set_username/$', views.ShopSetUsernameView.as_view()),
    url(r'^user_view/$', views.ShopUserView.as_view()),





]
