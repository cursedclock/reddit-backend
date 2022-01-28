from rest_framework import serializers
from reddit.models import Post, PostVote


class PostSerializer(serializers.ModelSerializer):

    downvotes = serializers.IntegerField(read_only=True)
    upvotes = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return super(PostSerializer, self).create({**validated_data, 'author': self.context['request'].user})

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'publish_date', 'comment_count']


class PostVoteSerializer(serializers.Serializer):

    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    is_upvote = serializers.SerializerMethodField()

    def get_user(self, obj):
        return self.context['request'].user.id

    def get_post(self, obj):
        return self.context['post'].id

    def get_is_upvote(self, obj):
        return self.context['action'] == 'upvote'

    def save(self):
        instance, _ = PostVote.objects.update_or_create(user=self.data['user'], post=self.data['post'],
                                                        defaults={'is_upvote': self.data['is_upvote']})
        return instance
