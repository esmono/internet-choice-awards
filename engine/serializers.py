from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from engine.models import BestGithubRepo, Review, RepoLike


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ReviewsSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Review
        fields = ["created_by", "created_at", "updated_at", "content"]


class BestGithubRepoSerializer(serializers.HyperlinkedModelSerializer):
    reviews = ReviewsSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = BestGithubRepo
        fields = [
            "id", "name", "description", "year", "likes", "dislikes",
            "created_by", "created_at", "updated_at", "reviews"
        ]

    def validate(self, data):
        validate_flag = False
        if self.instance:
            validate_flag = BestGithubRepo.objects.filter(
                name=data.get("name", self.instance.name),
                year=data.get("year", self.instance.year)
            ).exists()
        else:
            validate_flag = BestGithubRepo.objects.filter(
                name=data.get("name"),
                year=data.get("year")
            ).exists()

        if validate_flag:
            raise serializers.ValidationError({
                "name": "Repo name already exists for the given year."
            })

        return data

    def get_likes(self, obj):
        return RepoLike.objects.filter(repo=obj.id, like="like").count()

    def get_dislikes(self, obj):
        return RepoLike.objects.filter(repo=obj.id, like="dislike").count()


class ReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Review
        fields = ["created_by", "created_at", "updated_at", "content", "repo"]

    def validate(self, data):
        validate_flag = Review.objects.filter(
            created_by=self.context["request"].user, repo=data['repo']
        ).exists()
        if validate_flag:
            raise serializers.ValidationError({
                "repo": "The user has already reviewed this repo."
            })

        return data


class ReviewEditSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Review
        fields = ["created_by", "created_at", "updated_at", "content"]


class RepoLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoLike
        fields = ["repo", 'like']

    def validate(self, data):
        validate_flag = RepoLike.objects.filter(
            created_by=self.context["request"].user, repo=data['repo'],
        ).exists()
        if validate_flag:
            raise serializers.ValidationError({
                "repo": "The user has already rated this repo."
            })

        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(
        required=True,
        validators=[validate_password],
        write_only=True
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
