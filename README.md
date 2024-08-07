
# 1、项目结构
```plaintext
project-root
|   |-- logs #日志目录
|   |   `-- secure.log
|   |-- main.py  #服务的python脚本
|   |-- start.sh #启动文件
|   |-- utils #工具类
|   |   `-- logconfig.py
```
# 2、安装相关依赖
pip install -r requirements.txt

# 3、运行
相关参数,在start.sh中设置
```
#测试运行
./start.sh
#测试后台运行
nohup bash start.sh >> ./logs/log_scure.log 2>&1 &
#部署,gunicorn设置多个工作进程
nohup gunicorn -w 5 -k uvicorn.workers.UvicornWorker --timeout 600 main:app --bind 0.0.0.0:8888  --log-level debug --access-logfile ../logs/gunicorn_output.log >> ./logs/log_scure.log 2>&1 &

```
# 4、服务请求示例
```
curl --location 'http://127.0.0.1:8888/v1/security' \
--header 'Content-Type: application/json' \
--data '{
"input":["输入1","输入2","输入3，敏感词测试"]
}
'
```

