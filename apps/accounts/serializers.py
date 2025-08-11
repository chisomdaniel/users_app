import os
import uuid
from PIL import Image
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings

from .models import User, Profile


class UserRegisterSerializer(RegisterSerializer):
    """serializer for the user registration view.
    Remember, the register serializer doesn't have to be uncessarily
    complex:
    -   You can use the custom_signup method to customise the signup
        after the default save method has been called on the user model already
    -   Any behaviour you don't want from the default signup process, you can
        just edit the field and make it `None`.
    -   If you include a phone number in the fields, you can make the
        `_has_phone_field` true.
    -   Put any other additional field that should go on the user model in
        the `get_cleaned_data` method.
    -   You can override the defualt behaviour of requiring two password entry
        or just leave it depending on your usecase and need
    """
    username = None
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    image = serializers.URLField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True)
    password1 = None
    password2 = None

    _has_phone_field = False

    def validate(self, data):
        """
        Validate the default behaviour of checking for
        `password1` and `password2`.
        """
        return data

    def get_cleaned_data(self):
        """
        additional fields that should be added on the custom
        user class apart from the default of just the username, password1 and email
        """
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password', None)
        })
        return data

    def custom_signup(self, request, user: User):
        """
        perform some custom action on the user model signup.
        If a profile model is linked to the user model, you can
        create that here.
        """
        user.image = self.validated_data.get('image', None)
        user.save()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "city",
            "state",
            "country",
            "date_of_birth",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """user detail serializer"""
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "image",
            "profile",
            "is_active",
            "date_joined",
            "updated_at",
        ]
        read_only_fields = ["email", "is_active", "date_joined", "updated_at"]

    def update(self, instance, validated_data):
        """update user profile"""
        method = self.context["request"].method
        if (method != 'PATCH'):
            raise serializers.ValidationError(f"Method not allowed: {method}. Only `PATCH`")


        profile_data = validated_data.pop('profile', {})

        for i, j in validated_data.items():
            if i in self.Meta.read_only_fields:
                continue
            setattr(instance, i, j)
        instance.save()

        profile = Profile.objects.get(user=instance)
        serializer = ProfileSerializer(profile, data=profile_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            raise serializers.ValidationError(f"Invalid profile data: {serializer.errors}")
        
        return instance


class VerifyEmailSerialzer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class ProfileImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def create(self, validated_data):
        file_location = os.path.join(settings.PROFILE_IMAGE_DIRECTORY,
                                     'profile-' + str(uuid.uuid4().hex)[:7] + '.jpg')

        img = Image.open(validated_data.get("image"))
        img.save(file_location)
        validated_data["image"] = file_location
        return validated_data

    def to_representation(self, instance):
        """the instance is a dict as set in the create method"""
        return instance
