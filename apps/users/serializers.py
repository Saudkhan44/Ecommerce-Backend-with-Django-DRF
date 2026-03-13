from rest_framework import serializers
from .models import CustomUser, UserProfile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile

User = get_user_model()

# apps/users/models.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# --------------------------
# Register Serializer
# --------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        user.role = "customer"
        user.save()

        return user


# --------------------------
# JWT Login Serializer
# --------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
        })
        return data
# --------------------------
# CustomUser Serializer
# --------------------------
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']

# --------------------------
# UserProfile Serializer
# --------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # nested user info

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'profile_image', 'phone_number', 'address', 'created_at']