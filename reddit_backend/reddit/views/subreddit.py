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
from reddit.models import Subreddit, Membership


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
        queryset = self.filter_queryset(self.get_queryset()).annotate(recent_posts=recent_posts).order_by('-recent_posts')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def memberships(self, request):
        memberships = Membership.objects.filter(user=request.user).values('subreddit__id')
        queryset = self.filter_queryset(self.get_queryset().filter(id__in=memberships))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def join(self, request, pk):
        subreddit = self.get_object()
        user = request.user
        Membership.objects.get_or_create(subreddit=subreddit, user=user)
        return Response({'code': 'success'}, status=201)

    @action(detail=True, methods=['POST'])
    def leave(self, request, pk):
        subreddit = self.get_object()
        user = request.user
        membership = Membership.objects.filter(subreddit=subreddit, user=user).first()
        if membership:
            membership.delete()
        return Response({'code': 'success'}, status=204)
