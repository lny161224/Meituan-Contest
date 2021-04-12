#总的爬具体信息的py
import os
import requests
from lxml import etree
import json
import time
#读取各大板块
def getdata(url,m):
    url = url[:len(url)-1]+"_1/"
    t=1
    while True:
        response = requests.get(url)
        txt = response.text
        html = etree.HTML(txt)
        result1 = html.xpath('//div[@class="sortC"]/dl/dd/a/text()')
        result2 = html.xpath('//div[@class="sortC"]/dl/dd/a/@href')
        t=t+1
        with open('./标准化.json', 'a', encoding='utf-8') as fp:
            json.dump({'板块名称': list5[i + 10*m], '具体分类': nameresult[j], '链接地址': urlresult[j], '名称': result1, '相关链接': result2},
                      fp,ensure_ascii=False)
            fp.write('\n')
        # with open('其他企业.json','a',encoding='utf-8') as fp:
        #     json.dump({'名称': result1, '相关链接': result2},fp,ensure_ascii=False,indent=2)
        #     # fp.write('\n')
        url = url[:len(url)-2]+str(t)+"/"
        time.sleep(0.5)
        if requests.get(url).status_code==404:
            break
list5 = []
with open('各大板块.txt','r',encoding='utf-8') as pf:
    list4=pf.readlines()
    for i in list4:
        i=i.strip('\n')
        list5.append(i)
url = "https://poi.mapbar.com/beijing/"
response = requests.get(url)
txt = response.text
html = etree.HTML(txt)
for i in range(0,10):
    urlresult = html.xpath('/html/body/div[2]/div[3]/div['+str(i+1)+']/a/@href')
    nameresult = html.xpath('/html/body/div[2]/div[3]/div['+str(i+1)+']/a/text()')
    for j in range(0,len(urlresult)):
        getdata(urlresult[j],0)
for i in range(0,8):
    urlresult = html.xpath('/html/body/div[2]/div[4]/div[' + str(i + 1) + ']/a/@href')
    nameresult = html.xpath('/html/body/div[2]/div[4]/div[' + str(i + 1) + ']/a/text()')
    for j in range(0, len(urlresult)):
        getdata(urlresult[j],1)
os.system("pause")
