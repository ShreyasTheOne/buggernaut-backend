import requests
import threading

from django.contrib.auth import login, logout

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from buggernaut.serializers import *
from buggernaut.mailingSystem import Mailer

from buggernaut_backend.settings import base_configuration


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post', 'options', ], detail=False, url_name="on_login", url_path="on_login",
            permission_classes=[AllowAny])
    def on_login(self, request):

        ode = self.request.data
        code = ode["code"]

        # GET AUTHORIZATION CODE
        url = "https://internet.channeli.in/open_auth/token/"
        data = {
            'client_id': base_configuration["secrets"]["clientID"],
            'client_secret': base_configuration["secrets"]["clientSecret"],
            'grant_type': 'authorization_code',
            'redirect_url': 'http://localhost:3000/onlogin',
            'code': code
        }
        user_data = requests.post(url=url, data=data).json()

        if (user_data == None):
            return Response({"status": "invalid token"})
        ac_tok = user_data['access_token']

        # GET ACCESS TOKEN
        headers = {
            'Authorization': 'Bearer ' + ac_tok,
        }
        user_data = requests.get(url="https://internet.channeli.in/open_auth/get_user_data/", headers=headers).json()

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
                        1] + "&background=DCD6F7&color=412234&size=512"
                else:
                    picture = "https://internet.channeli.in" + user_data["person"]["displayPicture"]

                is_admin = False
                if user_data["student"]["currentYear"] >= 3:
                    is_admin = True

                newUser = User(enrolment_number=enrolNum, username=enrolNum, email=email, first_name=firstName,
                               full_name=fullName, is_superuser=is_admin, is_staff=is_admin, display_picture=picture)
                newUser.save()
                login(request=request, user=newUser)
                return Response({"status": "user created"}, status=status.HTTP_202_ACCEPTED)
            else:
                # SORRY YOU CAN'T USE THIS
                return Response({"status": "user not in IMG"})

        if user.banned:
            return Response({"status": "user banned"})

        login(request=request, user=user)
        return Response({"status": "user exists"})

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

    @action(methods=['get', 'options', ], detail=False, url_name="logout_user", url_path="logout_user",
            permission_classes=[IsAuthenticated])
    def logout_user(self, request):
        logout(request)
        return Response({"status": "logged_out"})

    @action(methods=['get', 'options', ], detail=False, url_name="test", url_path="test",
            permission_classes=[AllowAny])
    def test(self, request):
        if request.user.is_authenticated:
            if request.user.banned:
                logout(request)
                return Response({"enrolment_number": "user banned"})
            ser = UserSerializer(request.user)
            return Response(ser.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"enrolment_number": "Not authenticated"})

    @action(methods=['get', 'options', ], detail=False, url_name="stats", url_path="stats",
            permission_classes=[AllowAny])
    def get_stats(self, request):
        if request.user.is_authenticated:
            if request.user.banned:
                logout(request)
                return Response({"enrolment_number": "user banned"})
            reported = Issue.objects.filter(reported_by=request.user).count()
            resolved = Issue.objects.filter(resolved_by=request.user).count()
            stats = {"resolved": resolved, "reported": reported}
            ser = UserSerializer(request.user)
            return Response({**ser.data, **stats}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"enrolment_number": "Not authenticated"})

    @action(methods=['get', 'options', ], detail=True, url_name="toggleStatus", url_path="toggleStatus",
            permission_classes=[IsAuthenticated])
    def toggleStatus(self, request, pk):
        if request.user.is_superuser:
            user = User.objects.get(pk=pk)
            if user == request.user:
                return Response({"status": "You cannot change your own status!"})

            if user.is_superuser:
                user.is_superuser = False
                user.is_staff = False
            else:
                user.is_superuser = True
                user.is_staff = True

            user.save()

            mailer = Mailer()

            if user.is_superuser:
                x = threading.Thread(target=mailer.statusUpdate,
                                     args=(user.email,
                                           user.full_name,
                                           "promote",
                                           request.user.full_name))
            else:
                x = threading.Thread(target=mailer.statusUpdate,
                                     args=(user.email,
                                           user.full_name,
                                           "demote",
                                           request.user.full_name))
            x.start()
            return Response({"status": "Role updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "You're not an admin"}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get', 'options', ], detail=True, url_name="toggleBan", url_path="toggleBan",
            permission_classes=[IsAuthenticated])
    def toggleBan(self, request, pk):
        if request.user.is_superuser:
            user = User.objects.get(pk=pk)
            if user == request.user:
                return Response({"status": "You cannot change your own status!"})

            if user.banned:
                user.banned = False
            else:
                user.banned = True
                user.is_superuser = False
                user.is_staff = False

            user.save()

            mailer = Mailer()

            if user.banned:
                x = threading.Thread(target=mailer.banOrAdmitUser,
                                     args=(user.email,
                                           user.full_name,
                                           "banned",
                                           request.user.full_name))
            else:
                x = threading.Thread(target=mailer.banOrAdmitUser,
                                     args=(user.email,
                                           user.full_name,
                                           "admit",
                                           request.user.full_name))
            x.start()
            return Response({"status": "Status updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "You're not an admin"}, status=status.HTTP_403_FORBIDDEN)
