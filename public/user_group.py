from django.contrib.auth.models import Group


def is_admin_group(user):
    try:
        user_group = Group.objects.get(user=user)
    except Exception as e:
        return False
    if "admin" == user_group:
        return False
    else:
        return True
