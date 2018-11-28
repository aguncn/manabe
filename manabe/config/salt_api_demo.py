def demo():
    sapi = SaltStack(host="192.168.1.111",
                     port='8899',
                     username="salt-api-client",
                     password="salt2018",
                     secure=True)
    # 为了语义明晰，使用列表
    attach_arg_list = [None]*9
    attach_arg_list[0] = "ZEP-BACKEND-JAVA"
    attach_arg_list[1] = "test"
    attach_arg_list[2] = "2018-0921-2023-34XZ"
    attach_arg_list[3] = "javademo-1.0.jar"
    attach_arg_list[4] = "18080"
    attach_arg_list[5] = "stop"
    attach_arg_list[6] = "tot"
    attach_arg_list[7] = "http://192.168.1.111"
    attach_arg_list[8] = "javademo-1.0.tar.gz"

    # cmd_script后面附加参数为字符串，所以要进行转换
    attach_arg = ' '.join(attach_arg_list)
    
	result = sapi.cmd_script(tgt='192.168.1.112',
                            arg=["http://192.168.1.111/scripts/ZEP-BACKEND-JAVA.sh",
							attach_arg])
    print(result['return'][0]['192.168.1.112']['stdout'])

if __name__ == '__main__':
    demo()
