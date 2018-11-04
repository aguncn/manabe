from django.core.management.base import BaseCommand

from .fake_user import fake_user_data
from .fake_app import fake_app_data
from .fake_env import fake_env_data
from .fake_server import fake_server_data
from .fake_deploy_status import fake_deploy_status_data
from .fake_deploy import fake_deploy_data
from .fake_action import fake_action_data
from .fake_permission import fake_permission_data


class Command(BaseCommand):
    help = 'It is a fake command, Import init data for test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin fake data'))
        fake_user_data()
        fake_app_data()
        fake_env_data()
        fake_server_data()
        fake_deploy_status_data()
        fake_deploy_data()
        fake_action_data()
        fake_permission_data()
        self.stdout.write(self.style.SUCCESS("end fake data"))










