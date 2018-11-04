from django.conf import settings
import requests
import json

PRISMLOGAPI_URL = settings.__getattr__("MABLOG_URL")


def post_mablog(app_name=None, ip_address=None, user_name=None,
                operation_type=None, operation_no=None,
                deploy_version=None, env_name=None, log_content=None):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    payload = {'deploy_version': deploy_version,
               'app_name': app_name,
               'ip_address': ip_address,
               'env_name': env_name,
               'user_name': user_name,
               'operation_type': operation_type,
               'operation_no': operation_no,
               'log_content': log_content}

    try:
        response = requests.post(PRISMLOGAPI_URL+"/wslog/log_add/", headers=headers, data=json.dumps(payload))
        print(response.status_code)
    except Exception as e:
        print(e)