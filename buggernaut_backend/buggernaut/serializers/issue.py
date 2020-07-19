from rest_framework import serializers
from buggernaut.models import *


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