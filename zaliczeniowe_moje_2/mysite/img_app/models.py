from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class Image(models.Model):
    image = models.ImageField(upload_to='data_images/')
    name = models.CharField(max_length=128)
    published = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='images')
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Image {self.name}'
