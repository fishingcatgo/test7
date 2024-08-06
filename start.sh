#!/bin/bash

# 启用调试模式
set -x

#环境变量，变量名和等号之间不能有空格。
Model_env=/nfs2/jiyuan.chen/Security-Model/model/server_test_model #模型
Dat_env=/nfs2/zhaochuan.cai/czc_test/datrie/pydatrie/filter_pydatrie.dat  #双数组字典树
Port_env=8888 #服务端口


python -u main.py \
    -m $Model_env \
    -d $Dat_env \
    -p $Port_env \
    #  >> ./logs/log_scure.log 2>&1 &

#后台运行
# nohup bash start.sh >> ./logs/log_scure.log 2>&1 &