import uuid
import time
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from django.conf import settings

from serverinput.models import Server
from .models import DeployPool, DeployStatus, History
from public.salt import salt_api_inst
from public.mablog import post_mablog


def deploy(subserver_list, deploy_type, is_restart_server,
           user_name, deploy_version, operation_type):

    worker_num = len(subserver_list[0])
    executor = ThreadPoolExecutor(max_workers=worker_num)

    # subserver_list格式[[1,2,3],[4,5,6],[7,8]]
    for item in subserver_list:
        if deploy_type in ['deployall', 'deploypkg', 'deploycfg']:
            cmd_list = ['prepare', 'backup', 'stop', deploy_type, 'start', 'check'] \
                if is_restart_server else ['prepare', 'backup', deploy_type, 'check']
        elif deploy_type == 'rollback':
            cmd_list = ['stop', 'rollback', 'start', 'check'] \
                if is_restart_server else ['rollback', 'check']
        elif deploy_type == 'stop':
            cmd_list = ['stop']
        elif deploy_type == 'start':
            cmd_list = ['start', 'check']
        elif deploy_type == 'restart':
            cmd_list = ['stop', 'start', 'check']
        else:
            return False
        cmd_len = len(cmd_list)
        for index, cmd in enumerate(cmd_list):
            # 根据命令的个数，计算每个命令执行完成之后的百分比
            percent_value = "%.0f%%" % ((index+1)/cmd_len*100)
            # 多线程版本，应用为IO密集型，适合threading模式

            server_id = []
            for itme_id in item:
                server_id.append(itme_id)
            server_len = len(server_id)
            for data in executor.map(cmd_run, server_id, [cmd] * server_len,
                                     [user_name] * server_len, [percent_value] * server_len,
                                     [deploy_version] * server_len, [operation_type] * server_len):
                if not data:
                    return False

    return True


def cmd_run(server_id, action, user_name, percent_value,
            deploy_version=None, operation_type=None):
    server_set = Server.objects.get(id=server_id)
    tgt = server_set.salt_name
    port = server_set.port
    app_user = server_set.app_user
    env_name = server_set.env_name.name.lower()
    app_name = server_set.app_name.name
    script_url = server_set.app_name.script_url
    zip_package_name = server_set.app_name.zip_package_name
    package_name = server_set.app_name.package_name
    nginx_url = settings.NGINX_URL

    if deploy_version != 'Demo':
        deploypool_set = DeployPool.objects.get(name=deploy_version)
        is_inc_tot = deploypool_set.is_inc_tot
        deploy_no = deploypool_set.deploy_no
    else:
        deploypool_set = None
        is_inc_tot = "tot"
        deploy_no = server_set.app_name.op_log_no

    arg_args = "-a {app_name} -e {env_name} -v {deploy_version} "\
               "-z {zip_package_name} -p {package_name} -o {port} " \
               "-c {action} -i {is_inc_tot} -u {nginx_url}".format(
                app_name=app_name,
                env_name=env_name,
                deploy_version=deploy_version,
                zip_package_name=zip_package_name,
                package_name=package_name,
                port=port,
                action=action,
                is_inc_tot=is_inc_tot,
                nginx_url=nginx_url
    )
    arg = [script_url, arg_args, 'runas='+app_user, 'env={"LC_ALL": ""}']
    result = salt_api_inst().cmd_script(tgt=tgt, arg=arg)
    try:
        result_retcode = result['return'][0][tgt]['retcode']
        result_stderr = result['return'][0][tgt]['stderr']
        result_stdout = result['return'][0][tgt]['stdout'].replace("\r\n", "")
        print(result_retcode, result_stderr, result_stdout, result, "@@@@@@@@@@@@@")
    except:
        return False
    if result_retcode == 0:
        if "deploy" in action or "rollback" in action:
            change_server(server_id, deploy_version, action, "success")
            change_deploypool(env_name, deploy_version, app_name, action)
        content = {'msg': 'success', 'ip': server_set.ip_address, 'action': action}
        log_content = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime()) + action + '\n' + tgt + ", deploy progress " + percent_value + '\n'
        post_mablog(app_name=app_name, ip_address=tgt, user_name=str(user_name),
                    operation_type=operation_type, operation_no=deploy_no,
                    deploy_version=deploy_version, env_name=env_name,
                    log_content=log_content)
        add_history(user_name, server_set.app_name, deploypool_set, server_set.env_name, operation_type, content)
    else:
        change_server(server_id, deploy_version, action, "error")
        change_deploypool(env_name, deploy_version, app_name, action)
        content = {'msg': 'error', 'ip': server_set.ip_address, 'action': action}
        log_content = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime()) + action + '\n' + tgt + ', error \n' + result
        post_mablog(app_name=app_name, ip_address=tgt, user_name=str(user_name),
                    operation_type=operation_type, operation_no=deploy_no,
                    deploy_version=deploy_version, env_name=env_name,
                    log_content=log_content)
        add_history(user_name, server_set.app_name, deploypool_set, server_set.env_name, operation_type, content)
        return False
    time.sleep(2)
    return True


