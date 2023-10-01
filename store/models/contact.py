from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return self.name