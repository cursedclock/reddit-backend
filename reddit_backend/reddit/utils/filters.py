from django.db.models import Count, Q, F
from rest_framework.filters import BaseFilterBackend


class SortPostsByUpvotesFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get('ordering')
        if ordering == 'upvotes':
            upvotes_count = Count('postvote', filter=Q(postvote__is_upvote=True))
            downvotes_count = Count('postvote', filter=Q(postvote__is_upvote=False))
            queryset = queryset.annotate(upvotes=upvotes_count).annotate(downvotes=downvotes_count)\
                       .annotate(popularity=F('upvotes')-F('downvotes')).order_by('-popularity')
        return queryset


class SortCommentByUpvotesFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get('ordering')
        if ordering == 'upvotes':
            upvotes_count = Count('commentvote', filter=Q(commentvote__is_upvote=True))
            downvotes_count = Count('commentvote', filter=Q(commentvote__is_upvote=False))
            queryset = queryset.annotate(upvotes=upvotes_count).annotate(downvotes=downvotes_count)\
                       .annotate(popularity=F('upvotes')-F('downvotes')).order_by('-popularity')
        return queryset
