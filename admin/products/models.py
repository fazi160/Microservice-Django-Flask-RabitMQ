from django.db import models

# Product model
class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

# User model (empty for now, you can add fields later)
class User(models.Model):
    pass
