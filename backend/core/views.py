import cloudinary.uploader

from rest_framework import generics
from django.contrib.auth.models import User

from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer


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
        avatar = self.request.FILES.get("avatar")
        if avatar:
            result = cloudinary.uploader.upload(avatar)
            avatar_url = result.get("secure_url")
            serializer.save(avatar=avatar_url)
        else:
            serializer.save()
