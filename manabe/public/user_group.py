from django.contrib.auth.models import Group
from appinput.models import App
from rightadmin.models import Permission


# 判断是否前台管理员组
def is_admin_group(user):
    try:
        user_group = Group.objects.get(user=user)
    except Exception as e:
        return False
    if "admin" == user_group:
        return False
    else:
        return True


# 判断是否为APP管理员
def is_app_admin(app_id, user):
    app = App.objects.get(id=app_id)
    if user == app.manage_user or is_admin_group(user):
        return True
    return False


# 获取APP管理员
def get_app_admin(app_id):
    return App.objects.get(id=app_id).manage_user


# 获取APP的各个权限的相关成员
def get_app_user(app_id, action_id, env_id):
    filter_dict = dict()
    filter_dict['app_name__id'] = app_id
    filter_dict['action_name__id'] = action_id
    if env_id != '0':
        filter_dict['env_name__id'] = env_id
    permission_set = Permission.objects.get(**filter_dict)
    user_set = permission_set.main_user.all()
    return user_set


# 判断是否具有APP的相关环境的相关权限
def is_right(app_id, action_id, env_id, user):
    # 是管理员，可直接具有相关权限
    if is_app_admin(app_id, user):
        return True
    filter_dict = dict()
    filter_dict['app_name__id'] = app_id
    filter_dict['action_name__id'] = action_id
    if env_id != '0':
        filter_dict['env_name__id'] = env_id
    try:
        permission_set = Permission.objects.get(**filter_dict)
        user_set = permission_set.main_user.all()
        if user in user_set:
            return True
    except Permission.DoesNotExist:
        pass
    return False
