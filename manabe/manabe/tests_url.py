from django.test import TestCase
from django.urls import resolve, reverse

from .urls import user_register, user_login


class UrlTests(TestCase):
    def test_user_register_view_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_login_view_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_register_url_resolves_get_classes_view(self):
        view = resolve('/accounts/register/')
        self.assertEqual(view.func, user_register)

    def test_user_login_url_resolves_get_classes_view(self):
        view = resolve('/accounts/login/')
        self.assertEqual(view.func, user_login)