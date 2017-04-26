#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#from urllib.error import HTTPError
#import re
import boozt2
import pymysql
import header as h

idList=set()
category={'Kvinnor'}
subCategory={'Klänningar','Ytterkläder','Överdelar','Nederdelar','Lingerie','Skor'}

def productLinks(bsObj):
    list = bsObj.find('ul', {'id': 'product-list-cont'}).findAll('li')
    for ele in list:
        link = ele.find('a', {'class': 'item-link'})
        id=int(link['href'].split('/')[5].split('?')[0])
        if id not in idList:
            idList.add(id)
            colorList = ele.find('div', {'class': 'item-thumbs'}).findAll('a')
            try:
                bsObj = get_bsObj(link['href'])
            except:
                print('link not found')
            boozt2.productInfo(bsObj, link['href'], colorList)

def pageLinks(bsObj,url):
    try:

        links = []
        if url== '/se/sv':
           list=bsObj.find('ul',{'class':'main-menu'}).findAll('a')
           for ele in list:
               if ele.get_text().replace(' ','').replace('\n','').replace('\r','') in category:
                   links.append(ele['href'])


        elif h.re.compile("\/[a-z]*\/[a-z]*\/[a-z-]*").fullmatch(url) != None:
            list=bsObj.find('div',{'class':'content'}).findAll('a')
            for ele in list:
                if ele.get_text().replace(' ','').replace('\n','').replace('\r','') in subCategory:
                    links.append(ele['href'])
            links.append('/se/sv/klader-for-kvinnor/badklaeder')

        elif h.re.compile("\/[a-z]*\/[a-z]*\/[a-z-]*\/[a-z]*\/*[a-z_]*").fullmatch(url) != None:
            link=bsObj.find('a',{'class':'pagination-previous'})
            if link is None:
                productLinks(bsObj)
            else:
                while(bsObj.find('a',{'class':'ignore-hidden-toggle pagination-next disabled'})==None):
                    print(link['href'])
                    bsObj=get_bsObj(link['href'])
                    productLinks(bsObj)
                    link = bsObj.find('a', {'class': 'pagination-next'})
            return

    except AttributeError as e:
        print ("Error :\t",e)
        input('problem')

    for link in links:
        bsObj = get_bsObj(link)
        pageLinks(bsObj,link)

def get_bsObj(url):
    try:
        pageUrl = "http://www.boozt.com" + url
        html = h.urlopen(pageUrl)
        # server not found /url is mistyped
        bsObj = h.BeautifulSoup(html.read(), "html.parser")
    except h.HTTPError as e:
        print(e)
    return bsObj


def main():#if __name__ == '__main__':
    #conn = pymysql.connect(host='127.0.0.1', user='root', passwd='iprospect', db='scraping', charset='utf8')
    #cur = conn.cursor()
    url = "/se/sv"
    bsObj = get_bsObj(url)
    pageLinks(bsObj, url)
    #cur.close()
    #conn.close()
