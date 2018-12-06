from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from appinput.models import App
from appinput.forms import AppForm


class AppInputCreateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('root', 'root@demon.com', 'root')
        admin_group = Group.objects.create(name='admin')
        admin_users = [self.user]
        admin_group.user_set.set(admin_users)
        self.client.login(username='root', password='root')

    def test_csrf(self):
        url = reverse('appinput:create')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('appinput:create')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, AppForm)

    def test_valid_form(self):
        data = {
            'name': 'app_name',
            'jenkins_job': "jenkins_job",
            'git_url': "http://localhost",
            'build_cmd': "mvn package",
            'dir_build_file': "dir",
            'package_name': 'app.zip',
            'zip_package_name': 'app.zip',
            'manage_user': self.user.id,
            'script_url': "http://local/"
        }
        form = AppForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {}
        form = AppForm(data=data)
        self.assertFalse(form.is_valid())

    def test_new_app_valid_post_data(self):
        url = reverse('appinput:create')
        data = {
            'name': 'app_name',
            'jenkins_job': "jenkins_job",
            'git_url': "http://localhost",
            'build_cmd': "mvn package",
            'dir_build_file': "dir",
            'package_name': 'app.zip',
            'zip_package_name': 'app.zip',
            'manage_user': self.user.id,
            'script_url': "http://local/"
        }
        response = self.client.post(url, data)
        self.assertTrue(App.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('appinput:create')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEqual(response.status_code, 200)

    def test_form_inputs(self):
        url = reverse('appinput:create')
        response = self.client.get(url)
        self.assertContains(response, '<input', 11)
        self.assertContains(response, 'type="checkbox"', 1)
        self.assertContains(response, '<select', 1)
