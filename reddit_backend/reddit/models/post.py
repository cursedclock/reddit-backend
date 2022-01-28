from django.db import models

from .users import User
from .subreddit import Subreddit


class Post(models.Model):

    title = models.CharField(max_length=150)
    body = models.TextField(max_length=3000)
    author = models.ForeignKey(to=User, related_name='posts', null=True, on_delete=models.SET_NULL)
    subreddit = models.ForeignKey(to=Subreddit, related_name='posts', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)

    @property
    def upvotes(self):
        return PostVote.objects.filter(is_upvote=True, post=self).count()

    @property
    def downvotes(self):
        return PostVote.objects.filter(is_upvote=False, post=self).count()

    # TODO comments


class PostVote(models.Model):

    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = [['post', 'user']]
