import os
import threading

from django.http import Http404
from django_filters import rest_framework as filters

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from buggernaut.models import Project
from buggernaut_backend.settings import BASE_DIR

from buggernaut.permissions import IsTeamMemberOrAdmin
from buggernaut.mailingSystem import Mailer
from buggernaut.serializers import *
from buggernaut.models import *

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['reported_by', 'assigned_to']

    def perform_create(self, serializer):
        issue_instance = serializer.save()
        project = issue_instance.project
        link = "http://localhost:3000/projects/" + project.slug
        mailer = Mailer()
        x = threading.Thread(target=mailer.newBugReported,
                             args=(project.title,
                                   link,
                                   issue_instance.reported_by.full_name,
                                   issue_instance.subject,
                                   project.members.all()))
        x.start()

    def get_serializer_class(self):
        if self.action == "create":
            return IssuePostSerializer
        else:
            return IssueGetSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            issue = self.get_object()
            project = issue.project
            user = self.request.user

            if user.is_superuser or user == issue.reported_by or user in project.members.all():
                pass
            else:
                return Response({"Status": "Not authorized"})

            link = "http://localhost:3000/projects/" + project.slug
            editor = issue.editorID
            images = Image.objects.filter(editorID=editor)

            for i in images:
                i.delete()
                url_tbd = BASE_DIR + i.url.url
                os.remove(url_tbd)

            mailer = Mailer()
            x = threading.Thread(target=mailer.bugStatusChanged,
                                 args=(project.title,
                                       link,
                                       issue.subject,
                                       "deleted",
                                       request.user.full_name,
                                       project.members.all()))
            x.start()
            self.perform_destroy(issue)

        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', ], detail=True, url_path='resolve-or-reopen', url_name='resolve-or-reopen',
            permission_classes=[IsAuthenticated])
    def resolve_or_reopen(self, request, pk):
        user_instance = self.request.user
        issue = Issue.objects.get(pk=pk)

        if user_instance.is_superuser or user_instance == issue.reported_by or user_instance in issue.project.members.all():
            pass
        else:
            return Response({"Status": "Not authorized"})

        if issue.resolved:
            issue.resolved = False
        else:
            issue.resolved = True

        issue.resolved_by = user_instance;
        issue.save()

        project = issue.project
        link = "http://localhost:3000/projects/" + project.slug
        mailer = Mailer()

        if issue.resolved:
            x = threading.Thread(target=mailer.bugStatusChanged,
                                 args=(project.title,
                                       link,
                                       issue.subject,
                                       "resolved",
                                       request.user.full_name,
                                       project.members.all()))
        else:
            x = threading.Thread(target=mailer.bugStatusChanged,
                                 args=(project.title,
                                       link,
                                       issue.subject,
                                       "reopened",
                                       request.user.full_name,
                                       project.members.all()))
        x.start()
        ser = IssueGetSerializer(issue)
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(methods=['get', ], detail=True, url_path='assign', url_name='assign',
            permission_classes=[IsTeamMemberOrAdmin])
    def assign_issue(self, request, pk):
        assign_to = self.request.query_params.get('assign_to')
        issue = Issue.objects.get(pk=pk)

        try:
            user = User.objects.get(pk=assign_to)
        except User.DoesNotExist:
            return Response({'Detail': 'User does not exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if user in issue.project.members.all():
            issue.assigned_to = user
            issue.save()

            assignment_link = "http://localhost:3000/mypage?show=my-assignments"
            project_instance = issue.project
            assigned = issue.assigned_to

            mailer = Mailer()
            x = threading.Thread(target=mailer.bugAssigned,
                                 args=(project_instance.title,
                                       assignment_link,
                                       issue.subject,
                                       assigned.full_name,
                                       assigned.email))
            x.start()

            return Response({'Detail': 'Assignment Successful'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Detail': 'User not a team member'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['get', ], detail=True, url_path='comments', url_name='comments',
            permission_classes=[IsAuthenticated])
    def get_comments(self, request, pk):

        try:
            comments_list = Comment.objects.filter(issue=pk)
        except Comment.DoesNotExist:
            return Response({'Empty': 'No comments for this issue'}, status=status.HTTP_204_NO_CONTENT)

        ser = CommentGetSerializer(comments_list, many=True)
        return Response(ser.data)
