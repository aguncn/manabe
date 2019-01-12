from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from api.views import UserViewSet
from api.views import AppViewSet
from appinput.models import App
from envx.models import Env

from model_mommy import mommy


class UserListTests(TestCase):
    def setUp(self):
        self.fatory = APIRequestFactory()

    def test_user_list_view_status_code(self):
        url = reverse('api:user-list')
        request = self.fatory.get(url)
        response = UserViewSet.as_view(({'get': 'list'}))(request)
        self.assertEqual(response.status_code, 200)

    def test_user_list_url_resolves_user_view(self):
        view = resolve('/api/users/')
        self.assertEqual(view.func.__name__,
                         UserViewSet.as_view(({'get': 'list'})).__name__)


class AppListTests(TestCase):
    def setUp(self):
        self.fatory = APIRequestFactory()

    def test_app_list_view_status_code(self):
        url = reverse('api:app-list')
        request = self.fatory.get(url)
        response = AppViewSet.as_view(({'get': 'list'}))(request)
        self.assertEqual(response.status_code, 200)

    def test_app_list_url_resolves_app_view(self):
        view = resolve('/api/apps/')
        self.assertEqual(view.func.__name__,
                         AppViewSet.as_view(({'get': 'list'})).__name__)


class AppCreateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test', )
        token = Token.objects.get(user__username='test')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_app(self):
        """
        Ensure we can create a new app object.
        """
        url = reverse('api:app-list')
        payload = {'name': "ZEP-BACKEND-JAVA",
                   'jenkins_job': "jenkins_job",
                   'git_url': "http://test/",
                   'dir_build_file': "./target/",
                   'build_cmd': "mvn packaget",
                   'script_url': "http://test/script.sh"
                   }
        response = self.client.post(url, payload, format='json')
        print(response, "@@@@@@@@@")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(App.objects.count(), 1)
        self.assertEqual(App.objects.get().name, 'ZEP-BACKEND-JAVA')


class ServerCreateTests(TestCase):
    def setUp(self):
        self.new_app = mommy.make(App,
                                  name='ZEP-BACKEND-NODEJS')
        self.new_env = mommy.make(Env,
                                  name='TEST')
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test', )
        token = Token.objects.get(user__username='test')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_server_create_view(self):
        url = reverse('api:server-list')
        payload = {'name': "192.168.1.213_8888",
                   'ip_address': "192.168.1.212",
                   'port': "8888",
                   'salt_name': "192.168.1.213_8888",
                   'app_name': "ZEP-BACKEND-NODEJS",
                   'env_name': "TEST",
                   'app_user': "root"
                   }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 201)
