import requests
from lxml import etree
import json
import time

def wash(node):
    res = ''
    for term in node:
        # 技巧1：使用node()方法获取其子标签，如我们这里是text()文本和span标签，
        #       那么使用"./node()[self::text() or self::span]"即可获取；
        #       如果是i标签就self::i，其他标签就不赘述了。

        if str(term)[0] != '<':
            res += term
    res = res.strip()  # 只去掉首尾的空字符
    return res  # 返回拼好的文字
def getmore(url,name):
    response = requests.get(url)
    txt = response.text
    html = etree.HTML(txt)
    Name = html.xpath('//*[@id="poiName"]/text()')
    Phone = html.xpath('//*[@id="strPhone"]/@name')
    L1 = html.xpath('/html/body/div[1]/div/div[1]/div[1]/div[2]/div/ul/li[2]/a[1]/text()')
    L2 = html.xpath('/html/body/div[1]/div/div[1]/div[1]/div[2]/div/ul/li[2]/a[2]/text()')
    L3 = html.xpath('/html/body/div[1]/div/div[1]/div[1]/div[2]/div/ul/li[2]/text()')
    L1 = wash(L1)
    L2 = wash(L2)
    L3 = wash(L3)
    Location = L1+L2+L3
    Name = wash(Name)
    Phone = wash(Phone)
    with open('./' + name + 'more.json', 'a', encoding='utf-8') as fp:
        json.dump({"名称": Name, "地址": Location, "联系电话": Phone}, fp, ensure_ascii=False)
        fp.write('\n')
def geturl(url, name):
    url = url[:len(url) - 1] + "_1/"
    t = 1
    while True:
        response = requests.get(url)
        txt = response.text
        html = etree.HTML(txt)
        purl = html.xpath('//div[@class="sortC"]/dl/dd/a/@href')
        cnt = 0
        for murl in purl:
            getmore(murl, name)
            cnt = cnt + 1
            if cnt > 200:
                break
        if cnt > 200:
            break
        t = t + 1
        url = url[:len(url) - 2] + str(t) + "/"
        time.sleep(0.5)
        if requests.get(url).status_code == 404:
            break
"""
def getlist(name):
    with open(name+'.json', 'r', encoding='utf-8') as pf:
        linklist = pf.read()
        for i in linklist:
            i = i.strip('\n')
        return linklist
"""
url = ['https://poi.mapbar.com/chongqing/130/', 'https://poi.mapbar.com/chongqing/520/',
       'https://poi.mapbar.com/chongqing/5I0/', 'https://poi.mapbar.com/chongqing/H83/']
name = ['快餐店', '超市', '便利店', '仓储物流企业']
geturl(url[3], name[3])
print("success!")