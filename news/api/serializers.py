from rest_framework import serializers
from news.models import News, Comment, Truth, Hashtag


class NewsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    true_count = serializers.SerializerMethodField()
    false_count = serializers.SerializerMethodField()
    true_false_rate = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    hashtags = serializers.StringRelatedField(many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments', 'true_count', 'false_count', 'true_false_rate', 'hashtags', 'popularity', 'is_flagged']

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

    def get_true_count(self, obj):
        return obj.truths.filter(is_true=True).count()

    def get_false_count(self, obj):
        return obj.truths.filter(is_true=False).count()

    def get_true_false_rate(self, obj):
        if obj.truths.count() == 0:
            return 0
        return round((obj.truths.filter(is_true=True).count() / obj.truths.count()) * 100, 2)


class CreateNewsSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ['title', 'content', 'author']


class UpdateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content']


class DeleteNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author',
                  'news', 'created_at', 'updated_at']


class CreateCommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['content', 'author', 'news']


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


class DeleteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id']


class TruthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truth
        fields = ['id', 'is_true', 'voter', 'news', 'created_at', 'updated_at']


class CreateTruthSerializer(serializers.ModelSerializer):
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Truth
        fields = ['is_true', 'voter', 'news']


class DeleteTruthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truth
        fields = ['id']
