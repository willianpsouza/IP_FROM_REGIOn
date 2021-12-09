#!/usr/bin/env python3

'''
    DISCLAIMER: Script para gerar lista ips a partir das atribuicoes do arin,ripe, lacnic, pode ser utilizado
    para filtrar acessos a servidores de email, web
    AUTHOR: cz63rt -> willian.souza@provengo.com.br
    DEPENDENCIES: ipcalc,requests
    STATUS: stable 2021/12/09 16:12 -3
    PERFORMANCE: 400ms AT i7-1065G7 CPU @ 1.30GHz, download at 120 secs
'''

import os
import sys

import math
import ipcalc
import requests

def DownloadFiles(download_url):
    for c in download_url:
        url = download_url[c]['url']
        dfile = download_url[c]['file']
        PARAMS = {}
        proxies = {}
        r = requests.get(url = url, params = PARAMS, proxies = proxies)
        if r.status_code == 200:
            f = open(dfile,'w')
            f.write(r.text)
            f.close()
        else:
            print("This download is not found: %s URL: %s" % (url,dfile))
    return None

def ConvertHostsInBitNet(hosts):
    return int(32-(math.log(hosts)/math.log(2)))

def ConvertBitNetInHosts(bitNet):
    return int(pow(2,(32-bitNet)))

def ConvertIPtoInteger(ip):
    ip = str(ip)
    octets = ip.split('.')
    val0 = int(octets[0]) * pow(256,3)
    val1 = int(octets[1]) * pow(256,2)
    val2 = int(octets[2]) * 256
    val3 = int(octets[3])
    intval = val0 + val1 + val2 + val3
    return intval  

def ProcessFiles(download_url):
    retdata = []
    networks = {}
    listcountries = ['RU', 'CN', 'NZ', 'RO']
    for c in download_url:
        NAME = c
        FILE = download_url[c]['file']
        f = open(FILE)
        for d in f.readlines():
            e = d.split('|')
            if len(e) > 5 and e[0] == c and e[2] == "ipv4":
                country     = e[1]
                ipaddr      = e[3]
                blocksize   = e[4]
                detail      = e[4]
                status      = e[5].replace('\n','')
                bitmask     = ConvertHostsInBitNet(int(blocksize))
                if country in listcountries:                   
                    netdescr =  ("%s/%s" % (ipaddr,bitmask))
                    n = ipcalc.Network(netdescr)
                    netdescr = ("%s/%s" % (str(n.network()),bitmask))                   
                    v = (ConvertIPtoInteger(netdescr.split('/')[0]) + int(blocksize))
                    networks[v] = netdescr

        for c in sorted(networks.keys()):
            retdata.append(networks[c])
    return retdata

def PostfixFilter(data,msg="NOT SPAM FROM you"):
    ret = ""
    for c in data:
        ret += ("%s   %s #%s \n" % (c,'   REJECT',msg))
    return ret

def CheckFileToDownload(download_url):
    for c in download_url:
        if not os.path.isfile(download_url[c]['file']):
            print('File not found: %32s trying to download: %s' % (download_url[c]['file'],download_url[c]['url']))
            DownloadFiles({c : download_url[c]})
    return True

def main():
    DESTFILE = "./FILTER_HOSTS"
    download_url = {}
    download_url['apnic'] =  {'url' : 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest','file' : 'delegated-lacnic-apnic.txt'}
    download_url['iana'] = {'url' : 'https://ftp.apnic.net/stats/iana/delegated-iana-latest', 'file' : 'delegated-iana-latest.txt'}
    download_url['ripencc'] = {'url' : 'https://ftp.apnic.net/stats/ripe-ncc/delegated-ripencc-latest', 'file' : 'delegated-ripencc-latest.txt'}
    download_url['lacnic'] = {'url' : 'https://ftp.apnic.net/stats/lacnic/delegated-lacnic-latest', 'file' : 'delegated-lacnic-latest.txt'}

    CheckFileToDownload(download_url)
    p = PostfixFilter(ProcessFiles(download_url))
    
    try:
        try:
            os.remove(DESTFILE)
        except:
            pass
        f = open(DESTFILE,'w')
        f.write(p)
        f.close()
    except:
        print("Error were trying write this file: %s" % (DESTFILE))
    exit()

main()


