from django.db import models

from .users import User
from .subreddit import Subreddit


class Post(models.Model):

    title = models.CharField(max_length=150)
    body = models.TextField(max_length=3000)
    author = models.ForeignKey(to=User, related_name='posts', null=True, on_delete=models.SET_NULL)
    subreddit = models.ForeignKey(to=Subreddit, related_name='posts', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    # TODO comments

