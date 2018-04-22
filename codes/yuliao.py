#! /usr/bin/env python3.6
#coding=utf-8
import re
import os
from os import path
from collections import Counter
import codecs
import jieba
import json
import sys
sys.setrecursionlimit(1000000)
global dirlist,filelist,filename,i
dirlist = []
filelist = []
filename = []
def adapt_file(file):
  #用将标记内容录入一个序列中，然后再文本中找到相同模式的部分就删除
  f = open(file,'r',encoding='utf-8')
  f.read()
  for data in f:
      regex_1 = r'(<(.*)?/>)'
      regex_2 = r'[*,=].\S*'
      #regex_3 = r'[]'
      data = re.sub(regex_1,"",data)
      data = re.sub(regex_2,"",data)
      # data = re.sub(regex_3,"",data)
      return data
def strQ2B(file):
  rstring = ""
  f = open(file,'r',encoding='utf-8')
  for line in f:
      ustring = line.strip()
      for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 0x3000:#全角空格直接转换
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
            if not((inside_code >= 0x0041 and inside_code <= 0x5A) or (inside_code >= 0x0030 and inside_code <= 0x0039) or (inside_code >= 0x0061 and inside_code <= 0x7A)):
                rstring += uchar
                continue
            rstring += chr(inside_code)
      return rstring
def strB2Q(file):
    f = open(file,'r',encoding='utf-8')
    rstring = ""
    for line in f:
        ustring = line.strip()
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 0x0020: # 全角空格直接转换
                 inside_code = 0x3000
            else:
                if not ((inside_code >= 0x0021 and inside_code <= 0x2F) or (inside_code >= 0x3A and inside_code <= 0x0040) or (inside_code >= 0x5B and inside_code <= 0x0060) or (inside_code >= 0x7B and inside_code <= 0x7E)):
                     rstring += uchar
                     continue
                     inside_code += 0xfee0
                rstring += chr(inside_code)
    return rstring
def get_file(level,path):
  files = os.listdir(path) #列出当前目录下的所有文件夹
  for file in files:
    subfile = os.path.join(path, file)
    if os.path.isdir(subfile):
      dirlist.append(subfile)
      get_file(level+1,subfile)
      if( level == 1):
        filename.append(subfile)
      continue
    else:
      filelist.append(subfile)
  return filename
def calculate_words_frequency(path):
  STOPWORDS = [u'的', u'地', u'得', u'而', u'了', u'在', u'是', u'我', u'有', u'和', u'就', u'不', u'人', u'都', u'一', u'一个', u'上',
         u'也', u'很', u'到', u'说', u'要', u'去', u'你', u'会', u'着', u'没有', u'看', u'好', u'自己', u'这']
  PUNCTUATIONS = [u'。', u'，', u'“', u'”', u'…', u'？', u'！', u'、', u'；', u'（', u'）', u'?', u'：']
  f_in = open(path, 'r', encoding='utf-8')
  f_out = open('file_out.txt', 'a+')
  for line in f_in:
    seg_list = jieba.cut(line)
  for seg in seg_list:
    if seg not in STOPWORDS and seg not in PUNCTUATIONS:
      f_out.write(seg + "\n")
  f_in.close()
  f_out.close()
  file = open('file_out.txt', 'r')
  wordDict = {}
  content = file.read()
  wordlist = re.split('[\s\ \\,\;\.\!\n]+', content)
  for word in wordlist:
    if word in wordDict:
      wordDict[word] = wordDict[word] + 1
    else:
      wordDict[word] = 1
  count = Counter(wordDict)
  print(json.dumps(count.most_common()[1:], ensure_ascii=False))
def main():
  path = r'K:\NLC_test\爱情婚姻\2007\07\海杰1'
  level = 1
  count = 0
  dirs = get_file(level,path)
  for dir in dirs:
    for root,subdirs,files in os.walk(dir):
      for file in files:
        path2 = os.path.join(root,file)
        adapt_file(path2)
        strQ2B(path2)
        strB2Q(path2)
        count += 1
        calculate_words_frequency(path2)
        break
      print(count)
main()




