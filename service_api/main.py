
from typing import Union
from fastapi import FastAPI,Query
import uvicorn
from pydantic import BaseModel,Field
from typing import Union,Optional,Literal
import argparse
import os
from typing import (
    Deque
)
#低版本python，3.10以下
# from typing import (
#     Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
# )

#异常相关包
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
import sys

#日志记录
from utils.logconfig import logger   # 引入你的 logger


app = FastAPI()


#1、全局异常捕获
#代码内部异常
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print('*'*100)
    uid=str(uuid.uuid1())
    print("request_id请求ID:",uid)
    print('内部异常:')
    print('请求路径:',request.method,request.url)

    #获取请求体
    if request.method == "POST":
        try:   
            json_body = await request.json()
            print('post请求体:',json_body)
        except Exception as e:
            # print('json处理异常:',Exception)
            print('post请求json解析异常,json可能为空或不是json格式')
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {e}")
            print(f"Exception details: {sys.exc_info()}")

             #记录日志
            logger.info(f"request_id:{uid}; 【error】全局捕获代码异常; 【error messenger】{e}")
            logger.info(f"request_id:{uid}; 【request body】{json_body}")
        
    if request.method == "GET":
        try:   
            # json_body = await request.json()
            json_body = dict(request.query_params)  # 将查询参数转换为普通字典
            print('get请求体:',json_body)
        except Exception as e:
            # print('json处理异常:',Exception)
            print('get请求解析异常,参数可能为空或格式错误')
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {e}")
            print(f"Exception details: {sys.exc_info()}")

             #记录日志
            logger.info(f"request_id:{uid}; 【error】全局捕获代码异常; 【error messenger】{e}")
            logger.info(f"request_id:{uid}; 【request body】{json_body}")

    print('抛出异常信息:')
    print(exc)
    print('*'*100)
     #记录日志
    logger.info(f"request_id:{uid}; 【error】全局捕获代码异常; 【error messenger】{exc}")
    logger.info(f"request_id:{uid}; 【request body】{json_body}")
    
    return JSONResponse(
            status_code=500,
            content={"request_id": uid,"code": "1903","message": "server_error","data":[]},
        )
    

#请参数异常
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print('*'*100)
    uid=str(uuid.uuid1())
    print("request_id请求ID:",uid)
    print('请求体异常:')
    print('请求路径:',request.method,request.url)

    #request异常有errors和body属性，可以获取到请求体
    print('抛出异常信息:')
    print(exc)
    print("detail",exc.errors())
    print("body",exc.body)
    print('*'*100)

     #记录日志
    logger.info(f"request_id:{uid}; 【error】请求体异常; 【error messenger】{exc}")
    logger.info(f"request_id:{uid}; 【request body】{exc.body}")
    return JSONResponse(
            status_code=400,
            content={"request_id": uid,"code": "1902","message": "illegal_params","data":[]},
        )


# 2、解决打包中文编码问题,只在cx_Freeze打包的时候用,部署不能用,影响日志输出
# import sys
# import codecs
# # 确保标准输出和错误输出使用UTF-8编码
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

#3、给路径参数赋值，多进程不支持命令行参数argparse，测试用
# #命领行参数获取
# def get_Parser():
#     # 定义一个ArgumentParser实例:
#     parser = argparse.ArgumentParser(
#         prog='mt_security', # 程序名
#         description='mt_security relevant arg.', # 描述
#         epilog='Mt ArgumentParser, 2024' # 说明信息
#     )
#      # 允许用户输入简写的-x:
#     parser.add_argument('-m', '--model',help='model path parameter', required=False,default=None)
#     parser.add_argument('-d', '--dat', help='Dat tree path parameter',required=False,default=None)
#     parser.add_argument('-p', '--port', help='api port parameter',required=False,default='8888',type=int)

#     # 解析参数:
#     args = parser.parse_args()
#     print('解析完参数：',args)
#     return args

# args=get_Parser()


#环境变量获取
Model_env = os.getenv('Model_env')
Dat_env= os.getenv('Dat_env')
Port_env= os.getenv('Port_env')
print('环境变量：',Model_env,Dat_env,Port_env)

# port=Port_env if Port_env else args.port

#测试用
# model_path='/nfs2/jiyuan.chen/Security-Model/model/server_test_model'
# dat_path="/nfs2/zhaochuan.cai/czc_test/datrie/pydatrie/filter_pydatrie.dat"

model_path=''
dat_path=''

# 选取存在的路径
for path in [Model_env,model_path] :
    if path and os.path.exists(path): model_path=path; break

for path in [Dat_env,dat_path] :
    if path and os.path.exists(path): dat_path=path; break

print('模型路径：',model_path)
print('dat字典树路径:',dat_path)

if not model_path or not dat_path:
    print('路径为空')
    quit("程序终止：路径不能为空，请设置正确的模型路径")



# 4、get请求，健康测试
@app.get("/healthcheck")
async def healthcheck():
    print('健康检测')
    return {"status": "healthy"}

