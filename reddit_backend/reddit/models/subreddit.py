from django.db import models

from .users import User


class Subreddit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='owned_subreddits')
    admins = models.ManyToManyField(to=User, related_name='administered_subreddits', blank=True)


class Membership(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(to=Subreddit, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'subreddit']]
