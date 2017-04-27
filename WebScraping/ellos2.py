"""...........This file scrape all the product information from the client website, fetch the data from the Google Analytic API
 and store all the data in a database.............."""

import header as h

urlDict = {"pageValue": 0.0, "pageViews": 0, "entrances": 0, "entrancesRate": 0.0, "pageviewsPerSession": 0.0,"uniquePageViews": 0, "timeOnPage": 0.0, "aveTimeOnPage": 0.0, "exits": 0, "exitRate": 0.0}
id=0

#list of categories for whom data will be scraped from the client website........"""

tCategory={'overdelar','ytterplagg','Jackor','Set','T-shirts','Toppar','Tröjor'}
bCategory={'nederdelar','Underkläder, sov & bad','underklader-bad','Byxor','Shorts','Tights','Underkläder','Trosor'}

#Mapping of a retailer size measure scale into international scale size........"""

intSize={'XXS','XS','S','M','L','XL','2XL','3XL','4XL','5XL','6XL'}
wintSize={'XXS':'X','XS':'X','S':'S','M':'M','L':'L','XL':'X','2XL':'X','3XL':'X','4XL':'X','5XL':'X','6XL':'X'}
wTops={'30':'X','32':'X','34':'S','36':'S','38':'M','40':'M','42':'L','44':'L','46':'X','48':'X','50':'X','52':'X','54':'X','56':'X','58':'X','60':'X','62':'X','64':'X','66':'X','68':'X'}
wBottom={'23':'X','24':'X','25':'X','26':'S','27':'S','28':'S','29':'M','30':'M','31':'M','32':'L','33':'L','34':'X','35':'X','36':'X','37':'X'}
wShoes={'36':'S','37':'S','38':'M','39':'M','40':'L','41':'L','42':'X','43':'X'}

#Initial the dictionary for each new PageURL for a unique product and convert the values into a appropriate formate

def init(value):
    urlDict['pageValue'] = float(value[0])
    urlDict["pageViews"] = int(value[1])
    urlDict["entrances"] = int(value[2])
    urlDict["entranceRate"] = float(value[3])
    urlDict["pageviewsPerSession"] = float(value[4])
    urlDict["uniquePageViews"] = int(value[5])
    urlDict["timeOnPage"] = float(value[6])
    urlDict["aveTimeOnPage"] = float(value[7])
    urlDict["exits"] = int(value[8])
    urlDict["exitRate"] = float(value[9])

#Each product can have multiple path and Google Analytic store each path information as a new record even though it's a same product.
#This function add multiple path infromation into a single record for a unique product

def addValue(value):
    urlDict['pageValue'] += float(value[0])
    urlDict["pageViews"] += int(value[1])
    urlDict["entrances"] += int(value[2])
    urlDict["entranceRate"] += float(value[3])
    urlDict["pageviewsPerSession"] += float(value[4])
    urlDict["uniquePageViews"] += int(value[5])
    urlDict["timeOnPage"] += float(value[6])
    urlDict["aveTimeOnPage"] += float(value[7])
    urlDict["exits"] += int(value[8])
    urlDict["exitRate"] += float(value[9])

#Receive the response object from the Google Analytic API for a parameter product page URL, extract the relevant the data and store it in a database

def urlData(analyticsReproting,idList):
    oldId=0
    response = h.apiData.urlData(analyticsReproting, "0")
    print(response)
    pagesNum = h.math.ceil((response['reports'][0]['data']['rowCount']) / 1000)
    for i in range(pagesNum - 1):
        data = response['reports'][0]['data']['rows']
        j = 0
        while j < 1000:
            value = data[j]['metrics'][0]['values']
            dim = data[j]['dimensions']
            newId=int(dim[0].split('/')[3].split('?')[0])
            if oldId!=newId:
                init(value)
                oldId = newId
            else:
                addValue(value)
            j = j + 1
            if id in idList:
                while (j < 1000 and oldId == int(data[j]['dimensions'][0].split('/')[3].split('?')[0])):
                    value = data[j]['metrics'][0]['values']
                    addValue(value)
                    j += 1

                if j < 1000 - 1 or i == pagesNum - 2:
                    try:
                        h.cur.execute(
                            "INSERT INTO producttitle (id,pageValue,pageViews,entrances,entranceRate,pageviewsPerSession,"
                            "uniquePageViews,timeOnPage,aveTimeOnPage,exits,exitRate,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (id, urlDict["pageValue"], urlDict["pageViews"], urlDict["entrances"], urlDict["entranceRate"],
                             urlDict["pageviewsPerSession"], urlDict["uniquePageViews"], urlDict["timeOnPage"],
                             urlDict["aveTimeOnPage"],
                             urlDict["exits"], urlDict["exitRate"],h.tDate))
                        h.cur.connection.commit()
                    except Exception as e:
                        print("duplicate issues", e)
        response = h.apiData.urlData(analyticsReproting, response['reports'][0]['nextPageToken'])

#Receive the response object from the Google Analytic API for a parameter Product Size SKU, extract the relevant the data and store it in a database

