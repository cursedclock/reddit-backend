from django.urls import path, include
from rest_framework import routers

from .views import UserRegistrationView, UserLoginView, UserProfileView
from .views.subreddit import SubredditViewSet


router = routers.SimpleRouter()

router.register('subreddit', SubredditViewSet)

url_patterns = [
    path('', include(router.urls)),
    path("auth/signup", UserRegistrationView.as_view()),
    path("auth/signin", UserLoginView.as_view()),
    path("profile", UserProfileView.as_view()),
]