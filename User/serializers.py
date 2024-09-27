# User/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'gender')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        gender = validated_data.pop('gender')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Set the gender in the profile
        UserProfile.objects.create(user=user, gender=gender)

        return user
