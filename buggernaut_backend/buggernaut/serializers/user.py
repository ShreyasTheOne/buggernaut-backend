from rest_framework import serializers
from buggernaut.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'first_name', 'username', 'pk', 'enrolment_number', 'email', 'display_picture',
                  'is_superuser', 'is_staff', 'banned']
        # read_only_fields = ['username', 'first_name', 'last_name', 'pk']