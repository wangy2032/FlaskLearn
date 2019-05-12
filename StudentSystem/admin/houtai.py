# -*- coding: utf-8 -*-
import psutil


def cpu_shuju():
    cpu_use=psutil.cpu_percent(1)
    return cpu_use

# 内存
def Ram():
    info = {}
    #空闲内存
    free=psutil.virtual_memory().free/(1024*1024*1024)
    # 总内存
    total=psutil.virtual_memory().total/(1024*1024*1024)
    #用过的
    used = ((psutil.virtual_memory().total - psutil.virtual_memory().free))/(1024*1024*1024)
    #内存使用率
    memory=float((psutil.virtual_memory().total - psutil.virtual_memory().free))/float(psutil.virtual_memory().total)
    info.update({'mem_total':total,'mem_percent':memory, 'mem_free':free,'mem_used':used})

    return info

#硬盘
def hard_disk():
    diskinfo = psutil.disk_partitions()
    zong = [] # 4个硬盘的总量
    shiyong = [] # 4个硬盘的使用情况
    for i in diskinfo:
        info=psutil.disk_usage(i.device)
        z=int(info.total / (1024 * 1024 * 1024))
        s = int(info.used/(1024*1024*1024))
        zong.append(z)
        shiyong.append(s)
    return zong, shiyong

#网卡
def Network():
    #网卡
    net=psutil.net_io_counters()
    # 接收
    recv=net.bytes_recv/1024/1024
    # 发送
    sent=net.bytes_sent/1024/1024
    print(sent, recv)

#用户
def user():
    #用户列表
    user_list=",".join([u.name for u in psutil.users()])
    return user_list
#进程
def psid():
    quan = []
    for psid in psutil.pids():
        gebie = {}
        p = psutil.Process(psid)
        gebie['name'] = p.name()# 进程名字
        gebie['zt']=p.status() #  进程状态
        gebie['cpu'] = round(p.memory_percent(), 2)    # cup使用率
        gebie['t']= p.create_time() #  创建时间
        # print(p.create_time())
        quan.append(gebie)
    return quan

for i in range(100):
    Ram()