def skuData(analyticsReporting,skuList):
    # Google Analytics API Data for a product
    print('sku also fine')
    try:
        response = h.apiData.skuData(analyticsReporting,"0")
        pagesNum = h.math.ceil((response['reports'][0]['data']['rowCount']) / 1000)
        for i in range(pagesNum - 1):
            data = response['reports'][0]['data']['rows']
            j = 0
            while j < 1000:
                value=data[j]['metrics'][0]['values']
                dim = data[j]['dimensions']
                if int(dim[0]) in skuList:
                    h.cur.execute("INSERT INTO productsize2 (sku,itemQuantity,uniquePurchases,revenuePerItem,itemRevenue,itemsPerPurchase,productRevenuePerPurchase,date)"
                            " VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(int(dim[0]),value[0],value[1],value[2],value[3],value[4],value[5],h.tDate))
                    h.cur.connection.commit()
                j+=1
            response = h.apiData.skuData(analyticsReporting, response['reports'][0]['nextPageToken'])
    except Exception as e:
        print("Data Not available for sku")

#Scraping the product data from the client website and stroing the data in a database

def productInfo(bsObj,url,skuList):
    try:
        #print(cur)
        """!!!...Extract and Format a Json File...!!!"""

        jsFiles = bsObj.findAll("script", {"type": "text/javascript"})
        for file in jsFiles:
            if file.get_text().find(" var product",0,150) != -1:
                jsFile=file.get_text()

        jsFile = jsFile.split('};')[0]
        #jsFile = list[0]
        jsFile = jsFile.replace("var product =", " ")
        string = " "
        seq = (jsFile, "}")
        jsonFile = string.join(seq)
        responseJson = h.json.loads(jsonFile)

        """!!!...get Product info from json file...!!!"""

        id = responseJson['Id']
        name=responseJson['Headline']
        brand=responseJson['Brand']
        gender=responseJson['GenderDepartmentText']
        subCategory=responseJson['ProductDepartmentLinkText']
        category = responseJson['ProductDepartmentLink'].split('/')[2]

        if category in tCategory or subCategory in tCategory:
            subCategory = category
            category = 'Top'
        elif category in bCategory or subCategory in bCategory:
            subCategory = category
            category = 'Bottom'

        """...Rating...."""

        rating = bsObj.find("div", id="BVRRContainer")
        if rating is None or rating.find("span", {"itemprop": "ratingValue"}) is None:
            aveRating = 0.0
            totalReviewer=0
        else:
            aveRating = rating.find("span", {"itemprop": "ratingValue"}).get_text().replace(",",".")
            totalReviewer = rating.find("span", {"itemprop": "reviewCount"}).get_text()

        h.cur.execute("INSERT INTO productinfo (id,pagePath,brand,name,gender,category,subcategory,ratingCount,ratingValue,date) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,url, brand, name, gender, category, subCategory, totalReviewer, aveRating,h.tDate))
        h.cur.connection.commit()

        Discount = responseJson['DiscountPercentage']
        if Discount is 0:
            originalPrice=responseJson['Price'].split('<')[0].replace(",",".")
            originalPrice=''.join(i for i in originalPrice if ord(i)<128)
            discountPrice=0
            discountPercentage=0
        else:
            originalPrice=responseJson['OriginalPrice'].split('<')[0].replace(",",".")
            originalPrice = ''.join(i for i in originalPrice if ord(i) < 128)
            discountPrice=responseJson['Price'].split('<')[0].replace(",",".")
            discountPrice = ''.join(i for i in discountPrice if ord(i) < 128)
            discountPercentage=responseJson['DiscountPercentage']

        products = responseJson['Articles']
        for product in products:
            if product['Headline'].find(product['Color'])!=-1 or len(product['Color'])==0 :
                color=None
            else:
                color=product['Color']
            colorId=product['Id']
            h.cur.execute("INSERT INTO productcolor (id,colorId,color,originalPrice,discountPrice,discountPercentage,date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (id,colorId,color,originalPrice,discountPrice,discountPercentage,h.tDate))
            h.cur.connection.commit()

            variants = product['Variants']
            for variant in variants:
                if len(variant['Size']) is 0:
                    size=0
                else:
                    size=str(variant['SizeSort'])
                    size1=variant['Size']

                    if category is 'Skor':
                        size = size[0:2]
                        if size.isdigit() and 35 < int(size) < 44:
                            size = wShoes[size]

                    elif size in intSize:
                        size = wintSize[size]

                    elif size[0] is 'W':
                        size = wBottom[size[1:3]]

                    elif  size.isdigit() and 22 < int(size) < 38 and category is 'Bottom':
                            size=wBottom[size]

                    elif size.isdigit() and 29 < int(size) < 69 and int(size) % 2 == 0:
                        size = wTops[size]

                    elif size.find('/') != -1:
                        size = size.split('/')[0]
                        if size in intSize:
                            size = wintSize[size]
                        elif size.isdigit() and 22 < int(size) < 38 and category is 'Bottom':
                            size = wBottom[size]
                        elif size.isdigit() and 29 < int(size) < 69 and int(size) % 2 == 0:
                            size = wTops[size]

                    else:
                        size = size[0:2]
                        if size in intSize:
                            size = wintSize[size]
                        elif size.isdigit() and 22 < int(size) < 38 and category is 'Bottom':
                            size = wBottom[size]
                        elif size.isdigit() and 29 < int(size) < 69 and int(size) % 2 == 0:
                            size = wTops[size]

                skuList.add(variant['Id'])
                quantity=variant['Availability']
                availability=variant['ShipsWhen']
                h.cur.execute("INSERT INTO productsize (colorId,sku,size,quantity,availability,date) VALUES(%s,%s,%s,%s,%s,%s)",
                            (colorId, variant['Id'], size, quantity, availability,h.tDate))
                h.cur.connection.commit()
    except Exception as e:
        print("Error:\t",e)
    return