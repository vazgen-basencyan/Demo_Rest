import jwt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import ModelViewSet
from .serializers import UserDetailSerializer
from .models import CustomUser, Post
from rest_framework import generics, permissions
from django.conf import settings
from django.contrib import auth
from .serializers import PostSerializer, LogoutSerializer, LikeSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import update_last_login
from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .filters import DateRangeFilterSet
from .models import Like
from django.db.models.functions import TruncDate
from django.db.models import Q, Count
from rest_framework.authtoken.models import Token


class UserRegistrationView(ModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = CustomUser.objects.all()


class PostView(ModelViewSet):
    permission_classes = permissions.IsAuthenticated,

    serializer_class = PostSerializer
    queryset = Post.objects.all()


class LikeView(ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


class AnalyticView(GenericAPIView):
    queryset = Like.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DateRangeFilterSet
    filterset_fields = "date",

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        return (filtered_queryset.
                annotate(day=TruncDate('date')).values("day").
                annotate(total_likes=Count('pk', filter=Q(like="like"))).
                annotate(total_dislikes=Count('pk', filter=Q(like="dislike")))
                )

    def get(self, request, format=None):
        queryset = self.get_queryset().values("day", "total_likes", "total_dislikes")
        return Response(queryset)


class ActivityView(GenericAPIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request):
        context = {
            "last_login_date": request.user.last_login,
            "last_like_date": Like.objects.filter(user=request.user).order_by("date").first().date,
            "last_post_creation_date": Like.objects.filter(user=request.user).order_by("date").first().date,
        }
        print("hello")
        return Response(context)


class LogoutView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
