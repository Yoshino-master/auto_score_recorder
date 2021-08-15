'''
@author: jinglingzhiyu
'''
import pickle, re, time
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup


fpath = r'E:\workspace\zhanguo_auto_recoder\data\202108.pkl'
with open(fpath, 'rb') as f:
    data = pickle.load(f)
print(data)
# print(dir(data))
# data.encoding = data.apparent_encoding
# cont = data.content.decode('utf-8')
# soup = BeautifulSoup(cont, 'html.parser')
# print(soup.prettify())

# ptx = re.compile(r'<tbody class="ant-table-tbody">.*?</tbody>')
# match = ptx.findall(cont)
# soup = BeautifulSoup(match[1], 'html.parser')
# print(soup.prettify())

