from datetime import date

tDate = date.today()

wTops={'32':'XS','34':'XS','36':'S','38':'S','40':'M','42':'L','44':'XL','46':'2XL','XX-Small':'2XS','X-Small':'XS','Small':'S','Medium':'M','Large':'L','X-Large':'XL','XX-Large':'2XL'}
wBottoms={'24':'XS','25':'XS','26':'S','27':'S','28':'M','29':'L','30':'L','31':'XL','32':'2XL','X-Small':'XS','Small':'S','Medium':'M','Large':'L','X-Large':'XL','XX-Large':'2XL'}
wShoes={'36':'S','37':'S','38':'M','39':'M','40':'L','41':'L','42':'XL','43':'XL'}
tSubcategory={'Blusar & Skjortor','Festklänningar','Jackor','Kavajer','Klänningar','T-Shirts','Tröjor','Toppar','Set Kläder','Jumpsuits','Baddräkter','Strandplagg','Sovplagg','Linnen'}
bSubcategory={'Byxor & Shorts','Kjolar','Leggings','Jeans','Bikini','Strumpbyxor & Stay-Ups','Trosor','Byxor Sport','Tights','Träningsshorts','Underkläder'}
shoes={'Skor löpning','Skor träning','Festskor','Vardagsskor'}

def productInfo(bsObj,cur):
    data=bsObj.find('input',{'class':'GA_productDetail'})
    ###print(data)
    id=int(data['data-articlenumber'].split('-')[0])
    name=data['data-name']
    brand=data['data-brand']
    subCategory = data['data-category']
    if subCategory in tSubcategory:
        category='Top'
    elif subCategory in bSubcategory:
        category = 'Bottom'
    elif subCategory in shoes:
        category = 'Skor'
    gender = 'female'

    cur.execute("INSERT INTO nel_productinfo (id,name,brand,gender,category,subcategory,date) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",(id,name,brand,gender, category, subCategory,tDate))
    cur.connection.commit()

    return (subCategory,id)

def colorInfo(bsObj,url,cur,id,subCategory):
    try:
        #print(url)
        data = bsObj.find('input', {'class': 'GA_productDetail'})
        colorId = data['data-articlenumber']
        #print(colorId)
        color=bsObj.find('span',{'itemprop':'color'}).get_text()
        #print(color)
        if bsObj.find('span',{'class':'price-sale'}) is None:
            originalPrice=bsObj.find('span',{'class':'product-price'}).find('span').get_text().replace(' ','')
            originalPrice = ''.join(i for i in originalPrice if ord(i) < 128)
            originalPrice=float(originalPrice)
            #print(originalPrice)
            discountPrice=0.0
            discountPercentage=0
        else:
            originalPrice=bsObj.find('span',{'class':'price-original'}).find('span').get_text().replace(' ','')
            originalPrice = ''.join(i for i in originalPrice if ord(i) < 128)
            originalPrice = float(originalPrice)
            #print(originalPrice)
            discountPrice=bsObj.find('span',{'class':'price-sale'}).find('span').get_text().replace(' ','')
            discountPrice = ''.join(i for i in discountPrice if ord(i) < 128)
            discountPrice=float(discountPrice)
            #print(discountPrice)
            discountPercentage=int(bsObj.find('span',{'class':'price-percentage'}).get_text().replace('%',''))


            #print(discountPercentage)
        aveRating=float(bsObj.find('ul',{'class':'product-rating'})['content'])
        #print(aveRating)
        ###print('Error 1')
        totalReviewer=int(bsObj.find('span',{'itemprop':'reviewCount'}).get_text().replace('(','').replace(')',''))
        #print(totalReviewer)
        ###print('Error 2')
        #print(id,colorId,color,originalPrice,discountPercentage,discountPrice,url,totalReviewer,aveRating)
        cur.execute("INSERT INTO nel_productcolor (id,colorId,color,pagePath,originalPrice,discountPrice,discountPercentage,totalReviewer, aveRating,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (id, colorId, color,url, originalPrice, discountPrice, discountPercentage,totalReviewer, aveRating,  tDate))
        cur.connection.commit()
        ###print('Error 3')

        '''!!!....Size Information....!!!!'''
        sList = bsObj.find('select', {'class': 'size-select'}).findAll('option')
        #print(sList)
        sList = sList[1:]
        ####print('Error 3')
        for ele in sList:
            sku=ele['value']
            size=ele.get_text().replace('EU','').replace(' ','')
            ###print('Error 4')
            #print(sku,size)
            if subCategory in tSubcategory:
                if size.isdigit() is False:
                    size=wTops[size]
                elif 31 < int(size) < 47:
                    size = wTops[size]

            elif subCategory in bSubcategory:
                if size[0]=='W':
                    size = wBottoms[size[1:3]]
                elif size.isdigit() is False:
                    size=wBottoms[size]
                elif 23 < int(size) < 33 :
                    size = wBottoms[size]
            elif  subCategory in shoes:
                size = wShoes[size]
            ###print('Error 5')
            if len(ele.attrs)==1:
                availability="In Stock"
            else:
                availability="Out of Stock"
            #print(availability)
            cur.execute("INSERT INTO nel_productsize (colorId,sku,size,availability,date) VALUES(%s,%s,%s,%s,%s)",
                    (colorId, sku, size, availability, tDate))
            cur.connection.commit()

    except Exception as e:
        print("Error:\t",e)
        #input('wait')
        return