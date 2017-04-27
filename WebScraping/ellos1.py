""".........This file extract all the product page links and fetch each product page data from the target webserver
 by transversing the entire client website................"""

import header as h
import ellos2

skuList=set()
idList=set()
gender={'/dam'}
category={'skonhet-halsa','accessoarer','traningstillbehor','set_3'}
analyticsReporting=None
curr=None

#Transverse the client entire website and extract all the product page links

def pageLinks(bsObj,url):
    try:
        links = []
        if ""==url:

            list = bsObj.find("div",{"class":"brandMenu"}).findAll("a",{"class":"submenuAsync anchor"})
            for ele in list:
                if ele['href'] in gender:
                    links.append(ele)

        elif h.re.compile("\/[a-z]*").fullmatch(url) != None:
            list = bsObj.find("ul",id="ProductDepartment").findAll("a",{"class":"async"})
            for ele in list:
                if ele['href'].split('/')[2] not in category:
                    links.append(ele)

        elif h.re.compile("\/[a-z]*\/[a-z-]*").fullmatch(url) != None:
            link = bsObj.find("a", {"class": "paginationLink"})
            if link is None:
                links = bsObj.find("ul", {"class": "productListWrapper"}).findAll("a", {"class": "productLink"})
            else:
                while (bsObj.find("a", {"class": "prevNextPage hide"}) == None):
                    print(link['href'])
                    bsObj = get_bsObj(link['href'])
                    pageLinks(bsObj, link['href'])
                    link = bsObj.findAll("a", {"class": "prevNextPage"})[1]
                return

        elif h.re.compile("\/[A-Za-z]*\/[A-Za-z0-9?=-]*").fullmatch(url)!= None:
            list = bsObj.find("ul", {"class": "productListWrapper"}).findAll("a", {"class": "productLink"})
            for ele in list:
                id=ele['href'].split('/')
                if len(id) >=4:
                    id=int(ele['href'].split('/')[3].split('?')[0])
                    if id not in idList:
                        idList.add(id)
                        links.append(ele)

        else:
            ellos2.productInfo(bsObj, url, skuList)
            return

    except AttributeError as e:
        print ("Error :\t",e)
        print("Correct the mistake and to resume hit [Enter]")

    for link in links:
        bsObj = get_bsObj(link['href'])
        pageLinks(bsObj,link['href'])

#Fetch the product page data from a target webserver and format it into beautifulsoup object

def get_bsObj(url):
    try:
        pageUrl = "http://www.ellos.se" + url
        html = h.urlopen(pageUrl)
        # server not found /url is mistyped
        bsObj = h.BeautifulSoup(html.read(), "html.parser")
    except h.HTTPError as e:
        print(e)
    return bsObj

#Get Google Analytic API credentials, call URL data and SKU data functions to fetch the data from the Google Analytic API

def main():
    analyticsReporting=h.apiData.get_credential()
    url=""
    bsObj=get_bsObj(url)
    pageLinks(bsObj,url)
    ellos2.urlData(analyticsReporting, idList)
    ellos2.skuData(analyticsReporting,skuList)
