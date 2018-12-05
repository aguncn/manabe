from django.test import TestCase
from model_mommy import mommy
from deploy.models import DeployStatus, DeployPool, History


class DeployModelTestMommy(TestCase):
    def setUp(self):
        self.new_status = mommy.make(DeployStatus)
        self.new_deploy = mommy.make(DeployPool)
        self.new_history = mommy.make(History)

    def test_status_creation_mommy(self):
        self.assertTrue(isinstance(self.new_status, DeployStatus))
        self.assertEqual(self.new_status.__str__(), self.new_status.name)

    def test_deploy_creation_mommy(self):
        self.assertTrue(isinstance(self.new_deploy, DeployPool))
        self.assertEqual(self.new_deploy.__str__(), self.new_deploy.name)

    def test_history_creation_mommy(self):
        self.assertTrue(isinstance(self.new_history, History))
        self.assertEqual(self.new_history.__str__(), self.new_history.name)