from uuid import UUID
#5、数据类
# 请求数据
class SecureRequest(BaseModel):
    input:Union[str,list[str],None] #选择，可以为空
    type:Union[str,None]=None #等价Optional[str]

# 返回数据
class SecureRespond(BaseModel):

    class DataItem(BaseModel):
        class Labels(BaseModel):
            probability: float = Query(default=0,ge=0, le=1) #float 0~1之间的小数
            label:  Literal['politics','porn','ad','violence','ban','abuse','private','pass'] #中的任意一个

        index: int
        label: Literal['politics','porn','ad','violence','ban','abuse','private','pass'] #中的任意一个
        all_labels: list[Labels]

    request_id: str | UUID
    code: Literal['1100','1901','1902','1903']
    message: Literal['success','qps_limited','illegal_params','server_error']
    data: list[DataItem] |None=None
     
# 1100：success 成功
# 1901：qps_limited QPS超限
# 1902：illegal_params 参数不合法
# 1903：server_error 服务失败
# '1100','1901','1902','1903'
# 'success','qps_limited','illegal_params','server_error'





#6、安全模型数据接口
@app.post("/v1/security",response_model=SecureRespond)  #返回数据校验没生效
async def create_secure(secu_data: SecureRequest) -> SecureRespond:
    # print('输入：',secu_data.dict())
    uid=str(uuid.uuid1())
    print("request_id请求ID:",uid)
    data_dict = secu_data.dict()
    print('输入转成字典：',data_dict,type(data_dict))

    #记录日志
    logger.info(f"request_id:{uid}; 【start】进入逻辑")
    logger.info(f"request_id:{uid}; 【request body】{data_dict}")
    # data_out=SecureRespond(**{"request_id": 'cf57432e-809e-4353-adbd-9d5c0d733868',"code": "1100","message": "success",})
    if secu_data.input:
        print('数据不为空：',secu_data.input)

         # 检查数据类型是否为字符串
        if isinstance(secu_data.input, str):
            # 如果是字符串，将其转换为包含该字符串的列表
            secu_data.input = [secu_data.input]
        
        #Bert模型批量分类
        data_allbatch=[]
        batch_size=6 #对数据分批处理
        for key,bat_data in enumerate([secu_data.input[i:i + batch_size] for i in range(0, len(secu_data.input), batch_size)]):
            print('标记：',key*batch_size)
            print(f'第{key}个',bat_data)
            # bert模型对数据分类
            data_batch=SecuClassify(model,tokenizer,bat_data,key*batch_size)
            data_allbatch.extend(data_batch)

        #封装所有批数据
        print('所有批数据：',data_allbatch)
        data_outs={"request_id": uid,"code": "1100","message": "success","data":data_allbatch}
        print('模型处理后的数据：',data_outs)

    else:
        print('数据为空')
        # return '数据为空'
    
    # 校验数据
    try:
        data_outs=SecureRespond(**data_outs)  
        print('校验后数据：',data_outs)  
    except ValidationError as e:
        print('异常：',e)
        #记录日志
        logger.info(f"request_id:{uid}; 【error】数据校验异常; 【error messenger】{e}")
        logger.info(f"request_id:{uid}; 【data】{data_outs}")
        return {"request_id": uid,"code": "1903","message": "server_error","data":[]}

    return data_outs


#7、加载分类模型
from transformers import AutoTokenizer
from transformers import AutoModel
import uuid
import numpy

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path, trust_remote_code=True)

