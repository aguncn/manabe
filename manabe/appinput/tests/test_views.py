from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from appinput.models import App
from appinput.views import AppInputCreateView, AppInputListView
from appinput.views import AppInputUpdateView, AppInputDetailView


class AppInputTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(App)

    def test_list_view_status_code(self):
        url = reverse('appinput:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_resolves_home_view(self):
        view = resolve('/app/list/')
        self.assertEqual(view.func.__name__, AppInputListView.as_view().__name__)

    def test_detail_view_status_code(self):
        url = reverse('appinput:detail', kwargs={'pk': self.new_app.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_home_view(self):
        view = resolve('/app/view/1/')
        self.assertEqual(view.func.__name__, AppInputDetailView.as_view().__name__)