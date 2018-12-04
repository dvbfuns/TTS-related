import urllib3
from urllib.parse import urlencode
import json
import os
import time

http = urllib3.PoolManager()

headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

url = "http://localhost:8000/synthesize"

wd = urlencode({'text': "费利佩六世表示"})

fullurl = url + '?' + wd
response = http.request(method = 'GET',url=fullurl,headers=headers)
print("response status: {}".format(response.status))

# 获取响应头信息,返回字符串
print(response.info())

out_wav_file = "./测试结果/"+time.strftime("%Y%m%d%H%M%S.wav", time.localtime())
with open(out_wav_file,"wb") as f:
    f.write(response.data)