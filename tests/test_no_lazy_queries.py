from contextlib2 import contextmanager
from django.test import TestCase

from nolazyqueries import no_lazy_queries

from .models import Account, Order, Profile


class NoLazyQueriesTest(TestCase):

    def setUp(self):
        super(NoLazyQueriesTest, self).setUp()

        self.account = Account.objects.create()
        self.profile = Profile.objects.create(account=self.account)
        self.order = Order.objects.create(purchaser=self.account)

    @contextmanager
    def assert_lazy_error(self, model_property, num_queries=0):
        message = '^Cannot lazy load %s' % model_property
        with self.assertNumQueries(num_queries):
            with self.assertRaisesRegexp(AttributeError, message):
                yield

    def test_reverse_one_to_one(self):
        account = Account.objects.get(pk=self.account.pk)

        with self.assert_lazy_error('Account.profile'):
            with no_lazy_queries():
                account.profile

        account = (Account.objects
                   .select_related('profile')
                   .get(pk=self.account.pk))

        with self.assertNumQueries(0):
            with no_lazy_queries():
                self.assertEqual(account.profile, self.profile)

    def test_one_to_one(self):
        profile = Profile.objects.get(pk=self.profile.pk)

        with self.assert_lazy_error('Profile.account'):
            with no_lazy_queries():
                profile.account

        profile = (Profile.objects
                   .select_related('account')
                   .get(pk=self.profile.pk))

        with self.assertNumQueries(0):
            with no_lazy_queries():
                self.assertEqual(profile.account, self.account)

    def test_foreign_key(self):
        order = Order.objects.get(pk=self.order.pk)

        with self.assert_lazy_error('Order.purchaser'):
            with no_lazy_queries():
                order.purchaser

        order = Order.objects.select_related('purchaser').get(pk=self.order.pk)

        with self.assertNumQueries(0):
            with no_lazy_queries():
                self.assertEqual(order.purchaser, self.account)
