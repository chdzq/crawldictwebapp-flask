#!/bin/bash

uwsgi_pid=$( ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' )

if [[ ${uwsgi_pid} ]]
then

    echo "正在停止服务..."

    kill ${uwsgi_pid}

    echo "等待提示：[*]  + *** done       nohup uwsgi --ini config.ini"

else

    echo "没有服务在运行！"

fi
