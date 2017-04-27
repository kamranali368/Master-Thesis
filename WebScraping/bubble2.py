"""...........This file scrape all the product information from the Competitor1 website and store all the data in a database.............."""

import header as h

#list of categories for whom data will be scraped from the competitor1 website........"""

tCategory={'Klänningar','Jackor & Kappor','Toppar & T-shirts','Tröjor','Blusar & Skjortor','Kavajer','T-shirts','Jackor','Linnen','Badkläder'}
bCategory={'Jeans','Leggings','Shorts','Kjolar','Byxor','Jumpsuits','Tights','Underkläder & Sovplagg','Strumpor och tights','Myskläder'}

#Mapping of a retailer size measure scale into international scale size........"""

wTops={'32':'X','34':'X','36':'S','38':'M','40':'L','42':'X','44':'X','46':'X','48':'X','50':'X','52':'X'}
intSize={'XXS','XS','S','M','L','XL','2XL','3XL','4XL','5XL','6XL'}
wintSize={'XXS':'X','XS':'X','S':'S','M':'M','L':'L','XL':'X','2XL':'X','3XL':'X','4XL':'X','5XL':'X','6XL':'X'}
wBottom={'22':'X','23':'X','24':'X','25':'X','26':'S','27':'S','28':'M','29':'M','30':'L','31':'L','32':'X','33':'X','34':'X','35':'X','36':'X','37':'X'}
wShoes={'36':'S','37':'S','38':'M','39':'M','40':'L','41':'L','42':'XL','43':'XL'}

#Scraping the product data from the competitor1 website and stroing the data in a database


def productInfo(bsObj,url,id):
    segment=url.split('/')
    gender=segment[3]
    brand=segment[4].replace('-',' ')
    str=bsObj.find('div',{'id':'breadCrumbData'}).get_text()
    bs4=h.BeautifulSoup(str,"html.parser")
    list=bs4.findAll('a')
    category=list[0].get_text()
    subCategory=list[1].get_text()
    name=list[2].get_text()

    if category in tCategory or subCategory in tCategory:
        subCategory=category
        category='Top'
    elif category in bCategory or subCategory in bCategory:
        subCategory=category
        category='Bottom'



    h.cur.execute("INSERT INTO bub_productinfo (id,brand,name,gender,category,subcategory,date) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",(id,brand,name,gender, category, subCategory, h.tDate))
    h.cur.connection.commit()
    return category

#Scraping the product color data from the competitor1 website and stroing the data in a database

def colorInfo(bsObj,url,id,category):
    try:
        """!!!...Color Information....!!!!"""
        list=bsObj.find('ul',{'class':'ulProdInfo'}).findAll('span')
        colorId=list[1].get_text()
        if len(list) > 3:
            color=list[3].get_text()
        else:
            color='NULL'


        if bsObj.find('div', {'class': 'divProdPriceSale'}) == None:
            originalPrice = bsObj.find('meta', itemprop='price')['content'].replace(' kr', '')
            originalPrice=float(''.join(i for i in originalPrice if ord(i)<128))
            discountPrice = 0.0
            discountPercentage = 0
        else:
            discountPrice = bsObj.find('meta', itemprop='price')['content'].replace(' kr', '')
            discountPrice=float(''.join(i for i in discountPrice if ord(i)<128))
            price = bsObj.find('div', {'class': 'divProdPriceInfo'})
            originalPrice = price.find('span', {'class': 'spanOrdPrice'}).get_text().replace(' kr', '')
            originalPrice = float(''.join(i for i in originalPrice if ord(i) < 128))
            discountPercentage = int(price.find('b', {'class': 'txtSale'}).get_text().replace('%', ''))

        h.cur.execute(
            "INSERT INTO bub_productcolor (id,colorId,color,pagePath,originalPrice,discountPrice,discountPercentage,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (id, colorId, color, url, originalPrice, discountPrice, discountPercentage, h.tDate))
        h.cur.connection.commit()

        '''!!!....Size Information....!!!!'''

        list = bsObj.find('select', id='intProductItemId')
        if list !=None:
            list=list.findAll('option')
            list = list[1:]
            for ele in list:
                sku=int(ele['value'])
                size=ele['title'].split(' ')[0]

                if category is 'Skor':
                    size = size[0:2]
                    if size.isdigit() and 35 < int(size) < 44:
                        size = wShoes[size]

                elif size in intSize:
                    size = wintSize[size]

                elif size.isdigit() and 21 < int(size) < 38 and category is 'Bottom':
                    size = wBottom[size]

                elif size.isdigit() and 31 < int(size) < 53 and int(size) % 2 == 0:
                    size = wTops[size]

                elif size.find('/') != -1:
                    size = size.split('/')[0]
                    if size in intSize:
                        size = wintSize[size]
                    elif size.isdigit() and 21 < int(size) < 38 and category is 'Bottom':
                        size = wBottom[size]
                    elif size.isdigit() and 31 < int(size) < 53 and int(size) % 2 == 0:
                        size = wTops[size]

                else:
                    size = size[0:2]
                    if size in intSize:
                        size = wintSize[size]
                    elif size.isdigit() and 21 < int(size) < 38 and category is 'Bottom':
                        size = wBottom[size]
                    elif size.isdigit() and 31 < int(size) < 53 and int(size) % 2 == 0:
                        size = wTops[size]

                quantity = ele['data-stock']
                if len(quantity) is 0 or int(quantity) is 0:
                    availability = 'Out of Stock'
                    quantity=0
                else:
                    availability = 'In Stock'
                    quantity=int(quantity)
                h.cur.execute(
                        "INSERT INTO bub_productsize (colorId,sku,size,availability,quantity,date) VALUES(%s,%s,%s,%s,%s,%s)",
                        (colorId, sku, size, availability, quantity, h.tDate))
                h.cur.connection.commit()

    except Exception as e:
        print("Error:\t",e)
        print(url)
        input('wait')
        return
