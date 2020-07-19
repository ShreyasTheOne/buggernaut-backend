from rest_framework import serializers
from buggernaut.models import *


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
