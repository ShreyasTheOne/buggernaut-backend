import json

from rest_framework import viewsets
from buggernaut.models import *
import requests
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from buggernaut.serializers import *
from django_filters import rest_framework as filters
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout


# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['deployed']

    @action(methods=['get', ], detail=True, url_path='issues', url_name='issues', permission_classes=[IsAuthenticated])
    def get_issues(self, request, pk):

        try:
            issues_list = Issue.objects.filter(project=pk)
        except Issue.DoesNotExist:
            return Response({'Empty': 'No Issues for this project yet'}, status=status.HTTP_204_NO_CONTENT)

        ser = IssueSerializer(issues_list, many=True)
        # ser = UserSerializer(user)
        return Response(ser.data)

    @action(methods=['get', ], detail=True, url_path='team', url_name='team')
    def get_team_members(self, request, pk):
        project = Project.objects.get(pk=pk)
        members_list = project.members

        ser = UserSerializer(members_list, many=True)
        return Response(ser.data)

    @action(methods=['patch', ], detail=True, url_path='deploy', url_name='deploy')
    # @permission_classes([IsTeamMemberOrAdmin])
    def deploy_project(self, request, pk):
        project = Project.objects.get(pk=pk)

        if not Issue.objects.filter(project=project, resolved=False):
            project.deployed = True
            project.save()
            return Response({'Success': 'Project successfully deployed'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Error': 'All issues are not resolved for this project'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    # @permission_classes([IsAdmin])
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['reported_by', 'assigned_to']

    @action(methods=['patch', ], detail=True, url_path='resolve', url_name='resolve')
    # @permission_classes([IsReportedByOrTeamMemberOrAdmin])
    def resolve(self, request, pk):
        issue = Issue.objects.get(pk=pk)
        issue.resolved = True
        issue.save()

        ser = IssueSerializer(issue)
        return Response(ser.data)

    @action(methods=['patch', ], detail=True, url_path='assign', url_name='assign')
    # @permission_classes([IsTeamMemberOrAdmin])
    def assign_issue(self, request, pk):
        assign_to = self.request.query_params.get('assign_to')
        issue = Issue.objects.get(pk=pk)

        if User.objects.get(pk=assign_to) in issue.project.members.all():
            ser = IssueSerializer(issue, data={'assigned_to': assign_to}, partial=True)

            if ser.is_valid():
                ser.save()
                return Response({'status': 'Assignment Successful'}, status=status.HTTP_202_ACCEPTED)

        else:
            return Response({'Error': 'User not a team member'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post', 'options', ], detail=False, url_name="onlogin", url_path="onlogin", permission_classes=[AllowAny])
    def on_login(self, request):

        ode = self.request.data
        code = ode["code"]

        # GET AUTHORIZATION CODE
        url = "https://internet.channeli.in/open_auth/token/"
        data = {
            'client_id': 'uj0edatgcr0kBx1OZECybxsXQZvDh63s2NSwE38t',
            'client_secret': 'roWePxnlQuNYEXWOsijvzp3f39FyIDSpl0ye3QNtMsmMxUTg4US5Y8Ex8QvdDQPaklWmJwpv6n3CjubFYF3G8hnER3qMxxHduZgcaNpa3jHnVIPQqqC5PvEJGBmxDNI2',
            'grant_type': 'authorization_code',
            'redirect_url': 'http://localhost:3000/onlogin',
            'code': code
        }
        user_data = requests.post(url=url, data=data).json()

        ac_tok = user_data['access_token']
        # GET ACCESS TOKEN
        headers = {
            'Authorization': 'Bearer ' + ac_tok,
        }
        user_data = requests.get(url="https://internet.channeli.in/open_auth/get_user_data/", headers=headers).json()

        # return Response(user_data)
        # CHECK IF USER EXISTS

        try:
            user = User.objects.get(enrolment_number=user_data["student"]["enrolmentNumber"])
        except User.DoesNotExist:
            # CHECK IMG MEMBER OR NOT
            in_img = False
            for role in user_data["person"]["roles"]:
                if role["role"] == "Maintainer":
                    in_img = True
                    break

            if in_img:
                # CREATE USER
                enrolNum = user_data["student"]["enrolmentNumber"]
                email = user_data["contactInformation"]["instituteWebmailAddress"]

                name = (user_data["person"]["fullName"]).split()
                firstName = name[0]
                fullName = user_data["person"]["fullName"]

                is_admin = False
                if user_data["student"]["currentYear"] >= 4:
                    is_admin = True

                newUser = User(enrolment_number=enrolNum, email=email, first_name=firstName, username=fullName,
                               is_superuser=is_admin, access_token=ac_tok)
                newUser.save()
                login(request=request, user=newUser)
                # ser = UserSerializer(newUser)
                return Response({"status": "user created", "access_token": ac_tok}, status=status.HTTP_202_ACCEPTED)
            else:
                # SORRY YOU CAN'T USE THIS
                return Response({"status": "user not in IMG"}, status=status.HTTP_401_UNAUTHORIZED)

        user.access_token = ac_tok
        user.save()
        login(request=request, user=user)
        # request.session["user"] = "dingo"
        return Response({"status": "user exists", "access_token": ac_tok})

    @action(methods=['post', 'options', ], detail=False, url_name="login", url_path="login", permission_classes=[AllowAny])
    def pre_login(self, request):
        # print({"hello":"o"})
        data = self.request.data
        token = data["access_token"]

        try:
            user = User.objects.get(access_token=token)
        except User.DoesNotExist:
            return Response({"status": "user does not exist in database"})

        # LOGIN
        login(request=request, user=user)
        # request.session["user"] = user
        return Response({"status": "user found"}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['get', 'options', ], detail=False, url_name="test", url_path="test", permission_classes=[AllowAny])
    def test(self, request):
        if request.user.is_authenticated:
            return Response({"detail": request.user.enrolment_number}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"detail": "Not authenticated"})
