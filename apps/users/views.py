from urllib import request

from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import UserProfile
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer

User = get_user_model()


# -----------------------------
# Register API
# -----------------------------
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# Login API (JWT)
# -----------------------------
class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# -----------------------------
# Profile API with image update
# -----------------------------
class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)

        # Update user fields
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()

        # update profile fields
        if profile:
            profile.phone_number = request.data.get('phone_number', profile.phone_number)
            profile.address = request.data.get('address', profile.address)

            # Profile image
            image = request.FILES.get('profile_image')
            if image:
                profile.profile_image = image

            profile.save()

        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_image": request.build_absolute_uri(
                profile.profile_image.url) if profile and profile.profile_image else None,
            "phone_number": profile.phone_number if profile else None,
            "address": profile.address if profile else None,
            "message": "Profile updated successfully",
        })