from rest_framework import serializers
from .models import *


class ProjectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'wiki', 'image', 'members', 'deployed', 'created_at', 'editorID']
        read_only_fields = ['id', 'deployed' 'created_at']


class ProjectGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'wiki', 'image', 'members', 'deployed', 'created_at', 'editorID']
        read_only_fields = ['id', 'deployed' 'created_at']
        depth = 1


class IssuePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'project', 'assigned_to', 'reported_by', 'resolved_by', 'subject', 'description', 'priority',
                  'resolved', 'created_at', 'tags', 'editorID']
        read_only_fields = ['id', 'created_at']


class IssueGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'project', 'assigned_to', 'reported_by', 'resolved_by', 'subject', 'description', 'priority',
                  'resolved', 'created_at', 'tags', 'editorID']
        read_only_fields = ['id', 'created_at']
        depth = 1


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name',]


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'issue', 'commented_by', 'content',]


class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'issue', 'commented_by', 'content', 'created_at',]
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'first_name', 'username', 'pk', 'enrolment_number', 'email', 'display_picture',
                  'is_superuser', 'banned']
        # read_only_fields = ['username', 'first_name', 'last_name', 'pk']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'editorID']
