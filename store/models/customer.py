from django.db import models
from django.db.models import CharField


class Customer(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=30)

    def register(self):
        self.save()

    def __str__(self):
        return self.name

    def isExists(self):
        if Customer.objects.filter(password=self.password):
            return True

        return False
