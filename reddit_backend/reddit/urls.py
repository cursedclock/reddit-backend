from django.urls import path, include
from rest_framework import routers

from .views.users import UserRegistrationView, UserLoginView, UserProfileView, UserView
from .views.subreddit import SubredditViewSet
from .views.post import PostViewSet
from .views.comment import CommentViewSet


router = routers.SimpleRouter()

router.register('subreddit', SubredditViewSet)
router.register('post', PostViewSet)
router.register('comment', CommentViewSet)

url_patterns = [
    path('', include(router.urls)),
    path("auth/signup", UserRegistrationView.as_view()),
    path("auth/signin", UserLoginView.as_view(http_method_names=['post'])),
    path("user", UserView.as_view(http_method_names=['get'])),
    path("profile", UserProfileView.as_view()),
]