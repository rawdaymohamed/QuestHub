from rest_framework import serializers
from .models import Profile
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source="user.username", required=False)
    password = serializers.CharField(
        source="user.password", write_only=True, required=False, min_length=8
    )
    avatar = serializers.ImageField(required=False, write_only=True) 
    avatar_url = serializers.CharField(source="avatar", read_only=True)
    class Meta:
        model = Profile
        fields = ["user_id", "username", "bio", "avatar", "password", "avatar_url"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        avatar_file = validated_data.pop("avatar", None)

        if "username" in user_data:
            instance.user.username = user_data["username"]
        if "password" in user_data:
            instance.user.set_password(user_data["password"])
        instance.user.save()

        if avatar_file:
            import cloudinary.uploader
            result = cloudinary.uploader.upload(avatar_file)
            validated_data["avatar"] = result.get("secure_url")

        return super().update(instance, validated_data)

# Serializer for registration
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