# server的deploy_status用于记录在哪一个发布步骤出错，或是全部成功
# deploypool的deploy_status用于发布单的周期状态，
# #创建，编译，准备好发布，发布中，发布出错，完成等状态(它不包括环境信息)。
# 后者的状态依赖于前者状态的成功。后者已独立出一个表来进行管理。
def change_server(server_id, deploy_version, action, result):
    server_set = Server.objects.get(id=server_id)
    server_set.deploy_status = "{}:{}".format(action, result)
    if "deploy" in action:
        if server_set.history_deploy:
            # 最多只保留十个发布单用于回滚
            temp_list = server_set.history_deploy.split(",")
            if len(temp_list) > 10:
                history_deploy = deploy_version + ',' + ','.join(temp_list[:-1])
            else:
                history_deploy = deploy_version + ',' + server_set.history_deploy
        else:
            history_deploy = deploy_version
        server_set.history_deploy = history_deploy
    if "rollback" in action:
        # 首次发布，不能回滚
        if len(server_set.history_deploy.split(",")) < 2:
            result = {'return': u'没有可回滚版本'}
            return JsonResponse(result, status=400)
        else:
            server_set.history_deploy = ",".join(server_set.history_deploy.split(",")[1:])
    server_set.save()


def change_deploypool(server_env, deploy_version, app_name, action):
    deploypool_set = DeployPool.objects.get(name=deploy_version)
    server_env = server_env.upper()
    server_set = Server.objects.filter(app_name__name=app_name, env_name__name=server_env)
    svr_his_version_total = []
    svr_status_total = ""

    if "rollback" in action:
        # 回滚，只是改变服务器的历史发布单，不影响当前发布单状态。
        pass
    else:
        for server_item in server_set:
            if server_item.history_deploy is not None:
                temp_item = server_item.history_deploy.split(",")[0]
                if temp_item not in svr_his_version_total:
                    svr_his_version_total.append(temp_item)
                else:
                    pass
            else:
                svr_his_version_total.append("None")
            if server_item.deploy_status is not None:
                svr_status_total += server_item.deploy_status
            else:
                svr_status_total += "None"
        # 使用两个条件判断发布单状态，1，所有服务器的历史发布单是否更新，2，每一个服务器发布状态有无错误。

        if "error" in svr_status_total:
            deploy_status = DeployStatus.objects.get(name="ERROR")
        elif len(svr_his_version_total) > 1 and ("error" not in svr_status_total):
            deploy_status = DeployStatus.objects.get(name="ING")
        elif (len(svr_his_version_total) == 1) and ("error" not in svr_status_total):
            deploy_status = DeployStatus.objects.get(name="FINISH")
        else:
            deploy_status = DeployStatus.objects.get(name="ERROR")
        deploypool_set.deploy_status = deploy_status
        deploypool_set.save()


def add_history(user, app_name, deploy_name, env_name, operation_type, content):
    rid = uuid.uuid4()
    History.objects.create(
        name=rid,
        user=user,
        app_name=app_name,
        env_name=env_name,
        deploy_name=deploy_name,
        do_type=operation_type,
        content=content
    )

