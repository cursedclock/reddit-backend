from requests import Response
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from reddit.utils.permissions import PostPermissions
from reddit.serializers.post import PostSerializer
from reddit.models import Post


class PostViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    permission_classes = (IsAuthenticatedOrReadOnly, PostPermissions)
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'list', 'retrieve']:
            return PostSerializer
