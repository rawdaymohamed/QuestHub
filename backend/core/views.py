from django.shortcuts import render

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from .utils import upload_avatar_to_cloudinary  # Assuming the method is in utils.py


# Serializer for registration
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# View for registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer):
        # If there's a new avatar, upload it to Cloudinary
        avatar = self.request.FILES.get('avatar')
        if avatar:
            avatar_url = upload_avatar_to_cloudinary(avatar)
            serializer.save(avatar_url=avatar_url)  # Save the avatar URL
        else:
            serializer.save()  # No avatar, just save other profile data
