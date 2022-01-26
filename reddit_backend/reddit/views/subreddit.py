from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reddit.utils.permissions import SubredditPermissions
from reddit.serializers.subreddit import SubredditSerializer
from reddit.models import Subreddit


class SubredditViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, SubredditPermissions)
    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer
