#!/usr/bin/env python3

'''
    DISCLAIMER: Script para gerar lista ips a partir das atribuicoes do arin,ripe, lacnic, pode ser utilizado
    para filtrar acessos a servidores de email, web
    AUTHOR: cz63rt -> willian.souza@provengo.com.br
    DEPENDENCIES: ipcalc,requests
'''

import os
import sys

import math
import ipcalc
import requests

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

def ConvertBitNetInHosts(bitNet):
    return int(pow(2,(32-bitNet)))

def ProcessFiles(download_url):
    total_pais = {}
    retdata = []
    networks = {}
    aclass = {}
    for c in download_url:
        NAME = c
        FILE = download_url[c]['file']
        f = open(FILE)
        listcountries = ['RU', 'CN', 'NZ', 'RO']
        for d in f.readlines():
            e = d.split('|')
            if len(e) > 5 and e[0] == c and e[2] == "ipv4":
                country = e[1]
                ipaddr = e[3]
                blocksize = e[4]
                detail = e[4]
                status = e[5].replace('\n','')
                bitmask = ConvertHostsInBitNet(int(blocksize))
                if country in listcountries:                   
                    netdescr =  ("%s/%s" % (ipaddr,bitmask))
                    n = ipcalc.Network(netdescr)
                    netdescr = ("%s/%s" % (str(n.network()),bitmask))                   
                    v = (IPtoInteger(netdescr.split('/')[0]) + int(blocksize))
                    networks[v] = netdescr

        for c in sorted(networks.keys()):
            retdata.append(networks[c])
    return retdata

def findMinMax(data,minname,maxname,minval,maxval,aclass,pesq):
    for c in sorted(data.keys()):
        if aclass == data[c]['ipaddr'].split('.')[0]:
            if data[c][minname] >= minval and data[c][maxname] <= maxval:
                print(data[c])
                return c
    return None

def IPtoInteger(ip):
    ip = str(ip)
    octets = ip.split('.')
    val0 = int(octets[0]) * pow(256,3)
    val1 = int(octets[1]) * pow(256,2)
    val2 = int(octets[2]) * 256
    val3 = int(octets[3])
    intval = val0 + val1 + val2 + val3
    return intval  

def postfix(data,msg="NOT SPAM FROM you"):
    ret = ""
    for c in data:
        ret += ("%s   %s #%s \n" % (c,'   REJECT',msg))
    return ret



def main():
    download_url = {}
    download_url['apnic'] =  {'url' : 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest','file' : 'delegated-lacnic-apnic.txt'}
    download_url['iana'] = {'url' : 'https://ftp.apnic.net/stats/iana/delegated-iana-latest', 'file' : 'delegated-iana-latest.txt'}
    download_url['ripencc'] = {'url' : 'https://ftp.apnic.net/stats/ripe-ncc/delegated-ripencc-latest', 'file' : 'delegated-ripencc-latest.txt'}
    #download_url['lacnic'] = {'url' : 'https://ftp.apnic.net/stats/lacnic/delegated-lacnic-latest', 'file' : 'delegated-lacnic-latest.txt'}

    if len(sys.argv) >= 2:
        if sys.argv[1] == "all":
            DownloadFiles(download_url)
    p = ProcessFiles(download_url)
    p = postfix(p)
    destfile = "./FILTER_HOSTS"
    try:
        try:
            os.remove(destfile)
        except:
            pass
        f = open(destfile,'w')
        f.write(p)
        f.close()
    except:
        print("erro")
    return True

main()