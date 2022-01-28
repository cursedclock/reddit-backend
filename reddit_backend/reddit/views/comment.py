from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from reddit.serializers.comment import PostCommentSerializer, CommentReplySerializer, CommentVoteSerializer
from reddit.models import PostComment


class CommentViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = PostComment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'list', 'retrieve']:
            return PostCommentSerializer
        elif self.action in ['upvote', 'downvote']:
            return CommentVoteSerializer
        elif self.action in ['reply']:
            return CommentReplySerializer

    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        if self.action in ['upvote', 'downvote']:
            context['comment'] = self.get_object()
            context['action'] = self.action
        elif self.action in ['reply']:
            context['comment'] = self.get_object()
        return context

    @action(detail=True, methods=['POST'])
    def reply(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['PUT'])
    def upvote(self, request, pk):
        return self._vote(request, pk)

    @action(detail=True, methods=['PUT'])
    def downvote(self, request, pk):
        return self._vote(request, pk)

    def _vote(self, request, pk):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
