from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="user")
    post = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}"


class Follow(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE,
                            blank=True, null=True, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True, related_name="follower")

    def __str__(self):
        return f"{self.usr} is following {self.follower}"


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True, related_name="liker")
    liked_post = models.ForeignKey(Posts, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name="liked")

    def __str__(self):
        return f"{self.liker} likes {self.liked_post}"
