# -*- coding: utf-8 -*-
import datetime
import sys
import requests
import mytoken, HeshMh

hashr=[]
hashlist = []
onlinehive=None
def hive_hashrate():
    nfarm=mytoken.nfarms
    global hashr
    url=(f'https://the.hiveos.farm/api/v2/farms/{nfarm}')
    try:

        responce=requests.get(url, headers=mytoken.headers_hive)
        json=responce.json()['hashrates_by_coin']
        coin_hashrate=[]
        #coin=[]
        hashrate=[]
        j=0
        global onlinehive
        onlinehive =responce.json()['stats']['workers_online']
        for i in json:
            hshr = json[j]['hashrate']*1000
            coin=i['coin']
            j+=1
            hashrate.append(HeshMh.hashrate_coin(hshr, coin))
        print(str(hashrate).translate({ord(i): " " for i in ']['}))
        return str(hashrate).translate({ord(i): " " for i in ']['})
    except :
        with open('log.txt', 'a') as log:
            log.write(str('Hive' +str(datetime.datetime.now())) + str(sys.exc_info()) + '\n')
def save_onlinehive():
    hive_hashrate()
    print(onlinehive)
    return onlinehive
if __name__=='__main__':
    hive_hashrate()


# автоматическое получение печенья