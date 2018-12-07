from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from appinput.models import App
from serverinput.models import Server
from envx.models import Env


class ServerInputModelTestMommy(TestCase):
    def setUp(self):
        self.new_server = mommy.make(Server)

    def test_server_creation_mommy(self):
        self.assertTrue(isinstance(self.new_server, Server))
        self.assertEqual(self.new_server.__str__(), self.new_server.name)
