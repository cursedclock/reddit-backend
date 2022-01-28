from datetime import timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Count, Q

from reddit.utils.permissions import SubredditPermissions
from reddit.serializers.subreddit import SubredditSerializer
from reddit.models import Subreddit, Post


class SubredditViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, SubredditPermissions)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['name']
    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer

    @action(detail=False, methods=['GET'])
    def trending(self, request):
        recent_posts = Count('posts', filter=Q(posts__publish_date__gte=timezone.now()-timedelta(days=1)))
        queryset = self.get_queryset().annotate(recent_posts=recent_posts).order_by('-recent_posts')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
