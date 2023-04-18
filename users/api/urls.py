from django.urls import path
from users.api.views import UserRegisterAPIView, UserLoginAPIView, UserDetailAPIView, UserUpdateAPIView, UserDeleteAPIView, FollowingCreateAPIView, FollowingListAPIView, FollowDeleteAPIView, FollowerListAPIView, ResetPasswordSendEmailAPIView, ResetPasswordAPIView, UserDetailWithPkAPIView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('me/', UserDetailAPIView.as_view(), name='detail'),
    path('me/', UserUpdateAPIView.as_view(), name='update'),
    path('<str:pk>/detail', UserDetailWithPkAPIView.as_view(), name='user-detail'),
    path('<int:pk>', UserDeleteAPIView.as_view(), name='delete'),
    path('unfollow/', FollowDeleteAPIView.as_view(), name='follows'),
    path('follow/', FollowingCreateAPIView.as_view(), name='follow'),
    path('<str:pk>/followings/', FollowingListAPIView.as_view(), name='followings'),
    path('<str:pk>/followers/', FollowerListAPIView.as_view(), name='followers'),
    path('reset-password-send-email/', ResetPasswordSendEmailAPIView.as_view(), name='reset-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]
