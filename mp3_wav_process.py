import os

def checkmp3(filename):
    print("checkmp3 ",filename)
    extension = filename[-3:]
    print("extension: ",extension)
    if extension == 'wav':
        print("wav file")
        return False
    else:
        print("mp3 file")
        return True
 

def main (path):
    files = os.listdir(path)
    for filename in files:
        print(filename)
        if checkmp3(filename):
            print("start command")
            wavname = filename.split('.')[0] + ".wav"
            filename = path + filename
            wavname  = path + wavname
            command = "ffmpeg -i "+filename+" -acodec pcm_s16le -ac 1 -ar 22050  "+wavname 
            print(command)
            os.popen(command)
        else:
            continue
 
 
if __name__ == '__main__':
    try:
        main("./news_mp3/")
    except:
        pass
