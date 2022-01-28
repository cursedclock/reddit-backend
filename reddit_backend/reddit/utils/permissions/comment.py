from rest_framework.permissions import BasePermission
from reddit.models import Membership, Post, PostComment


class CommentPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user = request.user
            post = Post.objects.filter(id=request.body.get('on_post'))
            if not post:
                return False
            return Membership.objects.filter(user=user, subreddit=post.subreddit).exists()
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'reply':
            user = request.user
            post_comment = PostComment.objects.filter(id=request.body.get('on_comment'))
            if not post_comment:
                return False
            return Membership.objects.filter(user=user, subreddit=post_comment.on_post.subreddit).exists()
        else:
            return True
