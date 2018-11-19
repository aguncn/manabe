# coding=utf8
from rest_framework import viewsets
from .serializers import UserSerializer, ServerSerializer, DeployPoolSerializer, AppSerializer
from .renderer import Utf8JSONRenderer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsOwnerOrReadOnly
from appinput.models import App
from serverinput.models import Server
from deploy.models import DeployPool
from envx.models import Env
from datetime import date, datetime, timedelta
from django.utils import timezone
import logging


mylog = logging.getLogger('manabe')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class AppViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    paginate_by = 100

    # 如有需要，自定义update和create方法，以实现外键方面的关联
    def create(self, request, *args, **kwargs):
        validated_data = dict()
        validated_data['name'] = request.data['name']
        validated_data['create_user'] = request.user

        try:
            Server.objects.create(**validated_data)
            response_data = {
                'result': 'success',
                'message': u'新服务器插入数据库成功！'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            response_data = {
                'result': 'failed',
                'message': u'不能正确插入数据库'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        name = request.data['name']
        try:

            DeployPool.objects.filter(name=name).update(order_no=order_no, version_name=None)
            response_data = {
                'result': 'success',
                'name': name,
                'create_user': request.user.username,
                'message': u'更新发布单成功！'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            response_data = {
                'result': 'failed',
                'message': u'更新发布单失败！'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ServerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    # 如有需要，自定义update和create方法，以实现外键方面的关联
    def create(self, request, *args, **kwargs):
        try:
            aa = TokenAuthentication()
            user_name, token = aa.authenticate(request)
            print(user_name, token)
        except Exception as e:
            print(e)
            result = {'return': 'fail', 'message': "auth fail."}
            return Response(result, status=403)
        if user_name != request.user:
            result = {'return': 'fail', 'message': "others token."}
            return Response(result, status=403)
        validated_data = dict()
        validated_data['name'] = request.data['name']
        validated_data['ip_address'] = request.data['ip_address']
        validated_data['port'] = request.data['port']
        validated_data['salt_name'] = request.data['salt_name']
        validated_data['app_name'] = App.objects.get(name=request.data['app_name'])
        validated_data['env_name'] = Env.objects.get(name=request.data['env_name'])
        validated_data['app_user'] = request.data['app_user']
        validated_data['op_user'] = request.user

        try:
            Server.objects.create(**validated_data)
            mylog.debug("create server is {}. ".format(validated_data))
            response_data = {
                'result': 'success',
                'message': u'新服务器插入数据库成功！'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            response_data = {
                'result': 'failed',
                'message': u'不能正确插入数据库'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            aa = TokenAuthentication()
            user_name, token = aa.authenticate(request)
            print(user_name, token)
        except Exception as e:
            print(e)
            result = {'return': 'fail', 'message': "auth fail."}
            return Response(result, status=403)
        if user_name != request.user:
            result = {'return': 'fail', 'message': "others token."}
            return Response(result, status=403)
        validated_data = dict()
        validated_data['name'] = request.data['name']
        validated_data['ip_address'] = request.data['ip_address']
        validated_data['port'] = request.data['port']
        validated_data['salt_name'] = request.data['salt_name']
        validated_data['app_name'] = App.objects.get(name=request.data['app_name'])
        validated_data['env_name'] = Env.objects.get(name=request.data['env_name'])
        validated_data['app_user'] = request.data['app_user']
        validated_data['op_user'] = request.user

        pk_id = kwargs["pk"]
        try:
            server_item = Server.objects.filter(pk=pk_id)
            server_item.update(**validated_data)
            mylog.debug("udpate server {} is {}. ".format(pk_id, validated_data))
            response_data = {
                'result': 'success',
                'name': pk_id,
                'create_user': request.user.username,
                'message': u'更新发布单成功！'
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            response_data = {
                'result': 'failed',
                'message': u'更新发布单失败！'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class DeployPoolViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    serializer_class = DeployPoolSerializer

    def get_queryset(self):
        filter_dict = dict()
        current_date = timezone.now()
        filter_dict['change_date__gt'] = current_date - timedelta(days=365)
        return DeployPool.objects.filter(**filter_dict)
