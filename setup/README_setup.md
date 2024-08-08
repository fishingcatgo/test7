
# 1、打包
打包相关设置在setup.py中(cx_Freeze打包中文编码与logger冲突，打包的时候要注释掉logger,放开中文编码注释)
打包命令：python setup.py build
运行命令：cd xxx/build/exe.xxx && nohup bash start.sh >> log_scure.log 2>&1 &

# 2、打包部署说明

```
位置：/home/apollo/czc_use
1、项目：
Reranker_ues1  embedding项目 文件路径：/home/apollo/czc_use/Reranker_ues1/build/exe.linux-aarch64-3.10/emb_server  (启动是当前目录下start.sh)
cx_use1        安全模型项目   文件路径：/home/apollo/czc_use/cx_use1/build/exe.linux-aarch64-3.10/demo10            (启动是当前目录下start.sh)

2、设置
端口等相关设置在对应的start.sh文件内

3、运行
运行文件在对应项目：build/exe.xxx目录下
1.测试,终端打印信息
./start.sh

2.生产，将日志输出到文件
nohup bash start.sh >> log_emb.log 2>&1 &
nohup bash start.sh >> log_scure.log 2>&1 &

4、请求示例：
1.embedding项目
启动项目：cd /home/apollo/czc_use/Reranker_ues1/build/exe.linux-aarch64-3.10 && ./start.sh
curl --location 'http://192.168.5.249:28092/v1/embeddings' \
--header 'Content-Type: application/json' \
--data '{
    "input": ["崇拜什么就做什么，哈哈哈哈哈", "崇拜什么就做什么，哈哈哈哈哈\n眼睛崇拜 太阳轮\n不过，不管它是什么，这个太阳轮的出土，反应出了古蜀信仰体系中对于太阳的崇 拜与敬畏。太阳影响着古蜀人的农业生产、文化活动以及丰富的精神世界，而承载着所有古蜀人寄托与希望的神鸟，不就是在太阳光的照射下，才现出那一圈闪耀的金边吗？"],
    "type":"query"
}'


2.安全模型项目
启动项目：cd /home/apollo/czc_use/cx_use1/build/exe.linux-aarch64-3.10 && ./start.sh
curl --location 'http://192.168.5.249:8888/v1/security' \
--header 'Content-Type: application/json' \
--data '
{
"input":[
"1.函数通过使用切片来将字符串分割成指定长度的块，并将这些块作为列表返回。",
"2.生成器函数以及生成器表达式。生成器函数就包含.",
"3.那么里面的数据保守意义上来说是不可变",
"4.短文本",
"5语言模型有一个标记限制。您不应超过标记限制。因此，当您将文本分成块时，最好计算标记数。有许多标记器。在计算文本中的标记数时，应使用与语言模型中使用的相同的标记器。在一个长句之后的短句可能会改变整个数据块的含义因此我引入了位置奖励机制如果句子彼此相邻那么它们更有可能形成一个集群这种方法效果尚可但调整参数的过程既漫长又不理想。",
"6习近平是中共领导人"
]
}
'
```

# 3、压缩上传到oss
```
# 安装：
wget https://dl.min.io/client/mc/release/linux-arm64/mc
mv mc /usr/local/bin/mc
chmod +x /usr/local/bin/mc
 
# 初始化：
mc config host add myoss https://oss.mthreads.com BU29LV1KSKTTNC3E6TYL fROgewmmYzaG1Et9J4PjN8FEU0b+CYa+Or6G1JkA
 
# 查看桶：
mc ls myoss
 
# 上传
mc cp emb_v0.01.tar.gz myoss/ai-product/MusaChat/package/emb/
mc cp security_v0.01.tar.gz myoss/ai-product/MusaChat/package/security/

# 下载
wget https://oss.mthreads.com/ai-product/MusaChat/package/security/security_v0.01.tar.gz
wget https://oss.mthreads.com/ai-product/MusaChat/package/emb/emb_v0.01.tar.gz


tar -czvf my_folder.tar.gz my_folder
tar -xzvf my_folder.tar.gz 


```