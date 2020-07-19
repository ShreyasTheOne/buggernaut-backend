from rest_framework import viewsets

from buggernaut.models import Tag
from buggernaut.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer