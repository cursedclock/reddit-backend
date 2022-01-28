from django.urls import path, include
from rest_framework import routers

from .views.users import UserRegistrationView, UserLoginView, UserProfileView
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
    path("auth/signin", UserLoginView.as_view()),
    path("profile", UserProfileView.as_view()),
]