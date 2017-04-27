"""........This file contains all the graph functions of a specific type using Matplotlib library..........."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


"""..........Mutiple Bar lot.........."""

def multipleBar(df,para2,products,retailer):

    p=df.pivot(index=para2,columns=retailer,values=products)
    print(p)
    p.plot(kind='bar')
    plt.title(products +' in each '+para2 +' for each retailers')
    plt.xlabel(para2)
    plt.ylabel(products)
    locs, labels = plt.xticks()
    print(labels,locs)
    plt.setp(labels, rotation=0)
    plt.savefig('C:/Users/KAli02/Desktop/Master_Thesis/Code/FlaskApp/static/'+para2 +'_'+products+date+'.png')
    plt.show()

"""..........stacked Multiple Bar Plot.........."""

def stackedMultiBar(df,para1,productNumber,para2,retailer):

    fig, axes = plt.subplots(nrows=1, ncols=3)
    ax_position = 0

    for concept in df.groupby(para2):
        var = concept[1].groupby([para1, retailer])[productNumber].sum()
        max = var.max(axis=0)
        print(var.unstack())
        ax = var.unstack().plot(kind='bar', stacked=True, color=['blue','green','red'], ax=axes[ax_position])
        ax.set_title(concept[0], fontsize=20, alpha=1.0)
        ax.set_ylabel(productNumber)
        ax.set_ylim(0, max*2 + 20)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(labels, loc='upper right', fontsize=15)
        ax_position += 1

    axes[1].set_ylabel("")
    axes[2].set_ylabel("")
    axes[1].set_yticklabels("")
    axes[2].set_yticklabels("")
    axes[0].legend().set_visible(False)
    axes[1].legend().set_visible(False)
    axes[2].legend(labels, loc='upper right', fontsize=15)
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=0)
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=0)
    plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=0)

    plt.show()
    plt.savefig('C:/Users/KAli02/Desktop/Master_Thesis/Code/FlaskApp/static/'+para2+'_'+para1+productNumber+date+'.png')

""".............Multiple Lines plot...................."""

def lines(df,date1,para,retailer):

    p=df.pivot(index=date1,columns=retailer,values=para)
    print(p)
    p.plot()
    plt.ylim(0)
    plt.ylabel(para)
    plt.show()
    plt.savefig('C:/Users/KAli02/Desktop/Master_Thesis/Code/FlaskApp/static/'+para+date+'.png')

"""..........Mutliple lines with two y-axis..........."""

def yAxis(topBrands,quantity,pageviews):
    y1=[]
    y2=[]
    x = [0, 1, 2, 3, 4]

    for i,j in zip(quantity,pageviews):
      y1.append(i)
      y2.append(j)

    #print(x,y1,y2)
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    lns1 = ax1.plot(x, y1, 'g-',label='transaction')
    lns2 = ax2.plot(x, y2, 'b-', label='pgeViews')

    ax1.set_xlabel('Brands')

    ax1.set_ylabel('Item sold', color='g')
    ax2.set_ylabel('pageViews', color='b')
    ax2.set_xticks(range(0, 5, 1))
    ax2.set_xticklabels(labels=topBrands, rotation=0, minor=False, fontsize=28)
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)

    plt.savefig('C:/Users/KAli02/Desktop/Master_Thesis/Code/FlaskApp/static/tran-revenue-'+date + '.png')
    plt.show()

""".........Single line..............."""

def singleLine(df):
    var = df.groupby('brand').offeredPercentage.sum()
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_xlabel('brands')
    ax1.set_ylabel('Offer Percentage')
    ax1.set_title("brands wise Offered Percentage")
    var.plot(kind='line')
    plt.savefig('C:/Users/KAli02/Desktop/Master_Thesis/Code/FlaskApp/static/offerPercentage'+date + '.png')

    plt.show()

"""........Subplots........."""

def subPlots(df,product):
    fig, axes = plt.subplots(nrows=1, ncols=5)
    ax_position = 0

    for concept in df.groupby('brand'):
        var = concept[1].groupby(['size', 'retailer'])[product].sum()
        max = var.max(axis=0)
        print(var.unstack())
        ax = var.unstack().plot(kind='bar', color='red', ax=axes[ax_position])
        ax.set_title(concept[0], fontsize=10, alpha=1.0)
        ax.set_ylabel(product)
        ax.set_ylim(0, max+ 30)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(labels, loc='upper right', fontsize=10)
        ax_position += 1
    axes[1].set_ylabel("")
    axes[2].set_ylabel("")
    axes[3].set_ylabel("")
    axes[4].set_ylabel("")
    axes[1].set_yticklabels("")
    axes[2].set_yticklabels("")
    axes[3].set_yticklabels("")
    axes[4].set_yticklabels("")
    axes[0].legend().set_visible(False)
    axes[1].legend().set_visible(False)
    axes[2].legend().set_visible(False)
    axes[3].legend().set_visible(False)
    axes[4].legend(labels, loc='upper right', fontsize=10)
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=0)
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=0)
    plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=0)
    plt.setp(axes[3].xaxis.get_majorticklabels(), rotation=0)
    plt.setp(axes[4].xaxis.get_majorticklabels(), rotation=0)

    plt.savefig('C:/Users/KAli02/Desktop/Master_Thesis/Code/FlaskApp/static/'+product+date + '.png')

    plt.show()

    """........Stacked Multiple bar graph............"""

    def brandStackedMultiBar(df, para1, productNumber, para2, retailer):

        fig, axes = plt.subplots(nrows=1, ncols=5)
        ax_position = 0

        for concept in df.groupby(para2):
            print(concept[0])
            var = concept[1].groupby([para1, retailer])[productNumber].sum()
            print(var)
            print('Unstacked version')
            max = var.max(axis=0)
            print(var.unstack())
            ax = var.unstack().plot(kind='bar', stacked=True, color=['blue', 'green', 'red'], ax=axes[ax_position])
            ax.set_title(concept[0], fontsize=10, alpha=1.0)
            ax.set_ylabel(productNumber)
            ax.set_ylim(0, max * 2 + 20)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(labels, loc='upper right', fontsize=10)
            ax_position += 1

        axes[1].set_ylabel("")
        axes[2].set_ylabel("")
        axes[3].set_ylabel("")
        axes[4].set_ylabel("")
        axes[1].set_yticklabels("")
        axes[2].set_yticklabels("")
        axes[3].set_yticklabels("")
        axes[4].set_yticklabels("")
        axes[0].legend().set_visible(False)
        axes[1].legend().set_visible(False)
        axes[2].legend().set_visible(False)
        axes[3].legend().set_visible(False)
        axes[4].legend(labels, loc='upper right', fontsize=10)
        plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=0)
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=0)
        plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=0)
        plt.setp(axes[3].xaxis.get_majorticklabels(), rotation=0)
        plt.setp(axes[4].xaxis.get_majorticklabels(), rotation=0)

        plt.show()
        plt.savefig(
            'C:/Users/KAli02/Desktop/Master_Thesis/Code/FlaskApp/static/' + para2 + '_' + para1 + productNumber + date + '.png')
