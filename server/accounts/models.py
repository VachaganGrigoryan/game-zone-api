from django.db import models


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    email = models.EmailField()
    mobile = models.TextField(max_length=100)


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    account_number = models.TextField()
    balance = models.TextField(max_length=100)
