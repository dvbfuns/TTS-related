import pymongo
import re
import requests
import time
import os

mp3path = "./news_mp3_f/"
textpath = "./news_text_f/"

client = pymongo.MongoClient("mongodb://username:password@test.data.com:xxxxx/")
db = client['news']
col = db['news']

ret = col.find({"host":"19"}).limit(20000)
i = 1
for x in ret:
    
    #下载mp3文件  
    fullname = x['mediaurl']
    fullname = fullname.replace("res.kx.qinghuafm.com", "cloud-news.oss-cn-shanghai.aliyuncs.com")
    mp3name  = re.findall(r'[^\\/:*?"<>|\r\n]+$', fullname)

    print("file .", i)
    print("i: "+ str(i) + " " +"mp3: "+fullname)

    try:
        if not os.path.exists(mp3path):
            os.mkdir(mp3path)

        if not os.path.exists(mp3path + mp3name[0]): 
            r = requests.get(fullname,timeout=(3.05,27))
            if r.status_code == requests.codes.ok:
                with open(mp3path + mp3name[0], "wb") as f:
                    f.write(r.content)
            else:
                print("request error: "+r.status_code)
                i = i+1
                continue        
        else:
            #文件已经存在
            print("...pass")
            i = i+1
            continue

    except Exception as e:
        print("mp3 download error"+fullname+" "+str(e))
        i = i+1
        continue

    #创建文本文件（与mp3同名）
    text = x['title']+'，'+x['content']
    textname = mp3name[0].split('.')[0] + '.txt'
    if not os.path.exists(textpath + textname):
        with open(textpath + textname, "w") as f:
            f.write(text)
    i += 1


