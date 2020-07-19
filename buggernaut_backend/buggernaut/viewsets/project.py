import os
import threading

from django.http import Http404
from django_filters import rest_framework as filters

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from buggernaut_backend.settings import BASE_DIR

from buggernaut.mailingSystem import Mailer
from buggernaut.serializers import *
from buggernaut.models import *

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['deployed', 'slug']

    def perform_create(self, serializer):
        project = serializer.save()

        mailerInstance = Mailer()
        link = "http://localhost:3000/projects/" + project.slug
        x = threading.Thread(target=mailerInstance.newProjectUpdate, args=(project.title, link, project.members.all()))
        x.start()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial":
            return ProjectPostSerializer
        else:
            return ProjectGetSerializer

    @action(methods=['get', ], detail=False, url_path='verify', url_name='verify',
            permission_classes=[IsAuthenticated])
    def check_slug(self, request):
        slug = self.request.query_params.get('slug')
        try:
            Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return Response({"status": "Available"}, status=status.HTTP_202_ACCEPTED)
        return Response({"status": "Taken"}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['get', ], detail=True, url_path='issues', url_name='issues',
            permission_classes=[IsAuthenticated])
    def get_issues(self, request, pk):

        try:
            issues_list = Issue.objects.filter(project=pk)
        except Issue.DoesNotExist:
            return Response(data="This project does not exist", status=status.HTTP_204_NO_CONTENT)

        ser = IssueGetSerializer(issues_list, many=True)
        return Response(ser.data)

    @action(methods=['patch', ], detail=True, url_path='update-team', url_name='update-team',
            permission_classes=[IsAuthenticated])
    def update_team(self, request, pk):
        project = Project.objects.get(pk=pk)
        members_list = self.request.data["members"]
        project.members.clear()
        for member in members_list:
            project.members.add(member)
        project.save()
        ser = ProjectGetSerializer(project)
        return Response(ser.data)

    @action(methods=['get', ], detail=True, url_path='deploy', url_name='deploy',
            permission_classes=[IsAuthenticated])
    def deploy_project(self, request, pk):
        project = Project.objects.get(pk=pk)

        if request.user.is_superuser or request.user in project.members.all():
            pass
        else:
            return Response({"Status": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        if not Issue.objects.filter(project=project, resolved=False):
            project.deployed = True
            project.save()

            mailer = Mailer()
            x = threading.Thread(target=mailer.deployProject,
                                 args=(project.title,
                                       request.user.full_name,
                                       project.members.all()))
            x.start()

            return Response({'Status': 'Project successfully deployed'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Status': 'All issues are not resolved for this project'})

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            pass
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            instance = self.get_object()
            editor = instance.editorID
            images = Image.objects.filter(editorID=editor)

            for i in images:
                i.delete()
                url_tbd = BASE_DIR + i.url.url
                os.remove(url_tbd)

            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)