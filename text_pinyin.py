from pypinyin import pinyin, lazy_pinyin, Style
import os

path = "/Users/mayanke/Documents/news_text/"


files = os.listdir(path)
count = 1
for file in files:
    with open(path+file, 'r') as f:
        line = f.readline()

    pinyin_str = "\n"
    with open(path+file,'a') as f:
        newline = pinyin(line,style=Style.TONE3)
        for word in newline:
            pinyin_str += word[0]+" "       
        f.write(pinyin_str)
    
    filenew = file.split('.')[0]+".wav.trn"
    os.rename(path+file,path+filenew)
    print("file "+file+" "+str(count)+"done")
    count += 1
    

