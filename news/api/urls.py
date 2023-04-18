from django.urls import path
from news.api.views import (
    CreateNewsAPIView,
    ListUserNewsAPIView,
    ListNewsAPIView,
    RetrieveNewsAPIView,
    UpdateNewsAPIView,
    DeleteNewsAPIView,
    SearchNewsAPIView,
    FeedNewsAPIView,
    CreateCommentAPIView,
    ListCommentAPIView,
    RetrieveCommentAPIView,
    UpdateCommentAPIView,
    DeleteCommentAPIView,
    CreateTruthAPIView,
    DeleteTruthAPIView,
    ListTruthAPIView,
    ListUserTruthAPIView,
)

urlpatterns = [
    path('create/', CreateNewsAPIView.as_view(), name='create'),
    path('list/', ListNewsAPIView.as_view(), name='list'),
    path('<str:pk>/list/', ListUserNewsAPIView.as_view(), name='list'),
    path('<str:pk>/retrieve/', RetrieveNewsAPIView.as_view(), name='retrieve'),
    #path('<str:pk>/update/', UpdateNewsAPIView.as_view(), name='update'),
    path('<str:pk>/delete/', DeleteNewsAPIView.as_view(), name='delete'),
    path('search', SearchNewsAPIView.as_view(), name='search'),
    path('feed/', FeedNewsAPIView.as_view(), name='feed'),

    path('<str:pk>/comments/create/', CreateCommentAPIView.as_view(), name='create'),
    path('<str:pk>/comments/list/', ListCommentAPIView.as_view(), name='list'),
    path('comments/<str:pk>/retrieve/', RetrieveCommentAPIView.as_view(), name='retrieve'),
    path('comments/<str:pk>/update/', UpdateCommentAPIView.as_view(), name='update'),
    path('comments/<str:pk>/delete/', DeleteCommentAPIView.as_view(), name='delete'),

    path('<str:pk>/truth/create/', CreateTruthAPIView.as_view(), name='create'),
    path('truth/<str:pk>/delete/', DeleteTruthAPIView.as_view(), name='delete'),
    path('<str:pk>/truth/list/', ListTruthAPIView.as_view(), name='list'),
    path('<str:pk>/truth/list/user/', ListUserTruthAPIView.as_view(), name='list'),
]
