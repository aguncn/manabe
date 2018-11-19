# coding=utf8
from rest_framework import serializers
from django.contrib.auth.models import User
from serverinput.models import Server
from appinput.models import App
from deploy.models import DeployPool


class UserSerializer(serializers.HyperlinkedModelSerializer):
    deploy_create_user = serializers.HyperlinkedRelatedField(many=True,
                                                             view_name='api:deploypool-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'deploy_create_user',)


class ServerSerializer(serializers.HyperlinkedModelSerializer):
    create_user = serializers.ReadOnlyField(source='create_user.username')
    app_name = serializers.ReadOnlyField(source='app_name.name')
    env_name = serializers.ReadOnlyField(source='env_name.name')

    class Meta:
        model = Server
        fields = ('id', 'name', 'ip_address', 'env_name', 'app_name', 'create_user')


class DeployPoolSerializer(serializers.ModelSerializer):
    create_user = serializers.ReadOnlyField(source='create_user.username')
    app_name = serializers.ReadOnlyField(source='app_name.name')
    is_restart_status = serializers.ReadOnlyField(source='app_name.is_restart_status')
    deploy_status = serializers.ReadOnlyField(source='deploy_status.description')

    class Meta:
        model = DeployPool
        fields = ('id', 'name', 'app_name', 'is_inc_tot', 'create_user',
                  'deploy_type', 'is_restart_status', 'deploy_status', 'change_date')


class AppSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = App
        fields = ('id', 'name', 'jenkins_job', 'git_url', 'script_url')