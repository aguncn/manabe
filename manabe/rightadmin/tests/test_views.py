from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from appinput.models import App
from rightadmin.views import RightAdminView


class RightAdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_app = mommy.make(App)

    def test_list_view_status_code(self):
        url = reverse('rightadmin:list', kwargs={'pk': self.new_app.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_resolves_home_view(self):
        view = resolve('/rightadmin/list/' + str(self.new_app.id) + '/')
        self.assertEqual(view.func.__name__, RightAdminView.as_view().__name__)