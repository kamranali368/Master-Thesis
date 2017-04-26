from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import nelly2
import pymysql
import urllib.parse

idList=set()
category={'Festklänningar','Klänningar','Jackor & Kappor','Toppar','Tröjor','Blusar & Skjortor','Byxor & Shorts','Jeans','Kjolar','Jumpsuits','Badkläder','Underkläder','Skor','Sport'}

def pageLinks(bsObj,url):
    try:
        links=[]
        if re.compile("\/[a-z]+\/[a-zäö-]*\/").fullmatch(url) != None:
            list1 = bsObj.findAll('div', {'class': 'yamm-content'})
            for ele in list1:
                list2=ele.findAll('a')
                for link in list2:
                    if link.get_text() in category:
                        links.append(link)

        elif re.compile("\/[a-z]+\/[a-zäö-]*\/[a-zäö-]*\/*[a-zäö-]*\/*").fullmatch(url) != None:
            list=bsObj.find('div',{'class':'pagination-right'}).findAll('a')
            count=int(list[len(list)-2].get_text())
            for i in range(count):
                url1=url+'?page='+str(i+1)
                bsObj = get_bsObj(url1)
                print(url1)
                pageLinks(bsObj, url1)

            return

        elif re.compile("\/[a-z]+\/[a-zäö-]*\/[a-zäö-]*\/*[a-zäö-]*\/*[a-z?=0-9]*").fullmatch(url) != None:
            list=bsObj.find('ul',{'class':'js-product-list'}).findAll('a',{'data-name':True})
            for ele in list:
                id = int(ele['data-articlenr'])
                if id not in idList:
                    idList.add(id)
                    links.append(ele)


        else:
            subCat,id=nelly2.productInfo(bsObj,cur)
            links= bsObj.find("select", {"class": "select-color"}).findAll("option")
            for link in links:
                url = link['value']
                bsObj = get_bsObj(url)
                nelly2.colorInfo(bsObj,url,cur,id,subCat)
            return

    except AttributeError as e:
        print ("Error :\t",e)
        print("Correct the mistake and to resume hit [Enter]")
    #print(links)
    #print(len(links))
    for link in links:
        #print(link['href'])
        bsObj = get_bsObj(link['href'])
        #print('problem')
        pageLinks(bsObj,link['href'])

def get_bsObj(url):
    try:
        url = urllib.parse.urlsplit(url)
        url = list(url)
        url[2] = urllib.parse.quote(url[2])
        url = urllib.parse.urlunsplit(url)
        #print(type(url))
        if url.startswith('http://nelly.com') is False:
            pageUrl = "http://www.nelly.com" + url
            #print('Hi There')
        else:
            pageUrl=url
            #print('come stas')
        html = urlopen(pageUrl)
        # server not found /url is mistyped
        bsObj = BeautifulSoup(html.read(), "html.parser")
        # print(pageUrl)
    except HTTPError as e:
        print(e)
    return bsObj


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='iprospect', db='scraping', charset='utf8')
    cur = conn.cursor()
    url = "/se/kläder-för-kvinnor/"
    bsObj = get_bsObj(url)
    pageLinks(bsObj, url)
    cur.close()
    conn.close()
