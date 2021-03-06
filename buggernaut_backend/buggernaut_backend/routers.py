from rest_framework import routers
from buggernaut.viewsets import *

router1 = routers.DefaultRouter()

router1.register(r'projects', ProjectViewSet)
router1.register(r'issues', IssueViewSet)
router1.register(r'users', UserViewSet)
router1.register(r'images', ImageViewSet)
router1.register(r'comments', CommentViewSet)
router1.register(r'tags', TagViewSet)


