from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from reddit.utils.permissions import PostPermissions
from reddit.serializers.post import PostSerializer, PostVoteSerializer
from reddit.models import Post


class PostViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    permission_classes = (IsAuthenticatedOrReadOnly, PostPermissions)
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'list', 'retrieve']:
            return PostSerializer
        if self.action in ['upvote', 'downvote']:
            return PostVoteSerializer

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        if self.action in ['upvote', 'downvote']:
            context['post'] = self.get_object()
            context['action'] = self.action
        return context

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
