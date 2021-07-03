from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions

from engine import serializers
from engine.models import BestGithubRepo, Review, RepoLike
from engine.permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class BestGithubRepoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows best github repo to be viewed or edited.
    """

    queryset = BestGithubRepo.objects.all().order_by("-created_at")
    serializer_class = serializers.BestGithubRepoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows review to be viewed or edited.
    """

    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ("PATCH", "PUT"):
            serializer_class = serializers.ReviewEditSerializer

        return serializer_class

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RegisterView(generics.CreateAPIView):
    """
    API endpoint that allows users to sing in.
    """

    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]


class RateView(generics.CreateAPIView):
    """
    API endpoint that allows users to rate a repo.
    """

    queryset = RepoLike.objects.all()
    serializer_class = serializers.RepoLikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
