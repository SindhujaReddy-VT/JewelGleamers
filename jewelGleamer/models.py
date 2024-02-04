from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Product class on the category page
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    url = models.ImageField(upload_to='images/')
    author = models.CharField(default='Sindhu')
    date_posted = models.DateTimeField(default=timezone.now)
    details = models.TextField(default='Made in 14k solid gold, the alloy gives our pieces its beautiful, subtle hue. '
                                       'Band Thickness: 1.0 mm')
    description = models.TextField(default='The Stacker is the white tee of rings. It is everyone go-to because there '
                                           'is nothing it cant go with. This 14k solid gold essential is the perfect '
                                           'starter ring or addition to anyone collection.')
    materials = models.TextField(default='14k Solid Gold Our 14k solid gold pieces are made to last forever. 14k gold '
                                         'will not oxidize or discolor, so you can wear your jewelry every day.')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jewelGleamer:item_detail', args=[self.id])


class Blogs(models.Model):
    description = models.TextField()


# Review Class
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.item.name

    def get_absolute_url(self):
        return reverse('jewelGleamer:item_detail', args=[self.item_id])


# Item Class for detailed view
class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    details = models.TextField()
    description = models.TextField()
    materials = models.TextField()
    urls = models.TextField()


# Image Class for urls
class Images(models.Model):
    url = models.CharField(max_length=200)


admin_user = {"username": "Admin", "password": "Admin"}
regular_user = {"username": "Sindhu", "password": "Sindhu"}

