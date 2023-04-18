from rest_framework import serializers
from users.models import User, Following, PasswordResetToken

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name',
                  'last_name', 'username', 'birth_date', 'user_type']

        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def login(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if user:
            if user.check_password(validated_data['password']):
                if user.is_active:
                    return user
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'email', 'first_name', 'last_name',
                  'username', 'birth_date', 'user_type', 'rate']

        extra_kwargs = {
            'user_type': {'read_only': True},
        }

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = ['user', 'token']


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['follower', 'following']


class FollowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['following']


class FollowerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['follower']
