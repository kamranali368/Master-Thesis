"""........This file contains all the database queries to retrieve the data from the database and
group the data based on a specific parameter to perform category, product and brand level analyses.........."""

import pymysql
from pandas.io import sql
import pandas as pd
import graphs
date1 = '2016-08-24'
date2 = '2016-08-23'
var=['productinfo','bub_productinfo','boo_productinfo']
var1=['productcolor','bub_productcolor','boo_productcolor']
var2=['productsize','bub_productsize','boo_productsize']
retName=['ellos','bubble','boozt']
brandName = []
topBrand=[]
topBrand1=[]
topBrand2=[]

"""............Category Level Aanlysis.........."""

def runQueryatCategoryLevel():

    """.........Total products in each category for each Retailer......."""

    df = pd.DataFrame()

    for o,z in zip(var,retName):
        query1="SELECT category,count(id) AS totalProduct from %s"%o
        query2=query1+" where date=%s and (category='Top' or category='Bottom' or  category='Skor') group by category ORDER BY count(id) DESC "
        results = sql.read_sql(query2, con=conn,params=[date1])
        results['retailer']=z
        df=df.append(results)
        df['category'] = df["category"].map(lambda x: x if type(x) != str else x.lower())
    print(df)

    header=df.dtypes.index

    #Call a multiple bar graph function
    graphs.multipleBar(df,header[0],header[1],header[2])
    print('\n')


    """....No of offered products in each category for every Retailer.... """

    df = pd.DataFrame()
    for o,i,z in zip(var,var1,retName):
        query1="select o.category,count(DISTINCT i.id) as offeredProduct from %s as o INNER JOIN %s as i on o.id=i.id"%(o,i)
        query2=query1+" WHERE o.date=%s AND i.date=%s AND (o.category='Top' OR o.category='Bottom' OR o.category='Skor') AND i.discountPercentage >0 " \
                      "GROUP BY o.category ORDER BY offeredProduct DESC "
        results = sql.read_sql(query2, con=conn, params=[date1,date1])
        results['retailer'] = z
        df = df.append(results)

    df['category'] = df["category"].map(lambda x: x if type(x) != str else x.lower())
    header = df.dtypes.index
    graphs.multipleBar(df, header[0], header[1], header[2])
    print(df)
    print('\n')

    """....Offer Percentage in each category for every Retailer.... """

    df = pd.DataFrame()
    for o, i, z in zip(var, var1, retName):
        query1="select o.category,AVG (i.discountPercentage) as offeredPercentage from %s as o INNER JOIN %s as i on o.id=i.id"%(o,i)
        query2=query1+" WHERE o.date=%s AND i.date=%s AND (o.category='Top' OR o.category='Bottom' OR o.category='Skor') AND i.discountPercentage >0 " \
                      "GROUP BY o.category ORDER BY offeredPercentage DESC "
        results = sql.read_sql(query2, con=conn, params=[date1,date1])
        results['retailer'] = z
        df = df.append(results)

    df['category'] = df["category"].map(lambda x: x if type(x) != str else x.lower())
    header = df.dtypes.index
    graphs.multipleBar(df, header[0], header[1], header[2])
    print(df)
    print('\n')


    """....Color Variation in each category for every Retailer.... """

    df = pd.DataFrame()
    for o, i, z in zip(var, var1, retName):
        query1_top="select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount " \
                   "FROM (select o.id from %s" \
                   " AS o inner join %s AS i on o.id=i.id"%(o,i)
        query2_top=query1_top+" where i.date=%s and o.date=%s AND o.category='Top' ) as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2_top, con=conn, params=[date1,date1])
        #Addition Needed:  No need to add a saeprate category in each data frame just use o.category in the SQL Query
        results['category'] = 'top'
        results['retailer'] = z
        df = df.append(results.ix[0:3,:])

        query1_bottom="select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount FROM (select o.id from %s" \
                      " AS o inner join %s AS i on o.id=i.id"%(o,i)
        query2_bottom =query1_bottom+" where i.date=%s and o.date=%s AND o.category='Bottom') as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2_bottom, con=conn, params=[date1,date1])
        results['category'] = 'bottom'
        results['retailer'] = z
        df = df.append(results.ix[0:3, :])

        query1_skor="select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount FROM (select o.id from %s" \
                    " AS o inner join %s AS i on o.id=i.id"%(o,i)
        query2_skor =query1_skor+" where i.date=%s and o.date=%s AND o.category='Skor' ) as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2_skor, con=conn, params=[date1,date1])
        results['category'] = 'skor'
        results['retailer'] = z
        df = df.append(results.ix[0:3, :])

    df['category'] = df["category"].map(lambda x: x if type(x) != str else x.lower())
    header = df.dtypes.index
    graphs.stackedMultiBar(df, header[0], header[1], header[2],header[3])
    print(df)
    print('\n')


    """.......Size Variation in each category for every Retailer.... """

    df = pd.DataFrame()
    for o, i, p, z in zip(var, var1,var2, retName):
        query1_top="select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId"%(o,i,p)
        query2_Top=query1_top+" WHERE o.category='Top' and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2_Top, con=conn, params=[date1, date1,date1])
        results['category'] = 'top'
        results['retailer'] = z
        df = df.append(results)

        query1_bottom="select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId"%(o,i,p)
        query2_bottom =query1_bottom+ " WHERE o.category='Bottom' and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2_bottom, con=conn, params=[date1, date1, date1])
        results['category'] = 'bottom'
        results['retailer'] = z
        df = df.append(results)

        query1_skor="select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId"%(o,i,p)
        query2_skor =query1_skor+ " WHERE o.category='Skor' and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2_skor, con=conn, params=[date1, date1, date1])
        results['category'] = 'skor'
        results['retailer'] = z
        df = df.append(results)

    df['category'] = df["category"].map(lambda x: x if type(x) != str else x.lower())
    header = df.dtypes.index
    graphs.stackedMultiBar(df, header[0], header[1], header[2], header[3])
    print(df)
    print('\n')

    """............Item Sold in each category........... """

    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    """....Yesterday....."""
    for o, i, p, z in zip(var[1:], var1[1:], var2[1:], retName[1:]):
        query1_top = "select o.category,p.size,p.sku,p.quantity  from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2_Top = query1_top + " WHERE (o.category='Top' or o.category='Bottom' or o.category='Skor') and o.date=%s and i.date=%s AND p.date=%s AND " \
                                  "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') "
        results = sql.read_sql(query2_Top, con=conn, params=[date1, date1, date1])
        results['retailer'] = z
        df1 = df1.append(results)

        """....Before Yesterday....."""

        query1_top = "select o.category,p.size,p.sku,p.quantity from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2_Top = query1_top + " WHERE (o.category='Top' or o.category='Bottom' or o.category='Skor') and o.date=%s and i.date=%s AND p.date=%s AND " \
                                  "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
        results = sql.read_sql(query2_Top, con=conn, params=[date2, date2, date2])
        results['retailer'] = z
        df2 = df2.append(results)

    query = "SELECT o.category as category_x,p.size as size_x,p.sku,q.itemQuantity as itemsold from productinfo AS o INNER JOIN productcolor AS i ON o.id=i.id INNER JOIN productsize AS p on p.colorId=i.colorId " \
            "INNER JOIN  productsize2 as q ON p.sku=q.sku WHERE o.date=%s AND i.date=%s AND p.date=%s AND q.date=%s AND (o.category='Top' or o.category='Bottom' or o.category='Skor') AND " \
            "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
    results = sql.read_sql(query, con=conn, params=[date1, date1, date1, date1])
    results['retailer_x'] = retName[0]


    df=pd.merge(df1,df2,on='sku',how='inner')
    df['itemsold'] = df['quantity_y'] - df['quantity_x']
    df = df.append(results)
    df=df[df['itemsold']>0]
    df['category_x'] = df["category_x"].map(lambda x: x if type(x) != str else x.lower())
    header = df.dtypes.index
    graphs.stackedMultiBar(df, header[7], header[2], header[0], header[5])

    print(df[0:20])
    print('\n')

    """....Revenue in each category.... """

    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    """....Yesterday....."""

    for o, i, p, z in zip(var[1:], var1[1:], var2[1:], retName[1:]):
        query1="select o.category,p.size,p.sku,p.quantity,i.originalPrice,i.discountPercentage from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId"%(o,i,p)
        query2=query1+" WHERE (o.category='Top' or o.category='Bottom' or o.category='Skor') and o.date=%s and i.date=%s AND p.date=%s AND " \
                               "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
        results = sql.read_sql(query2, con=conn, params=[date1, date1, date1])
        results['retailer'] = z
        df1 = df1.append(results)

        """........Before Yesterday......"""

        query1 = "select o.category,p.size,p.sku,p.quantity,i.originalPrice,i.discountPercentage from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " WHERE (o.category='Top' or o.category='Bottom' or o.category='Skor') and o.date=%s and i.date=%s AND p.date=%s AND " \
                          "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
        results = sql.read_sql(query2, con=conn, params=[date2, date2, date2])
        results['retailer'] = z
        df2 = df2.append(results)

    query = "SELECT o.category as category_x,p.size as size_x,p.sku,q.itemQuantity as itemsold,q.itemRevenue as revenue from productinfo AS o INNER JOIN productcolor AS i ON o.id=i.id INNER JOIN productsize AS p on p.colorId=i.colorId " \
            "INNER JOIN  productsize2 as q ON p.sku=q.sku WHERE o.date=%s AND i.date=%s AND p.date=%s AND q.date=%s AND (o.category='Top' or o.category='Bottom' or o.category='Skor') AND " \
                "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
    results = sql.read_sql(query, con=conn, params=[date1, date1, date1, date1])
    results['retailer_x'] = retName[0]

    df = pd.merge(df1, df2, on='sku', how='inner')
    df['itemsold'] = df['quantity_y'] - df['quantity_x']
    df = df[df['itemsold'] > 0]
    df['price']=df['originalPrice_x']-(df['discountPercentage_x']/100)

    df['revenue']=df['price']*df['itemsold']
    df=df.append(results)

    df['category_x'] = df["category_x"].map(lambda x: x if type(x) != str else x.lower())
    header = df.dtypes.index
    graphs.stackedMultiBar(df, header[13], header[12], header[0], header[10])

    print(df[0:20])
    print('\n')


