from rest_framework import serializers
from reddit.models import Subreddit


class SubredditSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super(SubredditSerializer, self).create({**validated_data, 'owner': self.context['request'].user})

    class Meta:
        model = Subreddit
        fields = '__all__'
        read_only_fields = ['owner']
