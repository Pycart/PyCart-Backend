import decimal
import datetime
import json

from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from django.utils.http import urlquote
from model_mommy import mommy
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from main.main_models.item import Item
from main.main_models.order import Status, Order
from main.serializers import ItemSerializer


class AdminDashboardViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.option = mommy.make('main.Option')
        self.items = mommy.make('main.Item', make_m2m=True, _quantity=50, option=self.option)
        self.item = mommy.make('main.Item', make_m2m=True, option=self.option)
        self.item_json = ItemSerializer(self.item).data
        self.status = mommy.make('main.Status')

        self.admin_user = mommy.make('main.ShopUser')
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.reg_user = mommy.make('main.ShopUser')

        # Generate token for token auth based on the user in the requests
        self.admin_token = Token()
        self.admin_token.key = self.admin_token.generate_key()
        self.admin_token.user_id = self.admin_user.id
        self.admin_token.save()
        self.reg_token = Token()
        self.reg_token.key = self.reg_token.generate_key()
        self.reg_token.user_id = self.reg_user.id
        self.reg_token.save()

    def test_admin_create_item_view(self):
        Item.objects.get(id=self.item.id).delete()

        self.client.force_authenticate(self.admin_user, self.admin_token)
        request = self.client.post(reverse('create_item'), data=self.item_json, format='json')
        item = Item.objects.get(pk=52)

        self.assertEqual(request.status_code, 201)
        self.assertEqual(item.name, self.item_json['name'])
        self.assertEqual(item.description, self.item_json['description'])
        self.assertEqual(item.weight, decimal.Decimal(self.item_json['weight']))
        self.assertEqual(item.price, decimal.Decimal(self.item_json['price']))
        self.assertEqual(item.option.id, 1)

    def test_admin_create_view_as_reg_user(self):
        Item.objects.get(id=self.item.id).delete()

        self.client.force_authenticate(self.reg_user, self.reg_token)
        request = self.client.post(reverse('create_item'), data=self.item_json, format='json')

        self.assertEqual(request.status_code, 403)
        with self.assertRaises(ObjectDoesNotExist):
            Item.objects.get(pk=52)

    def test_admin_item_list(self):
        self.client.force_authenticate(self.admin_user, self.admin_token)
        request = self.client.get(reverse('create_item'))
        data = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual('count' in data, True)
        self.assertEqual('next' in data, True)
        self.assertEqual(len(data['results']), 25)

        for result in data['results']:
            self.assertEqual('id' in result, True)
            self.assertEqual('name' in result, True)
            self.assertEqual('description' in result, True)
            self.assertEqual('weight' in result, True)
            self.assertEqual('price' in result, True)
            self.assertEqual('option' in result, True)
            self.assertEqual('tags' in result, True)

    def test_admin_item_list_as_reg_user(self):
        self.client.force_authenticate(self.reg_user, self.reg_token)
        request = self.client.get(reverse('create_item'))
        self.assertEqual(request.status_code, 403)

    def test_admin_option_list(self):
        self.client.force_authenticate(self.admin_user, self.admin_token)
        request = self.client.get(reverse('create_option'))
        data = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['name'], self.option.name)

    def test_admin_option_list_as_reg_user(self):
        self.client.force_authenticate(self.reg_user, self.reg_token)
        request = self.client.get(reverse('create_option'))
        self.assertEqual(request.status_code, 403)

    def test_admin_option_detail(self):
        self.client.force_authenticate(self.admin_user, self.admin_token)
        request = self.client.get(reverse('option_detail_update', args=(1,)))
        data = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(data['id'], self.option.id)
        self.assertEqual(data['name'], self.option.name)

    def test_admin_option_detail_as_reg_user(self):
        self.client.force_authenticate(self.reg_user, self.reg_token)
        request = self.client.get(reverse('option_detail_update', args=(1,)))
        self.assertEqual(request.status_code, 403)

    def test_admin_status_list(self):
        self.client.force_authenticate(self.admin_user, self.admin_token)
        request = self.client.get(reverse('create_status'))
        data = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['status'], self.status.status)
        self.assertEqual(data['results'][0]['description'], self.status.description)

    def test_admin_status_list_as_reg_user(self):
        self.client.force_authenticate(self.reg_user, self.reg_token)
        request = self.client.get(reverse('create_status'))
        self.assertEqual(request.status_code, 403)

    def test_admin_status_detail(self):
        self.client.force_authenticate(self.admin_user, self.admin_token)
        request = self.client.get(reverse('status_detail_update', args=(1,)))
        data = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(data['status'], self.status.status)
        self.assertEqual(data['id'], self.status.id)
        self.assertEqual(data['description'], self.status.description)

    def test_admin_status_detail_as_reg_user(self):
        self.client.force_authenticate(self.reg_user, self.reg_token)
        request = self.client.get(reverse('status_detail_update', args=(1,)))
        self.assertEqual(request.status_code, 403)

