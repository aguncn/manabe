from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from appinput.models import App
from serverinput.models import Server
from envx.models import Env


class ServerInputModelTest(TestCase):

    def setUp(self):
        manage_user = User.objects.create_user(username='Samantha', password="password")
        env_item = Env.objects.create(name="TEST",
                                      eid=1,)
        app_item = App.objects.create(name="ABC-BACKEND-JAVA",
                                      jenkins_job="test_jenkins_job",
                                      git_url="http://tese_git_url/",
                                      dir_build_file="test_project/",
                                      build_cmd="mvn package",
                                      is_restart_status=True,
                                      package_name="package_name.war",
                                      zip_package_name="zip_package_name.zip",
                                      op_log_no=88,
                                      manage_user=manage_user,
                                      script_url="http://nginx/script_url/test.sh",)
        server_item = Server.objects.create(name="192.168.1.1_8080",
                                            salt_name="192.168.1.1_8080",
                                            ip_address="192.168.1.1",
                                            port="8080",
                                            app_name=app_item,
                                            env_name=env_item,
                                            app_user="root",
                                            op_user=manage_user,
                                            )

    def test_server_models(self):
        result = Server.objects.get(id=1)
        self.assertEqual(result.salt_name, "192.168.1.1_8080")
        self.assertEqual(result.app_user, "root")


class ServerInputModelTestMommy(TestCase):
    def setUp(self):
        self.new_server = mommy.make(Server)

    def test_server_creation_mommy(self):
        self.assertTrue(isinstance(self.new_server, Server))
        self.assertEqual(self.new_server.__str__(), self.new_server.name)
