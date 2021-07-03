from django.test import TestCase

from engine.models import BestGithubRepo


class BestGithubRepoTestCase(TestCase):
    def setUp(self):
        BestGithubRepo.objects.create(
            description="The uncompromising Python code formatter",
            name="psf/black",
            year="2021"
        )
        BestGithubRepo.objects.create(
            description="Code coverage measurement for Python",
            name="nedbat/coveragepy",
            year="2021"
        )

    def test_repo_created_by(self):
        repo_black = BestGithubRepo.objects.get(name="psf/black")
        self.assertIsNone(repo_black.created_by)
