import datetime as dt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import time
import urllib2
from urllib2 import urlopen
from weather import Weather, Unit


style.use('ggplot')
stock = raw_input("Enter the stock ticker of the stock you would like to analyze ")
year = input("What year would you like your stock data to start from? ")
if (year < 1900):  # Error checking: cannot access date before 1900 or after 2019
    year = 1900
if(year > 2019):
    year = 2019

movingAverage = input("How many days would you like your moving average to include? ")
if(movingAverage < 1): # Error checking: moving average must be atleast 1
    movingAverage = 0

start = dt.datetime(year, 1, 1)
end = dt.datetime.now()
df = web.DataReader(stock, 'yahoo', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)


df.to_csv('stock.csv')

df = pd.read_csv('stock.csv', parse_dates=True, index_col=0)
df['ma'] = df['Adj Close'].rolling(window=movingAverage, min_periods=0).mean()

print("Which service would you like to access? Type M for Moving Average Graph, V for Volume Graph, MV for a graph of both, M2 to see a graph against an additional moving average, S for short-term analysis,")
option = raw_input("G for general short-term analysis, R for raw data of stock, SL to see where you should set your stop loss Q to quit: ")
while (option!= 'Q'):

    if(option == 'R'):
        print
        print(df.head(9999999))#Print as many as possible
        print




    if(option == 'M'):
        print
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        MAName = 'Moving Average: ' + str(movingAverage) + " days"
        ax1.plot(df.index, df['ma'], label=MAName)
        plt.ylabel("Price($)", fontsize = 20)
        plt.xlabel("Year", fontsize = 20)
        ax1.legend()
        print("Close graph to continue")
        plt.show()
        print
    if(option == 'V'):
        print
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        ax1.bar(df.index, df['Volume'], label = stock)
        plt.ylabel("Volume Sold", fontsize = 20)
        plt.xlabel("Year", fontsize = 20)
        ax1.legend()
        print("Close graph to continue")
        plt.show()
        print
    if(option == 'MV'):
        print
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
        MAName = 'Moving Average: ' + str(movingAverage) + " days"
        ax1.plot(df.index, df['ma'], label = MAName)
        ax2.bar(df.index, df['Volume'])
        ax1.legend()
        plt.ylabel("Volume     Price", fontsize = 20)
        plt.xlabel("Year", fontsize = 20)
        print("Close graph to continue")
        plt.show()
        print
    if(option == 'M2'):
        print
        secondMovingAverage = input("How many days would you like your second moving average to include? ")
        if (secondMovingAverage < 1):  # Error checking: moving average must be atleast 1
            secondMovingAverage = 0
        df['ma2'] = df['Adj Close'].rolling(window=secondMovingAverage, min_periods=0).mean()
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        MA1Name = 'Moving Average 1: ' + str(movingAverage) + " days"
        MA2Name = 'Moving Average 2: ' + str(secondMovingAverage) + " days"
        ax1.plot(df.index, df['ma'], label = MA1Name)
        ax1.plot(df.index, df['ma2'], label = MA2Name)
        ax1.legend()
        plt.ylabel("Price($)", fontsize=20)
        plt.xlabel("Year", fontsize=20)
        print("Close graph to continue")
        plt.show()
        del df['ma2']
        print
    if(option == 'S'):
        print
        print("In the short term:")
        #Count to check if any analysis outputted
        count = 0
        #Checks if 15 day moving average is above 50 day moving average, in which case, short
        df['15ma'] = df['Adj Close'].rolling(window=15, min_periods=0).mean()
        shortTermMA = df['15ma'][-1]
        del df['15ma']
        df['50ma'] = df['Adj Close'].rolling(window=50, min_periods=0).mean()
        longTermMA = df['50ma'][-1]
        del df['50ma']
        if (shortTermMA > longTermMA):
            count = 1
            print("Short the stock: 15 day moving average is above the 50 day moving average")
        #Testing if closing value has passed above 50 day moving average in last 5 days, if so: Buy. If opposite: sell
        lastClosingVal = df['Adj Close'][-1]
        MA50DayPassedClosingValBuy = False
        MA50DayPassedClosingValSell = False

        last5ClosingDays = []
        last5ClosingDays.append(df['Adj Close'][-5])
        last5ClosingDays.append(df['Adj Close'][-4])
        last5ClosingDays.append(df['Adj Close'][-3])
        last5ClosingDays.append(df['Adj Close'][-2])
        last5ClosingDays.append(df['Adj Close'][-1])
        for closingDay in last5ClosingDays:
            if(closingDay < longTermMA):
                if (longTermMA <= lastClosingVal):
                    MA50DayPassedClosingValBuy = True
        for closingDay in last5ClosingDays:
            if(closingDay > longTermMA):
                if (longTermMA >= lastClosingVal):
                    MA50DayPassedClosingValSell = True

        if(MA50DayPassedClosingValBuy is True):
            print("Buy the stock: A close above a moving average can suggest a new uptrend")
            count = 1
        if(MA50DayPassedClosingValSell is True):
            print("Sell the stock: A close below a moving average can suggest a new downtrend")
            count = 1
        #Testing if five day moving average crossed above 10 and 20 day moving averages recently
        df['5ma'] = df['Adj Close'].rolling(window=5, min_periods=0).mean()
        df['10ma'] = df['Adj Close'].rolling(window=10, min_periods=0).mean()
        df['20ma'] = df['Adj Close'].rolling(window=20, min_periods=0).mean()


        FiveDayMovingAverages =[]
        FiveDayMovingAverages.append(df['5ma'][-5])
        FiveDayMovingAverages.append(df['5ma'][-4])
        FiveDayMovingAverages.append(df['5ma'][-3])
        FiveDayMovingAverages.append(df['5ma'][-2])
        FiveDayMovingAverages.append(df['5ma'][-1])
        del df['5ma']

        TenDayMovingAverages = []
        TenDayMovingAverages.append(df['10ma'][-5])
        TenDayMovingAverages.append(df['10ma'][-4])
        TenDayMovingAverages.append(df['10ma'][-3])
        TenDayMovingAverages.append(df['10ma'][-2])
        TenDayMovingAverages.append(df['10ma'][-1])
        del df['10ma']

        TwentyDayMovingAverages = []
        TwentyDayMovingAverages.append(df['20ma'][-5])
        TwentyDayMovingAverages.append(df['20ma'][-4])
        TwentyDayMovingAverages.append(df['20ma'][-3])
        TwentyDayMovingAverages.append(df['20ma'][-2])
        TwentyDayMovingAverages.append(df['20ma'][-1])
        del df['20ma']

        FiveDayMABelowTenDay = False
        FiveDayMAAboveTenDay = False
        FiveDayMABelowTwentyDay = False
        FiveDayMAAboveTwentyDay = False

        for FiveDayMA in FiveDayMovingAverages:
            for TenDayMA in TenDayMovingAverages:
                if (FiveDayMA > TenDayMA):
                    FiveDayMAAboveTenDay = True
                if (FiveDayMA < TenDayMA):
                    FiveDayMABelowTenDay = True

        for FiveDayMA in FiveDayMovingAverages:
            for TwentyDayMA in TwentyDayMovingAverages:
                if (FiveDayMA > TwentyDayMA):
                    FiveDayMAAboveTwentyDay = True
                if (FiveDayMA < TwentyDayMA):
                    FiveDayMABelowTwentyDay = True
        if(FiveDayMABelowTenDay is True and FiveDayMAAboveTenDay is True and FiveDayMAAboveTwentyDay is True and FiveDayMABelowTwentyDay is True):
            count = 1
            print("Buy the stock: Five Day Moving Average has recently passed Ten Day and Twenty Day Moving Average")

        if(count == 0):
            print("Sorry, no short-term analysis available based upon moving averages")
        print

    if(option == 'SL'):
        #Based upon idea that it should not drop lower than 95% of long term moving average
        print
        df['100ma'] = df['Adj Close'].rolling(window=5, min_periods=0).mean()
        stopLossPrice = .95 * df['100ma'][-1]
        del df['100ma']
        print"Set the stop loss of this stock to $"+ str(int(stopLossPrice))
        print
    if(option =='L'):
        try:
            sourceCode = urllib2.urlopen('http://finance.yahoo.com/q/ks?s=' + stock).read()
            pbr = sourceCode.split('Price/Book (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
            print 'price to book ratio:', stock, pbr

        except Exception, e:
            print 'failed in the main loop', str(e)

    if(option == 'G'):
        print("Hello")
        af = web.DataReader('^VIX', 'yahoo', dt.datetime(2019,4,27), end) #VIX is market volitality index
        marketVolitality = af['High'][-1]
        print

        if(marketVolitality <= 20):
            print("Market volitality is low, investors have become complacent, might be a good time to sell")
        elif(marketVolitality < 30):
            print("Market volitality is medium, wait for lower volitality to sell, or higher volitality to buy")
        else:
            print("Market volitality is high, investors are panicked, might be a good time to buy")

        dt.datetime.today()
        day = (dt.datetime.today().weekday())
        if(day == 0):
            print("Due to the Monday effect, today might be a good day to buy stock")
        elif(day == 5):
            print("Due to the converse of the Monday effect, since it is Friday, today might be a good day to sell stock")
        elif(day > 5):
            newday1 = 7 - day
            newday2 = 11 - day
            print("Due to the Monday effect, it might be better to buy stock " + str(newday1) + " day(s) from now and sell stock " + str(newday2) + "day(s) from now")
        else:
            newday1 = 7 - day
            newday2 = 4 - day
            print("Due to the Monday effect, it might be better to buy stock " + str(newday1) + " day(s) from now and sell stock " + str(newday2) + "day(s) from now")

        print("Due to the cloudy and rainy weather in New York over the next few days, the stock market is expected to perform worse")

        print


    print("Which service would you like to access?")
    print("M for Moving Average Graph, V for Volume Graph, MV for a graph of both, M2 to see a graph against an additional moving average, S for short-term analysis, G for General short-term analysis R for raw data of stock,")
    option = raw_input ( "SL to see where you should set your stop loss, Q to quit: ")