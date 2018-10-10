from pypinyin import pinyin, lazy_pinyin, Style
import os

import warnings
from decimal import Decimal


path = "/Users/mayanke/Documents/test_pinyin/"


def number_trans(value, capital=True, prefix=False, classical=None):
    if not isinstance(value, (Decimal, str, int)):
        msg = '''
        由于浮点数精度问题，请考虑使用字符串，或者 decimal.Decimal 类。
        因使用浮点数造成误差而带来的可能风险和损失作者概不负责。
        '''
        warnings.warn(msg, UserWarning)
    # 默认大写金额用圆，一般汉字金额用元
    if classical is None:
        classical = True if capital else False
        
    # 汉字金额前缀
    if prefix is True:
        prefix = '人民币'
    else:
        prefix = ''
        
    # 汉字金额字符定义
    dunit = ('角', '分')
    if  1: 
        num = ('ling1 ', 'yi1 ', 'er4 ', 'san1 ', 'si4 ', 'wu3 ', 'liu4 ', 'qi1 ', 'ba1 ', 'jiu3 ')
        iunit = [None, 'shi2 ', 'bai3 ', 'qian1 ', 'wan4 ', 'shi2 ', 'bai3 ', 'qian1 ','yi4 ', 'shi2 ', 'bai3 ', 'qian1 ', 'wan4 ', 'shi2 ', 'bai3 ', 'qian1 ']
    #if classical:
        iunit[0] = ' ' if classical else ' '
    # 转换为Decimal，并截断多余小数

    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))

    # 处理负数
    if value < 0:
        prefix += 'fu4'          # 输出前缀，加负
        value = - value         # 取正数部分，无须过多考虑正负数舍入
                                # assert - value + value == 0
    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError('金额太大了，不知道该怎么表达。')
    istr, dstr = s.split('.')           # 小数部分和整数部分分别处理
    istr = istr[::-1]                   # 翻转整数部分字符串
    so = []     # 用于记录转换结果
    
    # 零
    if value == 0:
        return prefix + num[0] + iunit[0]
    haszero = False     # 用于标记零的使用
    if dstr == '00':
        haszero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”
        
    # 处理小数部分
    # 分
    if dstr[1] != '0':
        so.append(dunit[1])
        so.append(num[int(dstr[1])])
    else:
        so.append('')         # 无分，则加“整”
    # 角
    if dstr[0] != '0':
        so.append(dunit[0])
        so.append(num[int(dstr[0])])
    elif dstr[1] != '0':
        so.append(num[0])       # 无角有分，添加“零”
        haszero = True          # 标记加过零了
        
    # 无整数部分
    if istr == '0':
        if haszero:             # 既然无整数部分，那么去掉角位置上的零
            so.pop()
        so.append(prefix)       # 加前缀
        so.reverse()            # 翻转
        return ''.join(so)

    # 处理整数部分
    for i, n in enumerate(istr):
        n = int(n)
        if i % 4 == 0:          # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and so[-1] == iunit[4]:   # 亿和万之间全部为零的情况
                so.pop()                        # 去掉万
            so.append(iunit[i])
            if n == 0:                          # 处理这些位上为零的情况
                if not haszero:                 # 如果以前没有加过零
                    so.insert(-1, num[0])       # 则在单位后面加零
                    haszero = True              # 标记加过零了
            else:                               # 处理不为零的情况
                so.append(num[n])
                haszero = False                 # 重新开始标记加零的情况
        else:                                   # 在其他位置上
            if n != 0:                          # 不为零的情况
                so.append(iunit[i])
                so.append(num[n])
                haszero = False                 # 重新开始标记加零的情况
            else:                               # 处理为零的情况
                if not haszero:                 # 如果以前没有加过零
                    so.append(num[0])
                    haszero = True

    # 最终结果
    so.reverse()

    # process 18 case:  yi shi ba --> should be "shi ba"
    if len(so) > 1 and so[0] == 'yi1 ' and so[1] == 'shi2 ':
        so = so[1:]

    return ''.join(so[:-2])



nian_lookup={'0':'ling2','1':'yi1','2':'er4','3':'san1','4':'si4','5':'wu3','6':'liu4','7':'qi1','8':'ba1','9':'jiu3'}


def expandnumber(number):
    number_str = ''

    return number_string


files = os.listdir(path)
count = 1

illegal_files = []

for file in files:
    print("process file: " + file + " index: " + str(count))

    if not file.split('.')[-1] == 'trn':
        print("---- bypass only process trn file")
        continue
    linecount = len(open(path+file,'r').readlines()) 
    if not linecount == 2:
        print("--- illegal file")
        illegal_files.append(file)
        continue

    content = []
    with open(path+file, 'r') as f:
        content = f.readlines()
        print(content)
        line = content[1]

#    print(line)
    newline = [] 
    for char in line:
        if ord(char) > 128:
            continue
        else:
            newline.append(char)
    line =''.join(newline)

    newline = line.split(' ')

    index = 0
    line = ''
    while index < len(newline):
        # % percentage
        if len(newline[index]) > 1 and newline[index][-1] == '%':
            print("---percentage--- ")
            print(newline[index])
            line += "bai3 fen1 zhi1 "
            newline[index] = newline[index][:-1]

        if newline[index].isdigit():
            #next is nian2
            if newline[index+1] == "nian2" and len(newline[index]) == 4 :
                print("---nian----  ",newline[index])
                #simply expand
                expand = []
                for i in newline[index]:
                    expand.append(nian_lookup[i])
                    expand.append(' ')
                expand = ''.join(expand)
                line += expand                    
            elif index > 1 and newline[index-1] == 'yue4' and newline[index+1] == 'ri4':
                # ri -> hao
                expand = number_trans(int(newline[index]))
                line += expand + 'hao4 '
                #bypass 'ri4'
                index += 1   
            elif newline[index+1] == 'shi2' and newline[index+3] == 'fen1':
                # shi2 -> dian3
                expand = number_trans(int(newline[index]))
                line += expand + 'dian3 '
                #bypass 'shi2'
                index += 1    
            else:
                print("---number--- ",newline[index])
                #expand number
                expand = number_trans(int(newline[index]))
                line += expand   
            index += 1
            continue
            
        # . dot            
        m = newline[index].split('.')
        if len(m) < 2 :
            line += newline[index] + ' '
        else:
            print("---dot--- ",m)
            #expand number before dot
            expand = number_trans(int(m[0]))
            line += expand
            #plus dot 
            line += 'dian3 '
            #expand number after dot
            expand = []
            for i in m[1]:
                expand.append(nian_lookup[i])
                expand.append(' ')
            expand = ''.join(expand)
            line += expand
        
        index += 1

    print(line)

    with open(path+file, 'w') as f:
        content[1] = line
        f.writelines(content)
    
    count += 1

print(illegal_files)
    

