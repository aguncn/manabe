from django.test import TestCase
from model_mommy import mommy
from rightadmin.models import Action, Permission


class RightManageModelTestMommy(TestCase):
    def setUp(self):
        self.new_action = mommy.make(Action)
        self.new_permission = mommy.make(Permission)

    def test_action_creation_mommy(self):
        self.assertTrue(isinstance(self.new_action, Action))
        self.assertEqual(self.new_action.__str__(), self.new_action.name)

    def test_permission_creation_mommy(self):
        self.assertTrue(isinstance(self.new_permission, Permission))
        self.assertEqual(self.new_permission.__str__(), self.new_permission.name)