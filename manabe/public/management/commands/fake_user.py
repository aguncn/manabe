from django.contrib.auth.models import User, Group


def fake_user_data():
    User.objects.all().delete()
    Group.objects.all().delete()
    print('delete all user data')
    User.objects.create_user(username='Dylan', password="password")
    User.objects.create_user(username='Tyler', password="password")
    User.objects.create_user(username='Kyle', password="password")
    User.objects.create_user(username='Dakota', password="password")
    User.objects.create_user(username='Marcus', password="password")
    User.objects.create_user(username='Samantha', password="password")
    User.objects.create_user(username='Kayla', password="password")
    User.objects.create_user(username='Sydney', password="password")
    User.objects.create_user(username='Courtney', password="password")
    User.objects.create_user(username='Mariah', password="password")
    User.objects.create_user(username='tom', password="password")
    User.objects.create_user(username='mary', password="password")
    admin = User.objects.create_superuser('admin', 'admin@demon.com', 'admin')
    root = User.objects.create_superuser('root', 'root@demon.com', 'root')
    admin_group = Group.objects.create(name='admin')
    Group.objects.create(name='test')
    Group.objects.create(name='dev')
    Group.objects.create(name='operate')
    admin_users = [admin, root]
    admin_group.user_set.set(admin_users)
    print('create all user data')