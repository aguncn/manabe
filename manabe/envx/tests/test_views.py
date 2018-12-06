from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from envx.models import Env
from envx.urls import EnvXListView, EnvXHistoryView


class EnvXListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(Env)

    def test_list_view_status_code(self):
        url = reverse('envx:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_resolves_home_view(self):
        view = resolve('/envx/list/')
        self.assertEqual(view.func.__name__, EnvXListView.as_view().__name__)


class EnvXHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(Env)

    def test_list_view_status_code(self):
        url = reverse('envx:history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_resolves_home_view(self):
        view = resolve('/envx/history/')
        self.assertEqual(view.func.__name__, EnvXHistoryView.as_view().__name__)