'''
@author: jinglingzhiyu
'''

import pickle, re, time, os
# import matplotlib.pyplot as plt
import requests
# from bs4 import BeautifulSoup

def def_params(module_):
    module_.params = type('test', (object,), {})()      #创建一个空对象
    module_.params.rooturl = r'http://senka.su'
    module_.params.dataroot = r'E:/workspace/zhanguo_auto_recoder/data'
    module_.params.columes = ['第一位', '联合线', '一群线', '二群线', '三群线']
    module_.params.hd = {'user-agent' : 'Chrome/10'}

class record_cls():
    def __init__(self, autorenew=True):
        def_params(self)
        self.t = time.localtime(time.time())
        dataname = str(self.t.tm_year) + '0'*(2-len(str(self.t.tm_mon))) + str(self.t.tm_mon)
        self.filepath = os.path.join(self.params.dataroot, dataname) + '.pkl'
        if os.path.exists(self.params.dataroot) is False:
            os.makedirs(self.params.dataroot)
        if os.path.exists(self.filepath) is True:
            with open(self.filepath, 'rb') as f:
                self.valdict = pickle.load(f)
        else:
            self.valdict = {'worlds':[], 'date':[]}
        if autorenew is True:
            self.renew()
            self.savedata()
    def renew(self):
        if len(self.valdict.keys()) > 2 and self.valdict['date'][-1][-2:] == '02' : return    #如果一天内已经完成了两次有效记录,就不再记录
        self.get_url()
        cur_vals = self.ext_data(self.cur_cont)
        worlds, firstplace, unionplace, oneplace, secondplace, thirdplace = cur_vals
        for i, world in enumerate(worlds):
            if self.valdict.get(world) is None:
                self.valdict[world] = {'firstplace':[], 'unionplace':[], 'oneplace':[], 'secondplace':[], 'thirdplace':[]}
                self.valdict['worlds'].append(world)
            if len(self.valdict[world]['thirdplace']) > 0 and self.valdict[world]['thirdplace'][-1] == thirdplace[i]:
                #如果三群线不动,说明存在重复记录
                return
            self.valdict[world]['firstplace'].append(firstplace[i])
            self.valdict[world]['unionplace'].append(unionplace[i])
            self.valdict[world]['oneplace'].append(oneplace[i])
            self.valdict[world]['secondplace'].append(secondplace[i])
            self.valdict[world]['thirdplace'].append(thirdplace[i])
        date = str(self.t.tm_mday)
        date = '0'*(2-len(date)) + date
        if len(self.valdict['date']) > 0 and self.valdict['date'][-1] == date + '01':
            date = date + '02'
        else : date = date + '01'
        self.valdict['date'].append(date)
    def savedata(self, target=None):
        if target is None : target = self.filepath
        print(self.valdict)
        with open(target, 'wb') as f:
            pickle.dump(self.valdict, f)
    def renew_time(self):
        self.t = time.localtime(time.time())
    def ext_data(self, content):
        comp1 = r'<tbody class="ant-table-tbody">.*?</tbody>'
        ptx = re.compile(comp1)
        content_table = ptx.findall(content)[1]
        worlds, firstplace, unionplace, oneplace, secondplace, thirdplace = [], [], [], [], [], []
        comp_worlds = r'<div class="cell text-success">.*?</div>'
        ptx_worlds = re.compile(comp_worlds)
        worlds_ = ptx_worlds.findall(content_table)
        for val in worlds_:
            val = val.replace(r'<div class="cell text-success">', '')
            comp_val = val + r'</td><td class="ant-table-cell" style="text-align:center">.*?</tr>'
            ptx_vals_ = re.compile(comp_val)
            vals_ = ptx_vals_.findall(content)[0]
            ptx_vals = re.compile('\d+')
            vals = ptx_vals.findall(vals_)
            firstplace.append(int(vals[0]))       #第一位
            unionplace.append(int(vals[1]))       #联合线
            oneplace.append(int(vals[2]))         #一群
            secondplace.append(int(vals[3]))      #二群
            thirdplace.append(int(vals[4]))       #三群
            val = val.replace(r'</div>', '')
            worlds.append(val)                    #镇守府名称
        return worlds, firstplace, unionplace, oneplace, secondplace, thirdplace
    def get_url(self):
        r = requests.request('POST', self.params.rooturl, headers=self.params.hd, timeout=50)
        r.encoding = r.apparent_encoding
        self.cur_html = r
        self.cur_cont = r.content.decode('utf-8')
        self.data = self.ext_data(self.cur_cont)
    def get_filedata(self, datapath):
        with open(datapath, 'rb') as f:
            self.cur_cont = pickle.load(f)
        self.cur_cont.encoding = self.cur_cont.apparent_encoding
        self.cur_cont = self.cur_cont.content.decode('utf-8')
    def self_check(self):
        fpath = r'tmpdata.pkl'
        self.get_filedata(fpath)
        res = self.ext_data(self.cur_cont)
#         soup = BeautifulSoup(res, 'html.parser')
#         print(soup.prettify())
        

if __name__ == '__main__':
    m = record_cls()
#     m.self_check()
    
#     url = m.params.rooturl
#     hd = {'user-agent' : 'Chrome/10'}
#     r  = requests.request('POST', url, headers=hd, timeout=50)
#     r.encoding = r.apparent_encoding
#     content = r.content.decode('utf-8')
#     with open(r'tmpdata.pkl', 'wb') as f:
#         pickle.dump(r, f)
    
    
    
    
