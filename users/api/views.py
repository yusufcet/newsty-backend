from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from users.api.serializers import UserRegisterSerializer, UserLoginSerializer, UserDetailSerializer, UserUpdateSerializer, FollowingSerializer, FollowingListSerializer, FollowerListSerializer, PasswordResetTokenSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AccessToken.for_user(user)
        send_mail(
            'Welcome to the newsty',
            '<h1 style="color:red">Welcome to the newsty</h1>',
            'newsty@newsty.com',
            [user.email]
        )

        return Response(
            {
                "user": {
                    **UserDetailSerializer(user, context=self.get_serializer_context()).data,
                    "token": str(token)
                },
                "message": "User Created Successfully."
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.login(serializer.validated_data)
        if user is None:
            return Response(
                {
                    "error": "Invalid Credentials."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = AccessToken.for_user(user)
        return Response(
            {
                "user": {
                    **UserDetailSerializer(user, context=self.get_serializer_context()).data,
                    "token": str(token)
                },
                "message": "User Logged In Successfully."
            },
            status=status.HTTP_200_OK,
        )


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request):
        serializer = self.get_serializer(self.get_object())
        return Response(
            {
                "user": serializer.data,
                "message": "User Details Fetched Successfully."
            },
            status=status.HTTP_200_OK,
        )


class UserDetailWithPkAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_object(self):
        return self.get_queryset().filter(pk=self.kwargs['pk']).first()

    def get(self, request, pk):
        user = self.get_object()
        if not user:
            return Response(
                {
                    "error": "User Not Found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(user)
        return Response(
            {
                "user": serializer.data,
                "message": "User Details Fetched Successfully."
            },
            status=status.HTTP_200_OK,
        )


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        return self.get_queryset().filter(pk=self.kwargs['pk']).first()

    def delete(self, request, pk):
        user = self.get_object()
        if not user:
            return Response(
                {
                    "error": "User Not Found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        user.delete()
        return Response(
            {
                "message": "User Deleted Successfully."
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordSendEmailAPIView(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = get_user_model().objects.filter(
            email=request.data['email']).first()

        if not user:
            return Response(
                {
                    "error": "User Not Found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        token = random.randint(100000, 999999)

        send_mail(
            'Reset Password',
            'Reset password token is {}'.format(token),
            'newsty@newsty.com',
            [user.email],
        )

        data = {
            'user': user.id,
            'token': token
        }

        user.password_reset_tokens.all().delete()

        serializer = PasswordResetTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Reset password link sent to your email."
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = get_user_model().objects.filter(
            email=request.data['email']).first()
        if not user:
            return Response(
                {
                    "error": "User Not Found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        token = user.password_reset_tokens.filter(
            token=request.data['token']).first()
        if not token:
            return Response(
                {
                    "error": "Invalid Token."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(request.data['password'])
        user.save()
        token.delete()
        return Response(
            {
                "message": "Password Reset Successfully."
            },
            status=status.HTTP_200_OK,
        )


class FollowingCreateAPIView(generics.CreateAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        follower = request.user
        following = get_user_model().objects.filter(
            pk=request.data['following']).first()

        if not following:
            return Response(
                {
                    "error": "User Not Found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if follower == following:
            return Response(
                {
                    "error": "You cannot follow yourself."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if following.id in follower.following.all().values_list('following', flat=True):
            return Response(
                {
                    "error": "You are already following this user."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "follower": request.user.id,
            "following": request.data.get('following')
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "User Followed Successfully."
            },
            status=status.HTTP_201_CREATED,
        )


class FollowDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.following.filter(following_id=self.request.data.get("following")).first()

    def delete(self, request):
        follow = self.get_object()
        if not follow:
            return Response(
                {
                    "error": "You Don't Follow This User."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        follow.delete()
        return Response(
            {
                "message": "User Unfollowed Successfully."
            },
            status=status.HTTP_200_OK,
        )


class FollowingListAPIView(generics.ListAPIView):
    serializer_class = FollowingListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.kwargs['pk']).first().following.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "followings": serializer.data,
                "message": "Following List Fetched Successfully."
            },
            status=status.HTTP_200_OK,
        )


class FollowerListAPIView(generics.ListAPIView):
    serializer_class = FollowerListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.kwargs['pk']).first().followers.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "followers": serializer.data,
                "message": "Follower List Fetched Successfully."
            },
            status=status.HTTP_200_OK,
        )