"""............. Brand Level Aanlysis............"""

def runQueryatBrandLevel():

    """....Total products in top 5 common brands for every Retailer......"""

    df = pd.DataFrame()

    query1 = "SELECT brand,count(id) AS totalProduct from productinfo where date=%s group by brand ORDER BY count(id) DESC "
    results1 = sql.read_sql(query1, con=conn, params=[date1])
    results1['retailer']=retName[0]
    df = df.append(results1)

    query1 = "SELECT brand,count(id) AS totalProduct from bub_productinfo where date=%s group by brand ORDER BY count(id) DESC "
    results2 = sql.read_sql(query1, con=conn, params=[date1])
    results2['retailer'] = retName[1]
    df = df.append(results2)

    query1 = "SELECT brand,count(id) AS totalProduct from boo_productinfo where date=%s group by brand ORDER BY count(id) DESC "
    results3 = sql.read_sql(query1, con=conn, params=[date1])
    results3['retailer'] = retName[2]
    df = df.append(results3)

    list1 = results1['brand'].tolist()
    list2 = results2['brand'].tolist()
    list3 = results3['brand'].tolist()


    for brand in list1:
        if brand in list2 and brand in list3:
            brandName.append(brand)
    topBrand=brandName[:5]

    df.set_index('brand',inplace=True)

    df = df.ix[topBrand, :]

    df.reset_index(inplace=True)
    header = df.dtypes.index
    graphs.multipleBar(df, header[0], header[1], header[2])

    print(df)
    print('\n')

    """.........No of offered products in top 5 common brands for every Retailer.......... """

    df = pd.DataFrame()
    for o, i, z in zip(var, var1, retName):
        query1 = "select o.brand,count(DISTINCT i.id) as offeredProduct from %s as o INNER JOIN %s as i on o.id=i.id " % (o, i)
        query2 = query1 + "WHERE o.date=%s AND i.date=%s AND (o.brand=%s OR o.brand=%s OR o.brand=%s OR o.brand=%s OR o.brand=%s) AND i.discountPercentage >0 GROUP BY o.brand ORDER BY offeredProduct DESC "
        results = sql.read_sql(query2, con=conn, params=[date1, date1,topBrand[0],topBrand[1],topBrand[2],topBrand[3],topBrand[4]])
        results['retailer'] = z
        df = df.append(results)

    header = df.dtypes.index
    graphs.multipleBar(df, header[0], header[1], header[2])
    print(df)
    print('\n')

    """..........Offer Percentage in top 5 common brands for every Retailer.........."""

    df = pd.DataFrame()
    for o, i, z in zip(var, var1, retName):
        query1 = "select o.brand,AVG (i.discountPercentage) as offeredPercentage from %s as o INNER JOIN %s as i on o.id=i.id" % (o, i)
        query2 = query1 + " WHERE o.date=%s AND i.date=%s AND (o.brand=%s OR o.brand=%s OR o.brand=%s OR o.brand=%s OR o.brand=%s) AND i.discountPercentage >0 " \
                          "GROUP BY o.brand ORDER BY offeredPercentage DESC "
        results = sql.read_sql(query2, con=conn, params=[date1, date1,topBrand[0],topBrand[1],topBrand[2],topBrand[3],topBrand[4]])
        results['retailer'] = z
        df = df.append(results)

    header = df.dtypes.index
    graphs.multipleBar(df, header[0], header[1], header[2])
    print(df)
    print('\n')

    """.........Color Variation in top 5 common brands for every Retailer........."""

    df = pd.DataFrame()
    for o, i,z in zip(var, var1, retName):
        query1 = "select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount FROM (select o.id from %s" \
                     " AS o inner join %s AS i on o.id=i.id" % (o, i)
        query2 = query1 + " where i.date=%s and o.date=%s AND o.brand=%s ) as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2, con=conn, params=[date1, date1,topBrand[0]])
        results['brand'] = topBrand[0]
        results['retailer'] = z
        df = df.append(results.ix[0:3, :])

        query1 = "select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount FROM (select o.id from %s" \
                        " AS o inner join %s AS i on o.id=i.id" % (o, i)
        query2 = query1 + " where i.date=%s and o.date=%s AND o.brand=%s) as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2, con=conn, params=[date1, date1,topBrand[1]])
        results['brand'] = topBrand[1]
        results['retailer'] = z
        df = df.append(results.ix[0:3, :])

        query1 = "select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount FROM (select o.id from %s" \
                      " AS o inner join %s AS i on o.id=i.id" % (o, i)
        query2 = query1 + " where i.date=%s and o.date=%s AND o.brand=%s ) as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2, con=conn, params=[date1, date1,topBrand[2]])
        results['brand'] = topBrand[2]
        results['retailer'] = z
        df = df.append(results.ix[0:3, :])

        query1 = "select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount FROM (select o.id from %s" \
                 " AS o inner join %s AS i on o.id=i.id" % (o, i)
        query2 = query1 + " where i.date=%s and o.date=%s AND o.brand=%s ) as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2, con=conn, params=[date1, date1, topBrand[3]])
        results['brand'] = topBrand[3]
        results['retailer'] = z
        df = df.append(results.ix[0:3, :])

        query1 = "select result.colorcount as colorNo,count(result.colorcount) AS products from (select infocolor.id,count(infocolor.id) as colorcount FROM (select o.id from %s" \
             " AS o inner join %s AS i on o.id=i.id" % (o, i)
        query2 = query1 + " where i.date=%s and o.date=%s AND o.brand=%s ) as infocolor GROUP BY infocolor.id) as result GROUP BY colorNo"
        results = sql.read_sql(query2, con=conn, params=[date1, date1, topBrand[4]])
        results['brand'] = topBrand[4]
        results['retailer'] = z
        df = df.append(results.ix[0:3, :])

    header = df.dtypes.index
    graphs.brandStackedMultiBar(df, header[0], header[1], header[2], header[3])
    print(df)
    print('\n')

    """..........Size Variation in top 5 common brands for every Retailer..........."""

    df = pd.DataFrame()
    for o, i, p, z in zip(var, var1, var2, retName):
        query1= "select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " where o.brand=%s and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2, con=conn, params=[topBrand[0],date1, date1, date1])
        results['brand'] = topBrand[0]
        results['retailer'] = z
        df = df.append(results)

        query1 = "select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " where o.brand=%s and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2, con=conn, params=[topBrand[1],date1, date1, date1])
        results['brand'] = topBrand[1]
        results['retailer'] = z
        df = df.append(results)

        query1 = "select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " where o.brand=%s and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2, con=conn, params=[topBrand[2],date1, date1, date1])
        results['brand'] = topBrand[2]
        results['retailer'] = z
        df = df.append(results)

        query1 = "select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " where o.brand=%s and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2, con=conn, params=[topBrand[3], date1, date1, date1])
        results['brand'] = topBrand[3]
        results['retailer'] = z
        df = df.append(results)

        query1 = "select p.size,count(o.id) as products from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " where o.brand=%s and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query2, con=conn, params=[topBrand[4], date1, date1, date1])
        results['brand'] = topBrand[4]
        results['retailer'] = z
        df = df.append(results)

    header = df.dtypes.index
    graphs.brandStackedMultiBar(df, header[0], header[1], header[2], header[3])
    print(df)
    print('\n')

    """....Items Sold in top 5 common brands.... """

    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    """....Yesterday....."""
    for o, i, p, z in zip(var[1:], var1[1:], var2[1:], retName[1:]):
        query1 = "select o.brand,p.size,p.sku,p.quantity from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " where (o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s) and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
        results = sql.read_sql(query2, con=conn, params=[topBrand[0],topBrand[1],topBrand[2],topBrand[3],topBrand[4],date1, date1, date1])
        results['retailer'] = z
        df1 = df1.append(results)

        """....Before Yesterday....."""

        query1 = "select o.brand,p.size,p.sku,p.quantity from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query2 = query1 + " where (o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s) and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
        results = sql.read_sql(query2, con=conn,params=[topBrand[0], topBrand[1], topBrand[2], topBrand[3], topBrand[4], date2, date2,date2])
        results['retailer'] = z
        df2 = df2.append(results)

    query = "SELECT o.brand as brand_x,p.size as size_x,p.sku as sku,q.itemQuantity as itemsold from productsize2 AS q INNER JOIN productsize AS p ON p.sku=q.sku INNER JOIN productcolor AS i on p.colorId=i.colorId " \
            "INNER JOIN  productinfo as o ON o.id=i.id WHERE o.date=%s AND i.date=%s AND p.date=%s AND q.date=%s AND (o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s) and " \
            "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')  "
    results = sql.read_sql(query, con=conn, params=[date1, date1, date1, date1,topBrand[0], topBrand[1], topBrand[2], topBrand[3], topBrand[4]])
    results['retailer_x'] = retName[0]

    df = pd.merge(df1, df2, on='sku', how='inner')
    df['itemsold'] = df['quantity_y'] - df['quantity_x']
    df = df[df['itemsold'] > 0]
    df = df.append(results)
    #df1['itemsold'] = df1['quantity'] - df2['quantity']
    #df = df1.ix[:, ['category', 'retailer', 'itemsold', 'size']].copy()
    header = df.dtypes.index
    graphs.brandStackedMultiBar(df, header[7], header[2], header[0], header[5])

    print(df)
    print('\n')

    """....Revenue in top 5 common brands.... """

    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    """....Yesterday....."""

    for o, i, p, z in zip(var[1:], var1[1:], var2[1:], retName[1:]):
        query1 = "select o.brand,p.size,p.sku,p.quantity,i.originalPrice,i.discountPercentage from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query = query1 + " where (o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s) and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
        results = sql.read_sql(query, con=conn, params=[topBrand[0], topBrand[1], topBrand[2], topBrand[3], topBrand[4],date1, date1, date1])
        results['retailer'] = z
        df1 = df1.append(results)

        """........Before Yesterday......"""

        query1 = "select o.brand,p.size,p.sku,p.quantity,i.originalPrice,i.discountPercentage from %s as o INNER JOIN %s as i on o.id=i.id INNER JOIN %s p on p.colorId=i.colorId" % (o, i, p)
        query = query1 + " where (o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s) and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
        results = sql.read_sql(query, con=conn,params=[topBrand[0], topBrand[1], topBrand[2], topBrand[3], topBrand[4], date2, date2,date2])
        results['retailer'] = z
        df2 = df2.append(results)


    query = "SELECT o.brand as brand_x,p.size as size_x,p.sku,q.itemQuantity as itemsold,q.itemRevenue as revenue from productsize2 AS q INNER JOIN productsize AS p ON p.sku=q.sku INNER JOIN productcolor AS i on p.colorId=i.colorId " \
                "INNER JOIN  productinfo as o ON o.id=i.id WHERE o.date=%s AND i.date=%s AND p.date=%s AND q.date=%s AND (o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s or o.brand=%s) AND " \
                "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L')"
    results = sql.read_sql(query, con=conn, params=[date1, date1, date1, date1,topBrand[0], topBrand[1], topBrand[2], topBrand[3], topBrand[4]])
    results['retailer_x'] = retName[0]

    df = pd.merge(df1, df2, on='sku', how='inner')
    df['itemsold'] = df['quantity_y'] - df['quantity_x']
    df = df[df['itemsold'] > 0]
    df['price'] = df['originalPrice_x'] - (df['discountPercentage_x'] / 100)

    df['revenue'] = df['price'] * df['itemsold']
    df = df.append(results)

    header = df.dtypes.index
    graphs.brandStackedMultiBar(df, header[13], header[12], header[0], header[10])


