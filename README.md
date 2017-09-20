# 部署
1. 环境： python3

	 `virtualenv .env --python=python3`
2. 安装相关包

	 `pip install -r requirements.txt`
3. 配置ngix
   
	```
	server {
		listen       8000;
		server_name  localhost;
		location = /arpabet { rewrite ^ /arpabet/; }
		location /arpabet { try_files $uri @arpabet; }
		location @arpabet {
			include uwsgi_params;
    		uwsgi_pass unix:/tmp/crawldictwebapp-flask.sock;
		}
	}
	```

4. 启动

  	`uwsgi --ini config.ini `
5. 启动nginx

	`/usr/nginx/sbin/nginx -s reload `

6. 其他相关：redis和mongodb
