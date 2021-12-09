import sys
import io
import re
import requests
import os
import math

def DownloadFiles(download_url):
    for c in download_url:
        URL = download_url[c]['url']
        FILE = download_url[c]['file']
        PARAMS = {}
        proxies = {}
        r = requests.get(url = URL, params = PARAMS, proxies = proxies)
        if r.status_code == 200:
            f = open(FILE,'w')
            f.write(r.text)
            f.close()
    return None

def ConvertHostsInBitNet(hosts):
    return int(32-(math.log(hosts)/math.log(2)))

def ProcessFiles(download_url):
    total_pais = {}
    for c in download_url:
        NAME = c
        FILE = download_url[c]['file']
        f = open(FILE)
        for d in f.readlines():
            e = d.split('|')
            if len(e) > 5 and e[0] == c and e[2] == "ipv4":
                country = e[1]
                ipaddr = e[3]
                blocksize = e[4]
                detail = e[4]
                status = e[5].replace('\n','')
                bitmask = ConvertHostsInBitNet(int(blocksize))
                if country == "BR":
                    #print("%2s %18s %2s %10s %12s" % (country,ipaddr,bitmask,status,detail))
                    print("kamctl address add 200 %s %s 5060 Brasil" % (ipaddr,bitmask))

                try:
                    total_pais[country]+=int(blocksize)
                except:
                    total_pais[country]=int(blocksize)

    #print(total_pais)

def main():
    download_url = {}
    download_url['apnic'] =  {'url' : 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest','file' : 'delegated-lacnic-apnic.txt'}
    download_url['lacnic'] = {'url' : 'https://ftp.apnic.net/stats/lacnic/delegated-lacnic-latest', 'file' : 'delegated-lacnic-latest.txt'}

    #DownloadFiles(download_url)
    ProcessFiles(download_url)
    return True

main()