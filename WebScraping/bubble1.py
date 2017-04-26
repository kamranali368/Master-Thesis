#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#from urllib.error import HTTPError
#import re
import bubble2
import pymysql
#import urllib.parse
import header as h
idList=set()

category={'Kläder','Skor'}

def pageLinks(bsObj,url):
    try:
        links = []
        if h.re.compile("\/[a-z]+\/[a-z]+").fullmatch(url) != None:
            list=bsObj.find('div',{'class':'headerContentHolder'}).findAll('a')
            for ele in list:
                if ele.get_text() in category:
                    links.append(ele)


        elif h.re.compile("\/[a-z]+\/[a-zä]*\/[a-z]+").fullmatch(url) != None:
            links=bsObj.find('div',{'class':'divStaticPaging'}).findAll('a')
            links=links[0:len(links)-1]


        elif h.re.compile("\/[a-z]+\/[a-zA-Z%0-9]*\/[a-zA-Z?=0-9]*").fullmatch(url) != None:
            links=bsObj.find('ul',{'class':'ulProdList'}).findAll('a',{'href':True})

        else:
            id=int(bsObj.find('span',{'itemprop':'identifier'}).get_text().split('-')[0])
            if id not in idList and url.find('beauty')==-1 and url.find('accessoarer')==-1 and url.find('bkr-water-bottle')==-1:
                idList.add(id)
                cat=bubble2.productInfo(bsObj,url,id)
                if bsObj.find("div", {"class": "jsCustomDropDownContent"}) ==None:
                    bubble2.colorInfo(bsObj, url, id, cat)
                else:
                    links= bsObj.find("div", {"class": "jsCustomDropDownContent"}).findAll("a")
                    for link in links:
                        url = link['href']
                        bsObj = get_bsObj(url)
                        bubble2.colorInfo(bsObj,url,id,cat)
            return

    except AttributeError as e:
        print ("Error :\t",e)

    for link in links:
        bsObj = get_bsObj(link['href'])
        pageLinks(bsObj,link['href'])

def get_bsObj(url):
    try:
        if url.find('%') == -1:
            url = h.urllib.parse.urlsplit(url)
            url = list(url)
            url[2] = h.urllib.parse.quote(url[2])
            url = h.urllib.parse.urlunsplit(url)
        else:
            print(url)
        pageUrl = "http://www.bubbleroom.se" + url
        html = h.urlopen(pageUrl)
        # server not found /url is mistyped
        bsObj = h.BeautifulSoup(html.read(), "html.parser")
        # #print(pageUrl)
    except h.HTTPError as e:
        print(e)
    return bsObj


def main():
    #conn = pymysql.connect(host='127.0.0.1', user='root', passwd='iprospect', db='scraping', charset='utf8')
    #cur = conn.cursor()
    url = "/sv/kvinna"
    bsObj = get_bsObj(url)
    pageLinks(bsObj, url)
    #cur.close()
    #conn.close()
