import json

from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
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
    # serializer_class = self.get_s
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['deployed', 'slug']

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial":
            return ProjectPostSerializer
        else:
            return ProjectGetSerializer

    @action(methods=['get', ], detail=False, url_path='verify', url_name='verify', permission_classes=[IsAuthenticated])
    def check_slug(self, request):
        slug = self.request.query_params.get('slug')
        print(slug)
        try:
            Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return Response({"status": "Available"}, status=status.HTTP_202_ACCEPTED)

        return Response({"status": "Taken"}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['get', ], detail=True, url_path='issues', url_name='issues', permission_classes=[IsAuthenticated])
    def get_issues(self, request, pk):

        try:
            issues_list = Issue.objects.filter(project=pk)
        except Issue.DoesNotExist:
            return Response({'Empty': 'No Issues for this project yet'}, status=status.HTTP_204_NO_CONTENT)

        ser = IssueGetSerializer(issues_list, many=True)
        # ser = UserSerializer(user)
        return Response(ser.data)

    @action(methods=['patch', ], detail=True, url_path='update-team', url_name='update-team', permission_classes=[IsAuthenticated])
    def update_team(self, request, pk):
        project = Project.objects.get(pk=pk)
        members_list = self.request.data["members"]
        # print("HEO")
        project.members.clear()
        for member in members_list:
            project.members.add(member)
        # print("HELLO")
        project.save()

        ser = ProjectGetSerializer(project)
        return Response(ser.data)

    @action(methods=['patch', ], detail=True, url_path='deploy', url_name='deploy')
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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['reported_by', 'assigned_to']

    def get_serializer_class(self):
        if self.action == "create":
            return IssuePostSerializer
        else:
            return IssueGetSerializer

    @action(methods=['get', ], detail=True, url_path='resolve-or-reopen', url_name='resolve-or-reopen', permission_classes=[IsTeamMemberOrAdmin])
    def resolve_or_reopen(self, request, pk):
        user = self.request.user;
        issue = Issue.objects.get(pk=pk)
        if issue.resolved:
            issue.resolved = False
        else:
            issue.resolved = True

        issue.resolved_by = user;
        issue.save()

        ser = IssueGetSerializer(issue)
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(methods=['get', ], detail=True, url_path='assign', url_name='assign', permission_classes=[IsTeamMemberOrAdmin])
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
            return Response({'Detail': 'Assignment Successful'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Detail': 'User not a team member'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['get', ], detail=True, url_path='comments', url_name='comments', permission_classes=[IsAuthenticated])
    def get_comments(self, request, pk):

        try:
            comments_list = Comment.objects.filter(issue=pk)
        except Comment.DoesNotExist:
            return Response({'Empty': 'No comments for this issue'}, status=status.HTTP_204_NO_CONTENT)

        ser = CommentGetSerializer(comments_list, many=True)
        # ser = UserSerializer(user)
        return Response(ser.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post', 'options', ], detail=False, url_name="onlogin", url_path="onlogin",
            permission_classes=[AllowAny])
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
        # print(user_data.text)
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

                if user_data["person"]["displayPicture"] is None:
                    picture = "https://ui-avatars.com/api/?name=" + name[0] + "+" + name[
                        1] + "&background=cae7b9&color=1e3231"
                else:
                    picture = "https://internet.channeli.in" + user_data["person"]["displayPicture"]

                is_admin = False
                if user_data["student"]["currentYear"] >= 4:
                    is_admin = True

                newUser = User(enrolment_number=enrolNum, username=enrolNum, email=email, first_name=firstName, full_name=fullName,
                               is_superuser=is_admin, display_picture=picture)
                newUser.save()
                login(request=request, user=newUser)
                # ser = UserSerializer(newUser)
                return Response({"status": "user created", "access_token": ac_tok}, status=status.HTTP_202_ACCEPTED)
            else:
                # SORRY YOU CAN'T USE THIS
                return Response({"status": "user not in IMG"})

        user.access_token = ac_tok
        user.save()
        login(request=request, user=user)
        # request.session["user"] = "dingo"
        return Response({"status": "user exists", "access_token": ac_tok})

    @action(methods=['post', 'options', ], detail=False, url_name="login", url_path="login",
            permission_classes=[AllowAny])
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
            ser = UserSerializer(request.user)
            return Response(ser.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"enrolment_number": "Not authenticated"})


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # parser_classes = [FileUploadParser, ]
    # @action(methods=['post', 'options', ], detail=False, url_name="upload", url_path="upload", permission_classes=[AllowAny])
    # def upload_image(self, request):
    #     # print(request.data)
    #     print("Hi  l")
    #     serializer = ImageSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CommentPostSerializer
        else:
            return CommentGetSerializer
