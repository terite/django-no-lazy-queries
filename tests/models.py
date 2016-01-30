from django.db import models


class Account(models.Model):
    pass


class Profile(models.Model):
    account = models.OneToOneField('Account', related_name='profile')


class Order(models.Model):
    purchaser = models.ForeignKey('Account', related_name='orders')
    referer = models.ForeignKey('Account', related_name='referals', null=True)
