import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def year_validator(year):
    awards_years = ["2019", "2020", "2021", "2018"]
    if year not in awards_years:
        awards_years.sort()
        raise ValidationError(f"Year must be one of: {' '.join(awards_years)}")


class BestGithubRepo(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="Unique ID for the Github repo.",
        primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        editable=False,
        null=True,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    name = models.CharField(max_length=40, help_text="Name of the repository")
    updated_at = models.DateTimeField(auto_now=True)
    year = models.CharField(
        help_text="Year for the awards",
        max_length=4,
        validators=[year_validator]
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        help_text="Unique ID for the review.",
        primary_key=True
    )
    content = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        editable=False,
        null=True,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    repo = models.ForeignKey(
        BestGithubRepo,
        editable=True,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    updated_at = models.DateTimeField(auto_now=True)


class RepoLike(models.Model):
    LIKE = (
        ('like', 'like'),
        ('dislike', 'dislike')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        editable=True,
        null=True,
        on_delete=models.CASCADE
    )
    like = models.CharField(max_length=10, choices=LIKE)
    repo = models.ForeignKey(
        BestGithubRepo,
        editable=True,
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