"""............. Product Level Aanlysis................."""

def runQueryPromotion():

    """.....productNumber on offer over the week..."""

    df = pd.DataFrame()
    """.....Day1..."""
    for i,z in zip(var1,retName):

        query1="SELECT date,count(DISTINCT id) as productOnOffer from %s"%i
        query2 =query1+ " where date=%s AND discountPercentage >0 "
        results = sql.read_sql(query2, con=conn, params=[date2])
        results['retailer']=z
        df=df.append(results)

        """.....Day2...."""

        query1 = "SELECT date,count(DISTINCT id) as productOnOffer from %s" % i
        query2 = query1 + " where date=%s AND discountPercentage >0 "
        results = sql.read_sql(query2, con=conn, params=[date1])
        results['retailer'] = z
        df = df.append(results)

    print(df)
    header = df.dtypes.index
    graphs.lines(df, header[0], header[1], header[2])

    """.....Offer Percentage over the week..........."""

    df = pd.DataFrame()
    """.....Day1..."""
    for i, z in zip(var1, retName):

        query1="SELECT date,AVG(discountPercentage) as discountPercentage from %s "%i
        query2 =query1+"where date=%s AND discountPercentage >0 "
        results = sql.read_sql(query2, con=conn, params=[date2])
        results['retailer'] = z
        df = df.append(results)

        """.....Day2...."""

        query1 = "SELECT date,AVG(discountPercentage) as discountPercentage  from %s " % i
        query2 = query1 + "where date=%s AND discountPercentage >0 "
        results = sql.read_sql(query2, con=conn, params=[date1])
        results['retailer'] = z
        df = df.append(results)

    print(df)
    header = df.dtypes.index
    graphs.lines(df, header[0], header[1], header[2])

    """..........API Level Analysis..........."""

def runQueryatApiLevel():

    """.....Transaction and Revenue for each brand...."""
    df = pd.DataFrame()

    query = "SELECT o.brand,SUM(q.itemQuantity) as itemSold ,SUM(q.itemRevenue) from productsize2 AS q INNER JOIN productsize AS p ON p.sku=q.sku INNER JOIN productcolor AS i on p.colorId=i.colorId " \
            "INNER JOIN  productinfo as o ON o.id=i.id WHERE o.date=%s AND i.date=%s AND p.date=%s AND q.date=%s GROUP BY o.brand ORDER BY SUM(q.itemQuantity) DESC "
    results1 = sql.read_sql(query, con=conn, params=[date1, date1, date1, date1])


    """.....Traffic/views for each brand......."""

    query = "SELECT o.brand,SUM(k.pageViews) as pageViews from producttitle as k INNER JOIN  productinfo as o ON o.id=k.id WHERE o.date=%s AND k.date=%s GROUP BY o.brand ORDER BY SUM(k.pageViews) DESC "
    results2 = sql.read_sql(query, con=conn, params=[date1, date1])

    for i,j in zip(results1['brand'],results2['brand']):
        if i==j:
            topBrand1.append(i)
        else:
            topBrand2.append(i)
            topBrand2.append(j)

    topBrand = topBrand1[:3]
    topBrand.append(topBrand2[0])
    topBrand.append(topBrand2[1])

    results1.set_index('brand',inplace=True)
    results2.set_index('brand',inplace=True)

    df1=results1.ix[topBrand,:]

    print(df1)

    df2=results2.ix[topBrand,:]
    print(df2)

    graphs.yAxis(topBrand,df1['itemSold'],df2['pageViews'])

    """.........Offer % for each brand........"""

    df = pd.DataFrame()

    query = "select o.brand,AVG (i.discountPercentage) as offeredPercentage from productinfo as o INNER JOIN productcolor as i on o.id=i.id " \
            "WHERE o.date=%s AND i.date=%s AND (o.brand=%s OR o.brand=%s OR o.brand=%s OR o.brand=%s OR o.brand=%s) AND i.discountPercentage >0 GROUP BY o.brand ORDER BY offeredPercentage DESC "
    results = sql.read_sql(query, con=conn,params=[date1, date1, topBrand[0], topBrand[1], topBrand[2], topBrand[3], topBrand[4]])
    df = df.append(results)

    graphs.singleLine(df)
    print(df)
    print('\n')


    """.........Size Popularity for each brand..........."""

    df = pd.DataFrame()

    for i in topBrand:
        query = "SELECT o.brand,p.size, sum(q.itemQuantity) as itemSold from productinfo AS o INNER JOIN productcolor AS i ON o.id=i.id INNER JOIN productsize AS p on i.colorId=p.colorId " \
                "INNER JOIN  productsize2 as q ON p.sku=q.sku where o.date=%s and i.date=%s and p.date=%s and q.date=%s and " \
                "(p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') and o.brand=%s group by p.size"
        results = sql.read_sql(query, con=conn, params=[date1, date1, date1, date1, i])
        df = df.append(results)

    df['retailer']='ellos'
    header = df.dtypes.index
    graphs.subPlots(df, header[2])

    print(df)

    """..........Size availability for each brand........"""
    df = pd.DataFrame()

    for i in topBrand:
        query = "select o.brand,p.size,count(o.id) as products from productinfo as o INNER JOIN productcolor as i on o.id=i.id INNER JOIN productsize p on p.colorId=i.colorId " \
                 "WHERE o.brand=%s and o.date=%s and i.date=%s AND p.date=%s AND (p.size='X' OR p.size='S' OR p.size='M' OR p.size='L') GROUP BY p.size"
        results = sql.read_sql(query, con=conn, params=[i, date1, date1, date1])
        df = df.append(results)

    df['retailer'] = 'ellos'
    header = df.dtypes.index
    graphs.subPlots(df,header[2])

if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='iprospect', db='scraping', charset='utf8')
    cur = conn.cursor()
    runQueryatCategoryLevel()
    runQueryatBrandLevel()
    runQueryPromotion()
    runQueryatApiLevel()

    cur.close()
    conn.close()