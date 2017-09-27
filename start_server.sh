#!/bin/bash

# 默认是product，要是启动develop 加上 develop参数
mode='product'
if [ $1 ]
then
    mode=$1
fi

if [[ 'product' != ${mode} && 'develop' != ${mode} ]]
then

     echo "启动develop环境，执行：source start_server.sh develop"
     echo "启动product环境，执行：source start_server.sh "
     echo "                 或是：source start_server.sh product"
     return

fi

uwsgi_pid=$( ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' )

if [[ ${uwsgi_pid} ]]
then

    echo "当前有服务正在运行！"
    echo "请执行：sh stop_server.sh 来停止当前服务"
    return

fi

# 启动环境
source .env/bin/activate

export FLASK_CRAWL_MODE=${mode}

# 只输出错误信息到~/logs/uwsgi_error_out.txt
nohup uwsgi --ini config.ini >/dev/null 2>~/logs/uwsgi_error_out.txt &

if [[ 'product' = ${mode} ]]
then

     echo "当前服务器启动的是product环境"
     echo "如果想启动develop环境，执行：source start_server.sh develop"

elif [[ 'develop' = ${mode} ]]
then

     echo "当前服务器启动的是develop环境"
     echo "启动product环境，执行：source start_server.sh "
     echo "                 或是：source start_server.sh product"

fi
