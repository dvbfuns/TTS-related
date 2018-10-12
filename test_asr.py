import requests
import urllib
import hashlib
import json
import subprocess
import time
import wave
import os
import random
import base64
import threading
import difflib
from contextlib import contextmanager
from ctypes import *
from pypinyin import pinyin, lazy_pinyin, Style

mapp_id = 'xxxxx'
mapp_key= 'xxxxxxxxxx'

def md5(string):
    md = hashlib.md5()
    md.update(string.encode('utf-8'))
    md5 = md.hexdigest().upper()
    return md5


def urlencode(args):
    tuples = [(k, args[k]) for k in sorted(args.keys()) if args[k]]
    query_str = urllib.parse.urlencode(tuples)
    return query_str


def signify(args, app_key):
    query_str = urlencode(args)
    query_str = query_str + '&app_key=' + app_key
    signiture = md5(query_str)
    return signiture


def http_post(api_url, args):
    try: 
        resp = requests.post(url=api_url, data=args,timeout=(3.05,27))
        print("http code: ",resp.status_code)
        resp = json.loads(resp.text)
        print(resp)
    except Exception as e:
        print("http request error" + str(e))
        resp = {'data':{'text':' '}} 
    return resp

class BaseASR(object):

    ext2idx = {'pcm': '1', 'wav': '2', 'amr': '3', 'slk': '4'}

    def __init__(self, api_url, app_id, app_key):
        self.api_url = api_url
        self.app_id = app_id
        self.app_key = app_key

    def stt(self, audio_file, ext='wav', rate=16000):
        raise Exception("Not Implemented!")

class BasicASR(BaseASR):
    """ Online ASR from Tencent
    https://ai.qq.com/doc/aaiasr.shtml
    """
    def __init__(self, api_url='https://api.ai.qq.com/fcgi-bin/aai/aai_asr',
                 app_id=mapp_id, app_key=mapp_key):
        super(BasicASR, self).__init__(api_url, app_id, app_key)

    def stt(self, audio_file, ext='wav', rate=16000):
        if ext == 'wav':
            wf = wave.open(audio_file)
            nf = wf.getnframes()
            audio_data = wf.readframes(nf)
            wf.close()
        else:
            raise Exception("Unsupport audio file format!")

        args = {
            'app_id': self.app_id,
            'time_stamp': str(int(time.time())),
            'nonce_str': '%.x' % random.randint(1048576, 104857600),
            'format': self.ext2idx[ext],
            'rate': str(rate),
            'speech': base64.b64encode(audio_data),
        }

        signiture = signify(args, self.app_key)
        args['sign'] = signiture
        resp = http_post(self.api_url, args)

        #text = resp['data']['text'].encode('utf-8')
        text = resp['data']['text']
        return text


unmatch_files = []

def test_stream_asr():
    audio_path = "./newclips1_trn/"
    tmp_path = "./newclips1_trn/tmp/"
    #audio_path = "./py_test/"
    #tmp_path   = "./py_test/tmp/"

    audio_files = os.listdir(audio_path)
    
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    asr_engine = BasicASR()

    count = 0
    index = 0
    for audio_file in audio_files:
        if not audio_file.split('.')[-1] == 'wav':
            continue
        index += 1        
        print("\nprocess wav file {}: {} ".format(index, audio_file))

        wavname = tmp_path + audio_file
        filename= audio_path + audio_file
        if not os.path.exists(wavname):
            command = "ffmpeg -i "+filename+" -acodec pcm_s16le -ac 1 -ar 16000  "+wavname 
            print(command)
            os.popen(command)
       
        time.sleep(1)

        print("start asr ...")
        text = asr_engine.stt(wavname)
        txt_file = audio_file.split('.')[0]+'.wav.trn'
        with open(audio_path + txt_file) as f:
            line_c = f.readline()
            line = f.readline()
        print(line_c)
        pinyin_str=""
        pinyin_text = pinyin(text,style=Style.TONE3)
        for word in pinyin_text:
            pinyin_str += word[0]+" "
        
        print(pinyin_str)
        print(line)
        ratio = difflib.SequenceMatcher(None,line,pinyin_str).ratio()
        print("ratio is: ",ratio)
        if ratio < 0.9:
            print("invalid file: {}, count: {} ",audio_file,count)
            count += 1
            os.remove(audio_path+audio_file)
            os.remove(audio_path+txt_file)
            print("delete ...")
            unmatch_files.append(audio_file+'|'+line_c+'|'+text)
    print("\n")

    print(unmatch_files)
   
    with open("unmatched_list.txt","w") as f:
        for file in unmatch_files:
            f.writelines(file)
            f.write("\n") 

test_stream_asr()
