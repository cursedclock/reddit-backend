from rest_framework.viewsets import ModelViewSet

from reddit.serializers.subreddit import SubredditSerializer
from reddit.models import Subreddit


class SubredditViewSet(ModelViewSet):

    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer
