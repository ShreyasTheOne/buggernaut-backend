from rest_framework import serializers
from buggernaut.models import *


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'issue', 'commented_by', 'content',]


class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'issue', 'commented_by', 'content', 'created_at',]
        depth = 1