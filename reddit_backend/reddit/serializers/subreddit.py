from rest_framework import serializers
from reddit.models import Subreddit


class SubredditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subreddit
        fields = '__all__'
