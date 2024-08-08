#!/bin/bash

# 启用调试模式
set -x

#*********************************1、测试****************************************************
# #命令行参数，变量名和等号之间不能有空格。
# Model_env=/nfs2/jiyuan.chen/Security-Model/model/server_test_model #模型
# Dat_env=/nfs2/zhaochuan.cai/czc_test/datrie/pydatrie/filter_pydatrie.dat  #双数组字典树
# Port_env=8888 #服务端口

# #运行python程序
# python -u main.py \
#     -m $Model_env \
#     -d $Dat_env \
#     -p $Port_env \
#     #  >> ./logs/log_scure.log 2>&1 &

#后台运行python程序
# nohup bash start.sh >> ./logs/log_scure.log 2>&1 &

#**********************************2、部署*****************************************************
#环境变量
export Model_env=/nfs2/jiyuan.chen/Security-Model/model/server_test_model  #模型
export Dat_env=/nfs2/zhaochuan.cai/czc_test/datrie/pydatrie/filter_pydatrie.dat #双数组字典树
export Port=8888 #服务端口
#gunicorn设置多个工作进程
# 【调试】- 请注意！--reload 参数仅应在开发时使用，不建议在生产环境中使用。
# gunicorn -w 5 -k uvicorn.workers.UvicornWorker --timeout 600 main:app --bind 0.0.0.0:$Port --reload --log-level debug --access-logfile ./logs/gunicorn_output.log

# 【生产】
# nohup gunicorn -w 5 -k uvicorn.workers.UvicornWorker --timeout 600 main:app --bind 0.0.0.0:8888  --log-level debug --access-logfile ../logs/gunicorn_output.log >> ./logs/log_scure.log 2>&1 &



#**********************************3、打包运行*****************************************************

#测试
./main 

#生产
# nohup bash start.sh >> log_scure.log 2>&1 &
   