from django.db import models

from .users import User
from .post import Post


class BaseComment(models.Model):
    commentor = models.ForeignKey(to=User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    @property
    def upvotes(self):
        return CommentVote.objects.filter(is_upvote=True, post=self).count()

    @property
    def downvotes(self):
        return CommentVote.objects.filter(is_upvote=False, post=self).count()


class PostComment(BaseComment):
    on_post = models.ForeignKey(to=Post, related_name='comments', on_delete=models.CASCADE)


class CommentReply(BaseComment):
    on_comment = models.ForeignKey(to=BaseComment, related_name='comments', on_delete=models.CASCADE)


class CommentVote(models.Model):

    comment = models.ForeignKey(to=BaseComment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = [['comment', 'user']]

