from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from serverinput.models import Server
from serverinput.urls import ServerInputListView, ServerInputCreateView
from serverinput.urls import ServerInputUpdateView, ServerInputDetailView


class ServerInputListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(Server)

    def test_list_view_status_code(self):
        url = reverse('serverinput:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_resolves_home_view(self):
        view = resolve('/server/list/')
        self.assertEqual(view.func.__name__,
                         ServerInputListView.as_view().__name__)


class ServerInputDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(Server)

    def test_detail_view_status_code(self):
        url = reverse('serverinput:detail', kwargs={'pk': self.new_app.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_home_view(self):
        view = resolve('/server/view/1/')
        self.assertEqual(view.func.__name__, ServerInputDetailView.as_view().__name__)


class ServerInputCreateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(Server)

    def test_detail_view_status_code(self):
        url = reverse('serverinput:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_home_view(self):
        view = resolve('/server/create/')
        self.assertEqual(view.func.__name__, ServerInputCreateView.as_view().__name__)


class ServerInputUpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(Server)

    def test_detail_view_status_code(self):
        url = reverse('serverinput:edit', kwargs={'pk': self.new_app.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_home_view(self):
        view = resolve('/server/edit/1/')
        self.assertEqual(view.func.__name__, ServerInputUpdateView.as_view().__name__)