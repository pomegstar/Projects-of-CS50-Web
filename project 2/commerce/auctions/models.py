from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bids(models.Model):
    bid = models.IntegerField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="bidder")
    blist = models.ForeignKey('A_listing', on_delete=models.CASCADE,
                               blank=True, null=True, related_name="blist")
    def __str__(self):
        return f"{self.bid}"


class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName


class A_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=1000)
    price = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True,
                              null=True, related_name="bidprice")
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watch")

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment = models.CharField(max_length=1000, null=True)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE,
                                  blank=True, null=True, related_name="commentor")
    listing = models.ForeignKey(A_listing, on_delete=models.CASCADE,
                                blank=True, null=True, related_name="listing")
    # listing= models.ManyToManyField(User, blank=True, null=True, related_name="listing")

    def __str__(self):
        return f"{self.commentor} comments on {self.listing}: {self.comment}"
