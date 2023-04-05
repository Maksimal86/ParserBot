
def hashrate_coin(hshr, coin):
    hrstr=[]
    hashr=[]
    #global hashr
     #hashlist
    if  hshr < 1000:
        #hr =  (round(hshr), 2)
        hrstr = (coin + " " + str(round(hshr, 2)) + 'H(Sol)')
        hashr.append(hrstr)
        #hashlist.append(hr)
    elif  hshr < 1000000:
        #hr = round(hshr / 1000, 1)
        hrstr = (coin + " " + str(round(hshr / 1000, 1)) + 'KH')
        hashr.append(hrstr)
        #hashlist.append(hr)
    elif  hshr < 1000000000:
        #hr = round(hshr / 1000000, 2)
        hrstr = (coin + " " + str(round(hshr / 1000000, 2)) + 'MH')
        hashr.append(hrstr)
        #hashlist.append(hr)
    elif  hshr < 1000000000000:
        #hr = round(hshr / 1000000000, 2)
        hrstr = (coin + " " + str(round(hshr / 1000000000, 2)) + 'GH')
        hashr.append(hrstr)
        #hashlist.append(hr)


    return hashr


