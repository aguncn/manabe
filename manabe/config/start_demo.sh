#!/bin/bash

# app部署根目录
APP_ROOT_HOME="/app"
# app软件包保存根目录
LOCAL_ROOT_STORE="/var/ops"
# app名称参数
PROJECT_NAME=$1
# env环境参数
ENV=$2
# version发布单参数
VERSION=$3
# app软件包名单数
PACKAGE_NAME=$4
# port服务端口参数
PORT=$5
# action服务启停及部署参数
ACTION=$6
# deploy_type部署类型参数
DEPLOY_TYPE=$7
# repo_url nginx软件仓库地址参数
REPO_URL=$8
# app压缩包名参数
ZIP_PACKAGE_NAME=$9

APP_HOME=$APP_ROOT_HOME/$1
LOCAL_STORE=$LOCAL_ROOT_STORE/$1/$3
     
LOG="$APP_HOME/$PROJECT_NAME.log"

RETVAL=0

pid_of_app() {
    pgrep -f "java.*$PACKAGE_NAME"
}

# 先建立相关目录，再从nginx上获取指定软件包，保存到指定目录
prepare() {
	if [ ! -d $APP_HOME  ];then
	  mkdir -p $APP_HOME
	fi
	if [ ! -d $LOCAL_STORE  ];then
	  mkdir -p $LOCAL_STORE
	fi
	
	if [ -f "$LOCAL_STORE/$ZIP_PACKAGE_NAME" ];then
		echo "$LOCAL_STORE/$ZIP_PACKAGE_NAME found."
	else
		wget -P \
$LOCAL_STORE $REPO_URL/$PROJECT_NAME/\
$VERSION/$ZIP_PACKAGE_NAME
	fi
	echo "$PROJECT_NAME prepare success."

}

# 清除目录已有文件，将软件解压到运行目录
deploy() {
	rm -rf $APP_HOME/*
	tar -xzvf $LOCAL_STORE/$ZIP_PACKAGE_NAME -C $APP_HOME
	echo "$PROJECT_NAME deploy success."
}

#启动应用，传递了port和env参数
start() {
    pid=`pid_of_app`
    if [ -n "$pid" ]; then
        echo "Project: $PROJECT_NAME (pid $pid) is running, kill first or restart."
        return 1
    fi

    start=$(date +%s)
    [ -e "$LOG" ] && cnt=`wc -l "$LOG" | awk '{ print $1 }'` || cnt=1

    echo -n $"Starting $PROJECT_NAME: "

    cd "$APP_HOME"
    jarcount=`ls -l *.jar |wc -l`
    if [ ! $jarcount = 1 ]; then
        echo "more than one jar files in $APP_HOME"
        return 1
    fi
	#此处为真正启动命令
nohup java -jar "$APP_HOME/$(ls *.jar)" \
--server.port=$PORT  \
--spring.profiles.active=$ENV >> "$LOG" 2>&1 &

    while { pid_of_app > /dev/null ; } &&
        ! { tail --lines=+$cnt "$LOG" | grep -q 'Started App in' ; } ; do
        sleep 1
    done

    pid=`pid_of_app`
    RETVAL=$?
    if [ $RETVAL = 0 ]; then
        end=$(date +%s)
        echo "start success in $(( $end - $start )) seconds with (pid $pid)"
    else
        echo "Start failure, please check $LOG \n"
    fi
    echo
}

stop() {
    printf "Stopping $PROJECT_NAME: "

    pid=`pid_of_app`
    [ -n "$pid" ] && kill $pid
	echo $pid
    RETVAL=$?
    cnt=10
    while [ $RETVAL = 0 -a $cnt -gt 0 ] &&
        { pid_of_app > /dev/null ; } ; do
            sleep 1
            ((cnt--))
    done
    printf "stop success\n"
}

status() {
    pid=`pid_of_app`
    if [ -n "$pid" ]; then
        echo "Project: $PROJECT_NAME (pid $pid) is success running..."
        return 0
    fi
    echo "Project: $PROJECT_NAME is stopped"
    return 1
}

case "$ACTION" in
	prepare)
        prepare
        ;;
	deploy)
        deploy
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo $"Usage: $0 {8 args}"
        exit 1
esac

exit $RETVAL
