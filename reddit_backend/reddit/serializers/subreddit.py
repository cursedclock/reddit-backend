from rest_framework import serializers
from reddit.models import Subreddit


class SubredditSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def create(self, validated_data):
        super(SubredditSerializer, self).create({**validated_data, 'owner': self.context['request'].user})

    class Meta:
        model = Subreddit
        fields = '__all__'
        read_only_fields = ['owner']