#8、bert模型对数据分类
def SecuClassify(model,tokenizer,batch_sentences,batch_idx):
   
    #双数组字典树（DAT），获取批量数据的敏感词标签
    found_words=contains_words(trie,batch_sentences)
    print('获取批量敏感词：',found_words)
    # for key,word in enumerate(found_words):
    #     if word:
    #         print(key,word)
    #         senten,lable=word[0]
    #         print('字典树查到的值：',senten,lable)
    
    #1、切割长文本，通过窗口滑动切割
    #切割单个文本
    def split_text(text, split_len, overlap_len):
            split_text = []
            window = split_len - overlap_len
            w = 0
            while w * window + split_len < len(text):
                text_piece = text[w * window: w * window + split_len]
                w += 1
                split_text.append(text_piece)
            # split_text.append(text[w * window:])
            split_text.append(text[-split_len:]) #最后一条长度也一样
            return split_text
    #切割多个文本，并标记分割文本所属的原文本
    def split_listtext(text_list,split_len, overlap_len):
        data={"sentences":[],"tags":[]} 
        idx=0
        for text in text_list:
            text_spilt=split_text(text, split_len, overlap_len)
            data["sentences"].extend(text_spilt)
            data["tags"].extend(list(zip([idx],[idx+len(text_spilt)])))
            idx +=len(text_spilt)
        return data

    #切分的长度和步长，split_len, overlap_len，窗口和步长
    texts =split_listtext(batch_sentences,8,3) #切分的长度和步长
    batch_sentences=texts["sentences"] #切分后句子
    every_texttag=texts["tags"]         #切分后句子所属标记
    print('分割后所属句子的标记：',every_texttag,len(every_texttag))
    print('每个句子切片:')
    for key,(pre,suf) in enumerate(every_texttag):
        print(f'第{key}个切片：',texts["sentences"][pre:suf])

    #2、batch数据处理，tokenizer
    encoded_input = tokenizer(batch_sentences, return_tensors="pt", padding=True,truncation=True)

    #3、模型对输入数据进行分类
    output = model(**encoded_input)

    #所有得分
    # logits=output.logits.tolist()
    # print('所有得分',logits)
    logits_all=output.logits.tolist()
    print('所有得分',numpy.shape(logits_all),len(logits_all),logits_all)

    # 使用clip函数限制矩阵元素的范围
    # clipped_matrix = np.clip(matrix, min_val, max_val)
    logits_all = numpy.clip(logits_all, 0, 1)

    #对分割后的得分进行合并
    print('分割后所属句子的标记：',every_texttag,len(every_texttag))
    print('所有得分切片:')
    logits=[]

    for key,(pre,suf) in enumerate(every_texttag):
        print(f'第{key}个切片：',logits_all[pre:suf])
        #取切片每列最大值
        print('取每列最大')
        print(numpy.max(logits_all[pre:suf], axis=0)) #取每列最小
        logits.append(numpy.max(logits_all[pre:suf], axis=0))

        print('取每列最大，在最大取下标：')
        print(numpy.max(logits_all[pre:suf], axis=0).argmax()) # argmin不加axix默认是全部
        

    print('对分割后的得分进行合并:',len(logits),logits)

    #argmax 获取最大得分的下标位置
    # class_ids=output.logits.argmax(dim=1).tolist()
    class_ids=numpy.argmax(logits, axis=1)
    print("每一行的最小值索引：",len(class_ids), class_ids)

    #所有标签，dict{0: 'politics', 1: 'porn', 2: 'ad', 3: 'violence', 4: 'ban', 5: 'abuse', 6: 'private'}
    labels=model.config.id2label
    print('所有标签:',labels,type(labels))

    #获取标签text
    print(type(labels))
    print('分类：',list(labels.values()))

    #最大概率标签
    label=[labels[i] for i in class_ids ]
    print('最大概率标签:',label)

    #对得分及关联的标签，由大到小排序
    allLabels_sort=[sorted(list(zip(a,b)), key = lambda x:x[0],reverse=True)  for a,b in list(zip(logits,[list(labels.values())]*len(logits))) ]
    print('多层zip排序：',allLabels_sort)

    #4、封装数据
    data=[]
    thred=0.3 #过滤阈值
    for index,(label,all_labels) in enumerate(list(zip(label,allLabels_sort))):
        #遍历的数据
        # print(f'第{index}条：')
        # print(index,label,all_labels)

        #字典数的结果,如果不为空,最终结果为字典树的
        if found_words[index]:
            senten,lable=found_words[index][0]
            print('字典树查到的值：',senten,lable)
            label=lable
            all_Labels=[ {"probability": 1,"label": lable}]
            print('all_Labels值：',all_Labels)
        else:
            print('阈值对象：',all_labels[0])
            score,_=all_labels[0]
            if score<thred : label='pass' 
            all_Labels=[ {"probability": i,"label": j} for i,j in all_labels if i>thred]
            print('all_Labels值：',all_Labels)

        data.append({"index": index+batch_idx,"label": label,"all_labels":all_Labels})

    print('初始化数据:',data)

    return data

 

# 9、双数组字典树（DAT），过滤敏感词
from pydatrie import DoubleArrayTrie
trie = DoubleArrayTrie.load(dat_path) #典树数据文件
print(trie.items()[-10:])
print('字典总长度：',len(trie))

# 检查句子中是否包含词
def contains_words(trie, batch_sentences):
    
    # 检查数据类型是否为字符串
    if isinstance(batch_sentences, str):
        # 如果是字符串，将其转换为包含该字符串的列表
        batch_sentences = [batch_sentences]
    result = []
    for sentence in batch_sentences:
        one_res=[]
        for i in range(len(sentence)):
            # prefix = sentence[i:]  #取i及其后面的
            prefix = sentence[i:i+10] #可以设置最长字符数，比如最长为6，i+6
            
            # found_words = trie.prefixes(prefix)  # 从前缀中找出所有在 trie 中的词（7w个数据，时间达到毫秒级别）
            found_words = trie.prefix_items(prefix)
            if found_words:
                    one_res.extend(found_words)
        result.append(one_res)
    return result


#启动服务
if __name__ == "__main__":
    #方法一：
    config = uvicorn.Config(app,host='0.0.0.0',port=port, reload=True, log_level="info") 
    server = uvicorn.Server(config)
    server.run()
    
    #方法二：
    # from pathlib import Path
    # uvicorn.run('getpost:app',host='0.0.0.0',port=8888, reload=True, log_level="info")
