from rest_framework import serializers
from reddit.models import Post


class PostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super(PostSerializer, self).create({**validated_data, 'author': self.context['request'].user})

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'publish_date', 'upvotes', 'downvotes']

