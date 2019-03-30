# -*- coding: UTF-8 -*-

from scapy.all import *
import matplotlib.pyplot as plt
import os

#根据数据包生成列表
def GetPackageInfo():
    packinfo={1:{},2:{},3:{},4:{},5:{},6:{},7:{}}
    for i in range(1,8):
        path="mypackages/"+str(i)+".pcapng"
        if os.path.exists(path)==False:
            print("warning:%d package(s) is/are lost!"%(8-i))
            return packinfo
        PackageInfo=rdpcap(path)
        for j in range(0,len(PackageInfo)):
            if PackageInfo[j].payload.name=='ARP' or PackageInfo[j].payload.name[-3:]=='Pv6'  :#or PackageInfo[j].payload.proto==2表示'igmp',这个没有端口
                continue
            if (PackageInfo[j].payload.src,PackageInfo[j].payload.dst) in packinfo[i].keys():
                packinfo[i][(PackageInfo[j].payload.src,PackageInfo[j].payload.dst)]+=1
            else:
                packinfo[i][(PackageInfo[j].payload.src,PackageInfo[j].payload.dst)]=1
    return packinfo 

#绘制折线图和箱线图  
def DrawPicture(datalist=[],title=''): #datalist:数据列表 title:图像标题 
    colorList = ['b','g','r','c','m','y','k']
    threadList =['day1','day2','day3','day4','day5','day6','day7']
    plt.xlabel('daytime')
    plt.ylabel('times')
    plt.title(title)
    lines = []
    titles = []
    dataList1 =datalist
    line1 = plt.plot(threadList, dataList1)
    plt.setp(line1, color=colorList[0], linewidth=2.0)
    titles.append('times')
    lines.append(line1)
    plt.legend(lines, titles)
    plt.show()
    plt.boxplot(datalist)#箱线图
    plt.show()

#程序主函数    
def main():
    a=GetPackageInfo()
    datalist=[]    
    for i in range(1,8):
        print "第%d天总数据量%d"%(i,sum(a[i].values()))
    
    #第一个模块
    for i in range(1,8):
        print('第%d天---------'%i)
        for j in a[i].keys():
            if j[0]=='192.168.9.1' and j[1]=='239.255.255.250':
                print "%-15s--->%-15s:%d次"%(j[0],j[1],a[i][j])
                datalist.append(a[i][j]*1.0/sum(a[i].values()))  
    fc=sum(k**2 for k in datalist)/(len(datalist)-1)
    data=[]
    for i in datalist:
        data.append(i)    
    data.sort
    print "最大值：%f\n最小值：%f\n平均数：%4f\n中位数：%4f\n方差：%4f"%(max(datalist),min(datalist),sum(datalist)/len(datalist),data[(len(data)+1)//2],fc)    
    DrawPicture(datalist,'192.168.9.1-->239.255.255.250 times')
    
    #第二个模块
    datalist=[]  
    for i in range(1,8):
        times2=0
        print('第%d天---------'%i)
        for j in a[i].keys():
            if j[0]=='192.168.9.1':
                times2+=a[i][j];
        print times2*1.0/sum(a[i].values())
        datalist.append(times2*1.0/sum(a[i].values()))
    DrawPicture(datalist,'from 192.168.9.1')
    
    #第三个模块
    datalist=[]  
    for i in range(1,8):
        times2=0
        print('第%d天---------'%i)
        for j in a[i].keys():
            if j[0]=='192.168.9.226':
                times2+=a[i][j];
        print times2*1.0/sum(a[i].values())
        datalist.append(times2*1.0/sum(a[i].values()))
    DrawPicture(datalist,'from 192.168.9.226')
    
    #第四个模块
    datalist=[]  
    for i in range(1,8):
        times2=0
        print('第%d天---------'%i)
        for j in a[i].keys():
            if j[1]=='192.168.9.226':
                times2+=a[i][j];
        print times2*1.0/sum(a[i].values())
        datalist.append(times2*1.0/sum(a[i].values()))
    DrawPicture(datalist,'to 192.168.9.226')
    
if __name__=="__main__":
    main()
