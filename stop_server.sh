#!/bin/bash

uwsgi_pid=$( ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' )

if [[ ${uwsgi_pid} ]]
then

    echo "正在停止服务..."

    kill ${uwsgi_pid}

    echo "服务器停止"
    echo "启动product环境，执行：source start_server.sh "
    echo "                 或是：source start_server.sh product"
    echo "启动develop环境，执行：source start_server.sh develop"

else

    echo "没有服务在运行！"

fi
