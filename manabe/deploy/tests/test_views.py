from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from unittest.mock import patch, Mock, MagicMock, create_autospec
from model_mommy import mommy
from envx.models import Env
from appinput.models import App
from serverinput.models import Server
from deploy.models import DeployPool, DeployStatus
from deploy.views import DeployCreateView, DeployDetailView
from deploy.views import DeployListView, DeployUpdateView
import deploy.salt_cmd_views


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


class DeployFunctionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test',)
        self.client.login(username='test', password='test')
        self.new_server = mommy.make(Server, env_name__name='fat',
                                     app_name__script_url="http://",
                                     app_user=self.user,
                                     app_name__name="hello",
                                     app_name__zip_package_name="heh",
                                     app_name__package_name="heh",
                                     port="3456",
                                     )
        self.new_deploy = mommy.make(DeployPool,
                                     name="2018--12-24-56XN",
                                     is_inc_tot='tot')
        DeployStatus.objects.create(name="FINISH", memo="FINISH")

    @patch('deploy.salt_cmd_views.cmd_run')
    def test_deploy_function(self, mock_cmd_run):
        mock_cmd_run.return_value = True
        self.assertEqual(deploy.salt_cmd_views.deploy(
            subserver_list=[[1, 2, 3], [4, 5, 6]],
            deploy_type="deployall",
            is_restart_server=True,
            user_name=self.user,
            deploy_version="2018--12-24-56XN",
            operation_type="deploy"
        ), True)

    @patch('deploy.salt_cmd_views.salt_run')
    def test_cmd_run_function(self, mock_salt_run):
        mock_salt_run.return_value = {'return': [{self.new_server.name: {'retcode': 0}}]}
        self.assertNotEquals(deploy.salt_cmd_views.cmd_run(
            server_id=self.new_server.id,
            action="deploy",
            user_name=self.user,
            percent_value="100%",
            deploy_version="2018--12-24-56XN",
            operation_type="deploy"),  True)
