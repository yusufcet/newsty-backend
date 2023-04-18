from rest_framework import generics, permissions
from rest_framework.response import Response
from news.api.serializers import (
    NewsSerializer,
    CreateNewsSerializer,
    UpdateNewsSerializer,
    DeleteNewsSerializer,
    CommentSerializer,
    CreateCommentSerializer,
    UpdateCommentSerializer,
    DeleteCommentSerializer,
    TruthSerializer,
    CreateTruthSerializer,
    DeleteTruthSerializer,
)
from news.models import News, Comment, Truth, Hashtag
from django.contrib.auth import get_user_model
from news.api.permissions import IsAuthenticatedAndOwner
import datetime
import random

User = get_user_model()


def update_news_popularity(news, count):
    if news.is_flagged == False:
        news.popularity += count
        news.save()


def update_user_rate(user):
    user_news = News.objects.filter(author=user)
    user_news_truths = Truth.objects.filter(news__in=user_news)
    user_news_truths_true_count = user_news_truths.filter(is_true=True).count()
    user_news_truths_false_count = user_news_truths.filter(is_true=False).count()
    rate = ((user_news_truths_true_count - user_news_truths_false_count) / user_news_truths.count()) * 5
    rate = round(rate, 2)
    user.rate = rate
    user.save()


def check_news_is_flagged(news):
    # if post take first vote before 24 hours this code will work
    news_truths = Truth.objects.filter(news=news).all().values()
    truths_date_count_dict = {}
    for news_truth in news_truths:
        if news_truth['created_at'].date() in truths_date_count_dict:
            truths_date_count_dict[news_truth['created_at'].date()] += 1

        else:
            truths_date_count_dict[news_truth['created_at'].date()] = 1
    
    truths_past_date_count_dict = truths_date_count_dict.copy()
    truths_past_date_count_dict.popitem()

    if len(truths_past_date_count_dict) != 0:
        avarage_vote_per_day = sum(truths_past_date_count_dict.values()) / len(truths_past_date_count_dict)
    else :
        avarage_vote_per_day = 0

    if truths_date_count_dict[datetime.date.today()] > avarage_vote_per_day * avarage_vote_per_day and avarage_vote_per_day != 0:
        news.is_flagged = True
        news.save()
    else:
        news.is_flagged = False
        news.save()

    # if post take first vote in 24 hours this code will work
    user_all_news = News.objects.filter(author=news.author)
    user_all_news_truths = Truth.objects.filter(news__in=user_all_news).all().values()
    truths_first_date_count_dict = {}

    for user_all_news_truth in user_all_news_truths:
        if user_all_news_truth['created_at'].date() != datetime.date.today():
            if user_all_news_truth['created_at'].date() in truths_first_date_count_dict:
                truths_first_date_count_dict[user_all_news_truth['created_at'].date()] += 1

            else:
                truths_first_date_count_dict[user_all_news_truth['created_at'].date()] = 1

    if len(truths_first_date_count_dict) != 0:
        avarage_first_day_vote = sum(truths_first_date_count_dict.values()) / len(truths_first_date_count_dict)
    else:
        avarage_first_day_vote = 0
    
    if datetime.date.today() in truths_date_count_dict:
        if len(truths_date_count_dict) == 1:
            # if post take first vote in 24 and first post is not in 24 hours this code will work
            if truths_date_count_dict[datetime.date.today()] > avarage_first_day_vote * avarage_first_day_vote and avarage_first_day_vote != 0:
                news.is_flagged = True
                news.save()
            else:
                news.is_flagged = False
                news.save()
            # if post take first vote in 24 and first post is in 24 hours this code will work
            if truths_date_count_dict[datetime.date.today()] > 50:
                news.is_flagged = True
                news.save()

class CreateNewsAPIView(generics.CreateAPIView):
    serializer_class = CreateNewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        # save hashtags
        if self.request.data.get('hashtags') is not None:
            hashtags = self.request.data['hashtags']
        else:
            hashtags = []

        for hashtag in hashtags:
            hashtag = Hashtag.objects.get_or_create(name=hashtag)[0]
            serializer.instance.hashtags.add(hashtag)


class ListNewsAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = News.objects.all()
        return queryset


class ListUserNewsAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = News.objects.filter(author=self.kwargs['pk'])
        return queryset

class FeedNewsAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = News.objects.filter(author__in=self.request.user.following.all().values_list('following_id', flat=True)) | News.objects.all().order_by('-popularity')[:random.randint(1, 5)]
        return queryset


class RetrieveNewsAPIView(generics.RetrieveAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = News.objects.filter(id=self.kwargs['pk'])
        return queryset


class UpdateNewsAPIView(generics.UpdateAPIView):
    serializer_class = UpdateNewsSerializer
    permission_classes = [IsAuthenticatedAndOwner | permissions.IsAdminUser]

    def get_queryset(self):
        queryset = News.objects.filter(id=self.kwargs['pk'])
        return queryset

class DeleteNewsAPIView(generics.DestroyAPIView):
    serializer_class = DeleteNewsSerializer
    permission_classes = [IsAuthenticatedAndOwner | permissions.IsAdminUser]

    def get_queryset(self):
        queryset = News.objects.filter(id=self.kwargs['pk'])
        return queryset


class SearchNewsAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = None
        if self.request.query_params.get('search') is not None:
            if queryset is not None:
                queryset = queryset | News.objects.filter(title__icontains=self.request.query_params.get('search')) | News.objects.filter(content__icontains=self.request.query_params.get('search'))
            else:
                queryset = News.objects.filter(title__icontains=self.request.query_params.get('search')) | News.objects.filter(content__icontains=self.request.query_params.get('search'))
        if self.request.query_params.get('hashtags') is not None:
            hashtags = self.request.query_params.get('hashtags').split(',')
            if queryset is not None:
                queryset = queryset | News.objects.filter(hashtags__name__in=hashtags)
            else:
                queryset = News.objects.filter(hashtags__name__in=hashtags)
        if self.request.query_params.get('user') is not None:
            if queryset is not None:
                queryset = queryset | News.objects.filter(author__username__icontains=self.request.query_params.get('user'))
            else:
                queryset = News.objects.filter(author__username__icontains=self.request.query_params.get('user'))
        return queryset



class CreateCommentAPIView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            'news': self.kwargs['pk'],
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_news_popularity(News.objects.filter(pk=self.kwargs["pk"]).first(), 1)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class ListCommentAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.filter(news=self.kwargs['pk'])
        return queryset


class RetrieveCommentAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.filter(id=self.kwargs['pk'])
        return queryset


class UpdateCommentAPIView(generics.UpdateAPIView):
    serializer_class = UpdateCommentSerializer
    permission_classes = [IsAuthenticatedAndOwner | permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Comment.objects.filter(id=self.kwargs['pk'])
        return queryset


class DeleteCommentAPIView(generics.DestroyAPIView):
    serializer_class = DeleteCommentSerializer
    permission_classes = [IsAuthenticatedAndOwner | permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Comment.objects.filter(id=self.kwargs['pk'])
        return queryset


class CreateTruthAPIView(generics.CreateAPIView):
    serializer_class = CreateTruthSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        news = News.objects.get(id=self.kwargs['pk'])
        data = {
            **request.data,
            'news': news.id
        }
        if news.author == request.user:
            return Response({'message': 'You can not vote for your own news'}, status=400)

        if news.truths.filter(author=request.user).exists():
            truth = news.truths.get(author=request.user)
            serializer = self.get_serializer(truth, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = TruthSerializer(serializer.instance)

            update_user_rate(news.author)
            check_news_is_flagged(news)

            return Response(serializer.data, status=200)


        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_news_popularity(news, 5)
        serializer = TruthSerializer(serializer.instance)

        update_user_rate(news.author)
        check_news_is_flagged(news)

        return Response(serializer.data, status=201)


class DeleteTruthAPIView(generics.DestroyAPIView):
    serializer_class = DeleteTruthSerializer
    permission_classes = [IsAuthenticatedAndOwner | permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Truth.objects.filter(id=self.kwargs['pk'])
        return queryset


class ListTruthAPIView(generics.ListAPIView):
    serializer_class = TruthSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Truth.objects.filter(news=self.kwargs['pk'])
        return queryset


class ListUserTruthAPIView(generics.ListAPIView):
    serializer_class = TruthSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Truth.objects.filter(author=self.kwargs['pk'])
        return queryset
