# 目标
  	从金山词霸、海词中爬取单词音标，然后转换成arpabet，存储到MongoDB中

	POST方式访问http://0.0.0.0:8080/crawl，
	返回数据：{
				"result": 0,
				"body": {"with": "W IH1 DH"},
				"message": ""
			}
# 部署

## 环境：

python3

`virtualenv .env --python=python3`

## 安装

`pip install -r requirements.txt`

## 配置

1. 配置ngix

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

2. 启动nginx

	`/usr/nginx/sbin/nginx -s reload `

3. 其他相关：redis和mongodb

## 启动服务

1. 正式环境

    `source start_server.sh`

2. 测试环境

  	`source start_server.sh develop`

3. 停止服务

  	`sh stop_server.sh`
