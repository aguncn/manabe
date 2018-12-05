from django.test import TestCase
from model_mommy import mommy
from envx.models import Env


class EnvModelTestMommy(TestCase):
    def setUp(self):
        self.new_env = mommy.make(Env)

    def test_env_creation_mommy(self):
        self.assertTrue(isinstance(self.new_env, Env))
        self.assertEqual(self.new_env.__str__(), self.new_env.name)