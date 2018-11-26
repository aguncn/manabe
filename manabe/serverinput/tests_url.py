from django.test import TestCase
from django.urls import resolve, reverse

from .urls import ServerInputListView, ServerInputCreateView


class UrlTests(TestCase):

    def test_server_list_view_status_code(self):
        url = reverse('serverinput:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_server_create_view_status_code(self):
        url = reverse('serverinput:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_server_list_url_resolves_get_classes_view(self):
        view = resolve('/server/list/')
        self.assertEqual(view.func.__name__, ServerInputListView.as_view().__name__)

    def test_server_create_url_resolves_get_classes_view(self):
        view = resolve('/server/create/')
        self.assertEqual(view.func.__name__, ServerInputCreateView.as_view().__name__)