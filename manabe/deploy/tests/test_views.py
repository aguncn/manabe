from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from deploy.models import DeployPool
from deploy.views import DeployCreateView, DeployDetailView
from deploy.views import DeployListView, DeployUpdateView


class DeployListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_deploy = mommy.make(DeployPool)

    def test_list_view_status_code(self):
        url = reverse('deploy:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_resolves_home_view(self):
        view = resolve('/deploy/list/')
        self.assertEqual(view.func.__name__, DeployListView.as_view().__name__)


class DeployDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_deploy = mommy.make(DeployPool)

    def test_detail_view_status_code(self):
        url = reverse('deploy:detail', kwargs={'pk': self.new_deploy.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_home_view(self):
        view = resolve('/deploy/view/' + str(self.new_deploy.id) + '/')
        self.assertEqual(view.func.__name__, DeployDetailView.as_view().__name__)


class DeployCreateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_deploy = mommy.make(DeployPool)

    def test_detail_view_status_code(self):
        url = reverse('deploy:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_home_view(self):
        view = resolve('/deploy/create/')
        self.assertEqual(view.func.__name__, DeployCreateView.as_view().__name__)


class DeployUpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_deploy = mommy.make(DeployPool)

    def test_detail_view_status_code(self):
        url = reverse('deploy:edit', kwargs={'pk': self.new_deploy.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_home_view(self):
        view = resolve('/deploy/edit/' + str(self.new_deploy.id) + '/')
        self.assertEqual(view.func.__name__, DeployUpdateView.as_view().__name__)