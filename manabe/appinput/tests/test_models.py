from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from appinput.models import App


class AppInputModelTest(TestCase):
    def setUp(self):
        manage_user = User.objects.create_user(username='Samantha', password="password")
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

    def test_app_models(self):
        result = App.objects.get(id=1)
        self.assertEqual(result.name, "ABC-BACKEND-JAVA")


class AppInputModelTestMommy(TestCase):
    def test_app_creation_mommy(self):
        new_app = mommy.make('appinput.App')
        self.assertTrue(isinstance(new_app, App))
        self.assertEqual(new_app.__str__(), new_app.name)