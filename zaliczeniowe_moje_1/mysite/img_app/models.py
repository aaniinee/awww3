from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    name = models.CharField(max_length=128)
    width = models.IntegerField()
    height = models.IntegerField()
    artists = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Rectangle(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    color = models.CharField(max_length=128)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rectangle(pos=({self.x}, {self.y}), w={self.width}, h={self.height}, color={self.color})'

