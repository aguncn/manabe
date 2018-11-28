import json
from time import sleep
import jenkins

# 设置jenkins连接超时5秒
server = jenkins.Jenkins('http://192.168.1.112:8088',
                         username='root',
                         password='adminadmin',
                         timeout=5)


jenkins_job = 'ZEP-BACKEND-JAVA'
arg_dic = {
    'git_url': 'http://192.168.1.112/ZEP-BACKEND/ZEP-BACKEND-JAVA.git',
    'branch_build': 'master',
    'package_name': 'javademo-1.0.jar',
    'app_name': 'ZEP-BACKEND-JAVA',
    'deploy_version': '2018-0923-2232-24BP',
    'dir_build_file': 'javademo',
    'zip_package_name': 'javademo-1.0.tar.gz',
    }

next_build_number = server.get_job_info(jenkins_job)['nextBuildNumber']
server.build_job(jenkins_job, arg_dic)
print(next_build_number)
sleep(10)
build_info = server.get_build_info(jenkins_job, next_build_number)
print(json.dumps(build_info, sort_keys=True,
                 indent=4, separators=(',', ':')))
