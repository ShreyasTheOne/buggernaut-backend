from rest_framework import serializers
from .models import *


class ProjectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'wiki', 'members', 'deployed', 'created_at']
        read_only_fields = ['id', 'deployed' 'created_at']


class ProjectGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'wiki', 'members', 'deployed', 'created_at']
        read_only_fields = ['id', 'deployed' 'created_at']
        depth = 1


class IssuePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'project', 'assigned_to', 'reported_by', 'subject', 'description', 'priority', 'resolved',
                  'created_at']
        read_only_fields = ['id', 'resolved', 'created_at']

class IssueGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'project', 'assigned_to', 'reported_by', 'subject', 'description', 'priority', 'resolved',
                  'created_at']
        read_only_fields = ['id', 'resolved', 'created_at']
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'username', 'pk', 'enrolment_number', 'email', 'display_picture', 'is_superuser']
        # read_only_fields = ['username', 'first_name', 'last_name', 'pk']
