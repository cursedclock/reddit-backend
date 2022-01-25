from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins, ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from reddit.serializers.subreddit import SubredditSerializer
from reddit.models import Subreddit


class SubredditViewSet(ModelViewSet):

    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer
