import ipcalc


def xipcalc(data):
    import math
    import re
    dataret = []
    (ipaddr,netmask)=re.split(r'/',data)
    (oct1,oct2,oct3,oct4)=ipaddr.split('.')
    netsize=int(netmask)
    nmnetsize = math.pow(2,(32-netsize))
    oct1=int(oct1)
    oct2=int(oct2)
    oct3=int(oct3)
    oct4=int(oct4)
    if(netsize == 32):
        dataret.append(ipaddr)
        return dataret
    if(netsize <= 8):
        dataret.append(str(oct1) + '.255.255.255')
        return dataret

    if(netsize>24):
        for c in range(0,255,int(nmnetsize)):
            ininet = int(c)
            endnet = int((c + nmnetsize)-1)
            if(oct4>=ininet and oct4<=endnet):
                for g in range(ininet,endnet+1):
                    dataret.append(str(oct1) + '.' + str(oct2) + '.' + str(oct3) + '.' + str(g))
        return dataret

    if(netsize>=16):
        for c in range(0,255,int(nmnetsize/256)):
            ininet = int(c)
            endnet = int(int(c + int(nmnetsize/256))-1)
            if(oct3>=ininet and oct3<=endnet):
                for b in range(ininet,endnet+1):
                    for g in range(0,255+1):
                        dataret.append(str(oct1) + '.' + str(oct2) + '.' + str(b) + '.' + str(g))
        return dataret





import ipcalc
address = '31.135.244.0/21'
c = ipcalc.Network(address)
print(c.network(),)


    

