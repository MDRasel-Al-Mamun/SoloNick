from django.db import models


class Contact(models.Model):
    STATUS = (
        ('New', "New"),
        ('Read', "Read"),
        ('Draft', "Draft"),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.SmallIntegerField(blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')

    def __str__(self):
        return self.name
