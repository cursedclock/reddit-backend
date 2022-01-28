from rest_framework import serializers
from reddit.models import CommentReply, PostComment, CommentVote


class CommentReplySerializer(serializers.ModelSerializer):
    downvotes = serializers.IntegerField(read_only=True)
    upvotes = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return super(CommentReplySerializer, self).create({**validated_data,
                                                           'on_comment': self.context['comment'],
                                                           'commentor': self.context['request'].user
                                                           })

    class Meta:
        model = CommentReply
        fields = '__all__'
        read_only_fields = ['on_comment', 'commentor']


class PostCommentSerializer(serializers.ModelSerializer):
    downvotes = serializers.IntegerField(read_only=True)
    upvotes = serializers.IntegerField(read_only=True)
    comments = CommentReplySerializer(read_only=True, many=True)

    def create(self, validated_data):
        return super(PostCommentSerializer, self).create({**validated_data, 'commentor': self.context['request'].user})

    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ['commentor']


class CommentVoteSerializer(serializers.Serializer):

    user = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    is_upvote = serializers.SerializerMethodField()

    def get_user(self, obj):
        return self.context['request'].user.id

    def get_post(self, obj):
        return self.context['comment'].id

    def get_is_upvote(self, obj):
        return self.context['action'] == 'upvote'

    def save(self):
        instance, _ = CommentVote.objects.update_or_create(user=self.data['user'], comment=self.data['post'],
                                                           defaults={'is_upvote': self.data['is_upvote']})
        return instance
