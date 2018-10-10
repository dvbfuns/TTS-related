import os

a = []
b = []
c = []
d = []

a = os.listdir("./news_mp3_f/")
b = os.listdir("./news_text_f_pinyin")

print(len(a))
print(len(b))

count = 0
for file in a:
    textfile = file.split('.')[0]
    c.append(textfile)    

for file in b:
    if file.split('.')[0] in c:
        continue
    else:
        d.append(file)
       

print(d)
print(len(d))