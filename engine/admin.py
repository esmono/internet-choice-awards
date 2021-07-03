from django.contrib import admin

from .models import BestGithubRepo, Review, RepoLike

admin.site.register(BestGithubRepo)
admin.site.register(Review)
admin.site.register(RepoLike)
