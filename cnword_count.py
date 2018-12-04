# -*- encoding: utf-8 -*-
import os

_dict = {}
_dict_pinyin = {}

trn_path = "./news_text/"

def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4E00' and uchar <= u'\u9FA5':
            return True
        else:
            return False
 
def count_chinese_word(filepath):
    try:
        print(filepath)
        with open (filepath, 'rb') as txt_file:
            for line in txt_file:
                try:
                    ustr = line.decode('utf-8')
                except:
                    continue    
                for uchar in ustr:
                    if is_chinese(uchar):
                        if uchar in _dict:
                            _dict[uchar] = _dict[uchar] + 1
                        else:
                            _dict[uchar] = 1
    except IOError as ioerr:
        print("file not exist !")

def count_word(filepath):
    try:
        with open (filepath, 'r') as txt_file:
            ustr = txt_file.readline()
            for uchar in ustr:
                if is_chinese(uchar):
                    if uchar in _dict:
                        _dict[uchar] = _dict[uchar] + 1
                    else:
                        _dict[uchar] = 1
            pinyin_str = txt_file.readline()
            pinyin_arr = pinyin_str.split(' ')
            for p_word in pinyin_arr:
                if p_word in _dict_pinyin:
                    _dict_pinyin[p_word] = _dict_pinyin[p_word] + 1
                else:
                    _dict_pinyin[p_word] = 1
    except IOError as ioerr:
        print("file not exist !")
    

if __name__ == '__main__':
    #files = os.listdir(trn_path)
    #count = 0
    #for file in files:
        #if not file.split('.')[-1] == 'trn':
        #    continue
    #    count_chinese_word(trn_path + file)
    #    count += 1
    
    count = 1
    count_chinese_word("../录音文本_utf8.txt")

    print(sorted(_dict.items(), key=lambda d: d[1])) 
    print("总共 {} 汉字， {} 文件 ".format(len(_dict),count))
    #print(sorted(_dict_pinyin.items(), key=lambda d: d[1])) 
    #print("total {} pinyin， {} files ".format(len(_dict_pinyin),count))

    