class ItemTestCase(TestCase):
    def setUp(self):
        self.items = mommy.make('main.Item', make_m2m=True, _quantity=25)
        self.single_item_no_sales = mommy.make('main.Item', make_m2m=True)
        self.single_item_sold = mommy.make('main.Item', make_m2m=True)
        self.single_item_sold_multiple_times = mommy.make('main.Item', make_m2m=True)
        self.single_item_sold_old_orders = mommy.make('main.item', make_m2m=True)
        self.order_with_sold_item = mommy.make('main.Order', items=[self.single_item_sold], make_m2m=True)
        self.orders_with_single_item = mommy.make('main.Order', items=[self.single_item_sold_multiple_times], make_m2m=True, _quantity=25)

        old_date = timezone.now() - datetime.timedelta(days=60)
        self.old_orders = mommy.make('main.Order', items=[self.single_item_sold_old_orders], make_m2m=True, _quantity=25)
        for order in self.old_orders:
            order.date_placed = old_date
            order.save()

    def test_to_unicode(self):
        self.assertEqual(self.single_item_sold.name, str(self.single_item_sold))

    def test_number_sold(self):
        self.assertEqual(self.single_item_sold.number_sold, 1)
        self.assertEqual(self.single_item_sold_multiple_times.number_sold, 25)
        self.assertEqual(self.single_item_sold_old_orders.number_sold, 25)

    def test_best_selling(self):
        self.assertListEqual(list(Item.get_best_selling()), [self.single_item_sold_multiple_times,
                                                             self.single_item_sold_old_orders, self.single_item_sold])
        self.assertEqual(Item.get_best_selling()[0], self.single_item_sold_multiple_times)
        self.assertEqual(Item.get_best_selling()[1], self.single_item_sold_old_orders)

    def test_best_selling_recently(self):
        self.assertListEqual(list(Item.get_best_selling_recently()), [self.single_item_sold_multiple_times,
                                                                      self.single_item_sold])

class OptionTestCase(TestCase):
    def setUp(self):
        self.option = mommy.make('main.Option')

    def test_to_unicode(self):
        self.assertEqual(str(self.option), self.option.name)

class OrderTestCase(TestCase):
    def setUp(self):
        self.orders = mommy.make('main.Order', _quantity=20, make_m2m=True)
        self.old_order = mommy.make('main.Order', make_m2m=True)
        self.old_order.date_placed = timezone.now() - datetime.timedelta(days=45)
        self.single_order = mommy.make('main.Order', make_m2m=True)

    def test_to_unicode(self):
        self.assertEqual(str(self.single_order), str(self.single_order.id))

    def test_weight_set_automatically(self):
        for order in self.orders:
            self.assertEqual(type(order.weight), decimal.Decimal)
            self.assertNotEqual(order.weight, None)
            self.assertNotEqual(order.weight, 0.00)

            total_weight = decimal.Decimal()
            items = Order.objects.get(id=order.id).items.all()
            for item in items:
                total_weight += item.weight

            self.assertEqual(total_weight, order.weight)

    def test_total_price_set_automatically(self):
        for order in self.orders:
            self.assertEqual(type(order._total_price), decimal.Decimal)
            self.assertNotEqual(order.total_price, None)
            self.assertNotEqual(order.total_price, 0.00)

            total_price = decimal.Decimal()
            items = Order.objects.get(id=order.id).items.all()
            for item in items:
                total_price += item.price

            self.assertEqual(total_price, order.total_price)

    def test_recently_placed(self):
        for order in self.orders:
            self.assertEqual(order.recently_placed(), True)

    def test_recently_placed_with_old_order(self):
        self.assertEqual(self.old_order.recently_placed(), False)

    def test_setters_throw_exception(self):
        with self.assertRaises(AttributeError):
            self.old_order.total_price = decimal.Decimal(5.00)

        with self.assertRaises(AttributeError):
            self.old_order.last_modified = timezone.now()

        with self.assertRaises(AttributeError):
            self.old_order.weight = decimal.Decimal(1.25)

    def test_current_status_property(self):
        self.assertIsInstance(self.single_order.current_status, Status)

    def test_current_status_property_setter(self):
        old_last_modified = self.single_order.last_modified
        status = Status.objects.get(pk=1)
        self.single_order.current_status = status
        self.assertNotEqual(self.single_order.last_modified, old_last_modified)
        self.assertEqual(self.single_order.current_status, status)

class ShopUserTestCase(TestCase):
    def setUp(self):
        self.shop_user = mommy.make('main.ShopUser', first_name='Alice', last_name='Smith')

    def test_get_full_name(self):
        self.assertEqual(self.shop_user.get_full_name(), str(self.shop_user.first_name + ' ' + self.shop_user.last_name))

    def test_get_short_name(self):
        self.assertEqual(self.shop_user.get_short_name(), self.shop_user.first_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.shop_user.get_absolute_url(), "/users/{}/".format(urlquote(self.shop_user.email)))

    def test_email_user(self):
        subject = "Email Test"
        message = "Message for email test"
        from_email = "unit_test@localhost"
        self.shop_user.email_user(subject, message, from_email)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, subject)

class StatusTestCase(TestCase):
    def setUp(self):
        self.status = mommy.make('main.Status')

    def test_to_unicode(self):
        self.assertEqual(str(self.status), self.status.status)
