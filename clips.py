

import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def make_wave_chunks(path, file_pre):
    song = AudioSegment.from_wav(path+file_pre+".wav")

    #split track where silence is 2 seconds or more and get chunks

    chunks = split_on_silence(song, 
        # must be silent for...
        min_silence_len=800,
        # consider it silent if quieter...
        silence_thresh=-30,
        # keep the successive begin and end of the initial audio...
        keep_silence=300,
    )

    #Process each chunk per requirements
    for i, chunk in enumerate(chunks):
        #Create 0.5 seconds silence chunk
        silence_chunk = AudioSegment.silent(duration=500)

        #Add  0.5 sec silence to beginning and end of audio chunk
        audio_chunk = silence_chunk + chunk + silence_chunk

        #Normalize each audio chunk
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        #Export audio chunk with new bitrate
        newfilename = "{}-{}.wav".format(file_pre, i+1)
        print("exporting {}".format(newfilename))
        newfiles.append(newfilename)
        normalized_chunk.export(path+newfilename, format="wav")

    return len(chunks)

def create_file(str, filename):
    file=open(filename,'a')
    file.write(str)
    file.close()

path = "./init/"
# whether the count of trunked wavs and texts are same.
path_match="./match/"
path_unmatch="./unmatch/"

nMatchSrc = 0
nMatchDst = 0
nUnmatchSrc = 0
nUnmatchDst = 0

newfiles = []

if not os.path.exists(path_match):
    os.makedirs(path_match)

if not os.path.exists(path_unmatch):
    os.makedirs(path_unmatch)

files = os.listdir(path)
for file in files:
    if not file.endswith(".wav"):
        continue

    file_pre = file.split(".")[0]

    newfiles = []

    print("begin to make wave and text chunks for " + file_pre + "...........................................")

    # make wav trunks
    nWav = make_wave_chunks(path, file_pre)

    # make text trunks
    nTxt = 0
    linecount = len(open(path+file_pre+".txt",'r').readlines()) 
    if linecount == 1:
        with open(path+file_pre+".txt", 'r') as f:
            line = f.readline()
            a = line.find("，")
            b = line.find("。")
            nAbstract = min(a, b)
            sAbstract = line[:nAbstract]
            sContent = line[nAbstract+1:]
            szContent = sContent.split("。")
            i = 1
            newfilename = "{}-{}.txt".format(file_pre, i)
            create_file(sAbstract, path+newfilename)
            newfiles.append(newfilename)
            for s in szContent:
                if len(s) <= 2: # ignore the end empty str when splitting
                    continue
                i = i + 1
                newfilename = "{}-{}.txt".format(file_pre, i)
                create_file(s, path+newfilename)
                newfiles.append(newfilename)
            nTxt = i

    # if trunks number is not same, warning, and move new files to unmatch folder. 
    # otherwise, move newfiles to match folder.
    if not nWav==nTxt:
        print("waring ******** mismatched {} wav and {} text chunks for file {}".format(nWav, nTxt, file_pre))
        nUnmatchSrc += 1
        nUnmatchDst += nWav
        for file in newfiles:
            shutil.move(path+file, path_unmatch+file)
    else:
        nMatchSrc += 1
        nMatchDst += nWav
        for file in newfiles:
            shutil.move(path+file, path_match+file)
        

print("Good: we get matched {} wav/txt from {} initial files".format(nMatchDst, nMatchSrc))
print("Waring: we get unmatched {} wav/txt from {} initial files".format(nUnmatchDst, nUnmatchSrc))



