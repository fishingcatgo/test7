
# cx_Freeze打包加密
from cx_Freeze import setup, Executable
#报import某个包错误，将代码中所有import的包加到下面，不要全部加pip导出的包名
packages=['typing','fastapi','uvicorn','pydantic','uuid','transformers','numpy','codecs','sys']

# 在这里定义要打包的数据文件，源路径:目标路径(支持文件和目录)，目标路径不能是绝对路径,在代码中用目标路径
# include_files = [
#     ('/nfs2/jiyuan.chen/Security-Model/model/server_test_model', 'data/model'),
#     ('/nfs2/zhaochuan.cai/czc_test/datrie/pydatrie/filter_pydatrie.dat','data/dat/filter_pydatrie.dat'),
#     './start.sh',
# ]

include_files = [
    ('/home/apollo/czc_data/server_test_model', 'data/model'),
    ('/home/apollo/czc_data/filter_pydatrie.dat','data/dat/filter_pydatrie.dat'),
    './start.sh',
]

# model_path='/nfs2/jiyuan.chen/Security-Model/model/server_test_model'
# dat_path="/nfs2/zhaochuan.cai/czc_test/datrie/pydatrie/filter_pydatrie.dat"

setup(
    name = "MtApp",
    version = "1.0",
    description = "Mt security application!",
    executables = [Executable("demo10.py")],
     options={'build_exe': {
        'packages': packages ,
        'include_files': include_files  # 数据文件/目录
    }},
)

#进入虚拟环境，执行以下命令即可完成打包
# python setup.py build
# python setup.py build_exe 

#代码中有中文，在代码文件中添加一下代码
# import sys
# import codecs
# # 确保标准输出和错误输出使用UTF-8编码
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

#中文字符问题，其他附加项（以上不能解决可以加）
# -*- coding: utf-8 -*-
# 终端环境变量
# export LANG=en_US.UTF-8
# export LC_ALL=en_US.UTF-8

# python demo9.py -m /nfs2/jiyuan.chen/Security-Model/model/server_test_model -d /nfs2/zhaochuan.cai/czc_test/datrie/pydatrie/filter_pydatrie.dat
