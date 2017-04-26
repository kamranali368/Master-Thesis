#import json
#from datetime import date
#tDate = date.today()
import header as h

tCategory={'Klänningar','Ytterkläder','Överdelar','Badkläder'}
bCategory={'Nederdelar','Lingerie'}


wTops={'32':'X','34':'S','36':'S','38':'M','40':'L','42':'X','44':'X','46':'X','48':'X','50':'X','52':'X'}
intSize={'XXS','XS','S','M','L','XL','XXL','XXXL','XXXXL'}
wintSize={'XXS':'X','XS':'X','S':'S','M':'M','L':'L','XL':'X','XXL':'X','XXXL':'X','XXXXL':'X'}
wBottom={'26':'X','27':'S','28':'S','29':'M','30':'L','31':'X','32':'X','33':'X','34':'X','35':'X','36':'X','37':'X'}
wShoes={'36':'S','37':'S','38':'M','39':'M','40':'L','41':'L','42':'X','43':'X'}




def productInfo(bsObj,url,colorList):

    try:
        id=bsObj.find('span',{'class','prd-item-number'}) #data ean id

        '''...!!!# Some product go out of color ?Size...'''
        if id is None:
            return

        id=id.get_text()
        brand=bsObj.find('span',{'itemprop':'brand'}).get_text()
        name=bsObj.find('div',{'class':'product-details'}).find('span',{'itemprop':'name'}).get_text()
        gender='female'
        list = bsObj.findAll('a', {'class': 'product-breadcrumbs__item'})# list=bsObj.findAll('a',{'class':'bread-crumb'})
        subCategory=list[len(list)-1].get_text().replace(' ','').replace('\n','').replace('\r','')
        #print(subCategory)
        if subCategory in tCategory:
            category = 'Top'
        elif subCategory in bCategory:
            category = 'Bottom'
        else:
            category = 'Skor'

        if bsObj.find('abbr',{'itemprop':'reviewCount'}) is None:
            totalReviewer=0
            aveRating=0.0
        else:
            totalReviewer=bsObj.find('abbr',{'itemprop':'reviewCount'}).get_text()
            aveRating=bsObj.find('abbr',{'itemprop':'ratingValue'}).get_text()

        h.cur.execute("INSERT INTO boo_productinfo (id,pagePath,brand,title,gender,category,subcategory,ratingCount,ratingValue,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (id, url, brand, name, gender, category, subCategory, totalReviewer, aveRating, h.tDate))
        h.cur.connection.commit()

        for col in colorList:
            colorId=int(col['data-variant-id'])
            color=bsObj.find('li',{'data-variant':col['data-variant-id']})
            if color is not None:
                color=color['title']
            discountPercentage=col['data-srate']
            if len(discountPercentage) is 0 or discountPercentage=='0':
                originalPrice=float(col['data-price'].replace(' kr',''))
                discountPrice=0.0
                discountPercentage=0
            else:
                originalPrice=float(col['data-price'].replace(' kr',''))
                discountPrice=float(col['data-sprice'].replace(' kr',''))
            h.cur.execute("INSERT INTO boo_productcolor (id,colorId,color,originalPrice,discountPrice,discountPercentage,date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (id, colorId, color, originalPrice, discountPrice, int(discountPercentage), h.tDate))
            h.cur.connection.commit()

        """!!!...Extract and Format a Json File...!!!"""

        jsFiles = bsObj.findAll("script", {"type": "text/javascript"})
        for file in jsFiles:
            if file.get_text().find("App.Config.fbid", 0, 150) != -1:
                jsFile = file.get_text()

        jsFile = jsFile.split('App.Config.Details =')[1]
        jsFile = jsFile.split('};')[0]
        string = " "
        seq = (jsFile, "}")
        jsonFile = string.join(seq)
        responseJson = h.json.loads(jsonFile)

        list=responseJson['allEans']
        for i in list:
            colorId=int(i['variant_id'])
            sku=int(i['ean_id'])
            size=i['size_filter']

            if category is 'Skor':
                size=size[0:2]
                if size.isdigit() and 35 < int(size) < 44:
                    size = wShoes[size]

            elif size in intSize:
                size=wintSize[size]

            elif size.isdigit() and 25<int(size)<38 and category is 'Bottom':
                size=wBottom[size]

            elif size.isdigit() and  31< int(size) < 53 and int(size)%2==0:
                size = wTops[size]

            elif size.find('/') !=-1:
                size=size.split('/')[0]
                if size in intSize:
                    size=wintSize[size]
                elif size.isdigit() and 25<int(size)<38 and category is 'Bottom':
                    size=wBottom[size]
                elif size.isdigit() and  31< int(size) < 53 and int(size)%2==0:
                    size=wTops[size]

            else:
                size=size[0:2]
                if size in intSize:
                    size = wintSize[size]
                elif size.isdigit() and 25 < int(size) < 38 and category is 'Bottom':
                    size = wBottom[size]
                elif size.isdigit() and 31 < int(size) < 53 and int(size)%2==0:
                    size = wTops[size]

            quantity=int(i['stock'])

            h.cur.execute("INSERT INTO boo_productsize (colorId,sku,size,quantity,date) VALUES(%s,%s,%s,%s,%s)",
                    (colorId, sku, size, quantity, h.tDate))
            h.cur.connection.commit()

    except Exception as e:
        print("Error:\t", e)
        print(url)
    return



