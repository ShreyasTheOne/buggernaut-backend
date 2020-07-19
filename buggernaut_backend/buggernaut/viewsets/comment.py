from rest_framework import viewsets
from buggernaut.serializers import *
from buggernaut.models import *


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CommentPostSerializer
        else:
            return CommentGetSerializer
