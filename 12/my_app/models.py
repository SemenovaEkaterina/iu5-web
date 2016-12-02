from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    document_number = models.IntegerField()
    birthday = models.DateField()


class Bank(models.Model):
    name = models.CharField(max_length=70)
    address = models.CharField(max_length=100)


class Transaction(models.Model):
    user = models.ForeignKey('User')
    bank = models.ForeignKey('Bank')
    type = models.CharField(max_length=60)
    count = models.IntegerField()