#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# a(app)e(env)v(version)z(zip)p(pkg)
# o(port)c(act)i(inc_tot)u(url)
# -a ZEP-BACKEND-JAVA -e test -v 2018-1021-112802QG -z javademo-1.0.tar.gz   \
# -p javademo-1.0.jar -o 8080 -c stop -i TOT -u http://192.168.1.111
while getopts "a:e:v:z:p:o:c:i:u:" opt
do
  case $opt in
          a ) APP="$OPTARG";;
          e ) ENV="$OPTARG";;
          v ) VER="$OPTARG";;
          z ) ZIP="$OPTARG";;
          p ) PKG="$OPTARG";;
          o ) PORT="$OPTARG";;
          c ) ACT="$OPTARG";;
          i ) INC_TOT="$OPTARG";;
          u ) URL="$OPTARG";;
          ? ) echo "error"
              exit 1;;
  esac
done
echo $APP $ENV $VER $ZIP $PKG $PORT $ACT $INC_TOT $URL

# app部署根目录
APP_ROOT_HOME="/app"
# app软件包保存根目录
LOCAL_ROOT_STORE="/var/ops"


APP_HOME=$APP_ROOT_HOME/$APP
LOCAL_STORE=$LOCAL_ROOT_STORE/$APP/$VER
LOCAL_BACKUP=$LOCAL_ROOT_STORE/$APP/BACKUP


psid=0

# 获取应用的进程号，没有就返回0号。
pid_of_app() {
    psid=$(pgrep -f "java.*${PKG}")
    psid=${psid/$$}
    psid=$psid|tr -d " "
    if [ -z "$psid" ];then
        psid=0
    fi
    echo $psid "@@@@@@@@@@@@@"
}

#
rm_tmp_file() {
	rm -rf $LOCAL_STORE/$ZIP
	rm -rf $LOCAL_STORE/tmp/*
}


# 回滚，即将本地保存的软件包cp到应用目录
rollback() {
	rm -rf $APP_HOME/*
	cp -arp $LOCAL_BACKUP/* $APP_HOME
	echo "$APP rollback success."
}

# 保存当前版本软件包，以便用于本地回滚操作
backup() {
	mkdir -p $LOCAL_BACKUP
	rm -rf $LOCAL_BACKUP/*
	if [ "$(ls -A $APP_HOME)" ];then
	    cp -arp $APP_HOME/* $LOCAL_BACKUP
	fi
	echo "$APP backup success."
}

# 先建立相关目录，再从nginx上获取指定软件包，保存到指定目录
prepare() {
	if [ ! -d $APP_HOME  ];then
	  mkdir -p $APP_HOME
	fi
	if [ ! -d $LOCAL_STORE  ];then
	  mkdir -p $LOCAL_STORE
	fi
	
	if [ -f "$LOCAL_STORE/$ZIP" ];then
		echo "$LOCAL_STORE/$ZIP found."
	else
		wget -P $LOCAL_STORE $URL/$APP/$VER/$ZIP
		mkdir -p  $LOCAL_STORE/tmp/
		tar -xzvf $LOCAL_STORE/$ZIP -C $LOCAL_STORE/tmp/
	fi
	echo "$APP prepare success."

}


# 部署所有
deployall() {
	if [ IS_INC_TOT == "TOT" ]; then
		rm -rf $APP_HOME/*
		cp -rf $LOCAL_STORE/tmp/* $APP_HOME
		rm_tmp_file
		echo "$APP deployall tot success."
	else
		cp -rf $LOCAL_STORE/tmp/* $APP_HOME
		rm_tmp_file
		echo "$APP deployall inc success."
	fi
}

# 部署软件包(不同的应用软件包，这里会不同，一个软件包，增量全量一样)
deploypkg() {
	if [ IS_INC_TOT == "TOT" ]; then
		rm -rf $APP_HOME/$PKG
		cp -rf $LOCAL_STORE/tmp/$PKG $APP_HOME
		rm_tmp_file
		echo "$APP deploypkg tot success."
	else
		rm -rf $APP_HOME/$PKG
		cp -rf $LOCAL_STORE/tmp/$PKG $APP_HOME
		rm_tmp_file
		echo "$APP deploypkg inc success."
	fi
}

# 部署配置（分环境提取文件）
deploycfg() {
	if [ IS_INC_TOT == "TOT" ]; then
		rm -rf $APP_HOME/configs/*
		cp -rf $LOCAL_STORE/tmp/configs/$ENV/* $APP_HOME/configs/
		rm_tmp_file
		echo "$APP deploycfg tot success."
	else
		cp -rf $LOCAL_STORE/tmp/config/$ENV/* $APP_HOME/configs/
		rm_tmp_file
		echo "$APP deploycfg inc success."
	fi
}


#启动应用，传递了port和env参数，注意先判断。
start() {
	pid_of_app  
  if [ $psid -ne 0 ]; then  
  	echo "$APP already started, error."  
    exit 1 
  else  
  	nohup java -jar "$APP_HOME/$PKG" \
		--server.port=$PORT  \
		--spring.profiles.active=$ENV > /tmp/log 2>&1 &
		pid_of_app
    if [ $psid -ne 0 ]; then  
    	echo "$APP start success." 
    else  
			echo "$APP start error."  
    	exit 1 
    fi  
  fi  

}

#停止应用，注意先判断。
stop() {
    pid_of_app
		if [ $psid -ne 0 ]; then  
    	kill -9 $psid
    	if [ $? -eq 0 ]; then
      	echo "$APP stop success."
      else
        echo "$APP stop error."
    		exit 1
      fi
      
      pid_of_app
      if [ $psid -ne 0 ]; then
         stop
      fi

		else
      echo "$APP has stoped."
		fi
}

# 业务应用自实现
check() {
	
	    echo "$APP check success."
}

case "$ACT" in
	backup) backup;;
	prepare) prepare;;
	deployall) deployall;;
	deploypkg) deploypkg;;
	deploycfg) deploycfg;;
	rollback) rollback;;
    start) start;;
    stop) stop;;
	check) check;;
    *)
        echo $"Usage: $0 {8 args}"
        exit 1;;
esac
