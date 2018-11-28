#coding=utf-8
import base64
#导入python-gitlab库
import gitlab

url = 'http://192.168.1.112'
token = 'D98-t7HJpXxwhq8qbXcJ'

# 登录
gl = gitlab.Gitlab(url, token)

#获取项目
project = gl.projects.get('ZEP-BACKEND/ZEP-BACKEND-JAVA')
#获取javademo/config目录下文件列表,版本为master
items = project.repository_tree(path='javademo', ref='master')

def get_all_files(path=None, ref='master'):
    items = project.repository_tree(path=path, ref=ref)
    for item in items:
        if item['mode'] == '040000':
            # 调用递归，实现目录递归输出
            get_all_files(item['path'], ref)
        if item['mode'] == '100644':
            print("===({})===".format(item['path']))

get_all_files(path='javademo', ref='master')
