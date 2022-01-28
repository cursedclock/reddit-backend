from rest_framework.permissions import BasePermission
from reddit.models import Membership


class PostPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user = request.user
            subreddit = request.body.get('subreddit')
            if not subreddit:
                return False
            return Membership.objects.filter(user=user, subreddit=subreddit).exists()
        else:
            return True
