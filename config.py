# *coding:UTF-8 *
import os
import queue
from fake_useragent import UserAgent

"""
线程：
        资产扫描线程
        攻击运行线程
"""
property_thread_count = 3   #被动资产扫描进程数
crack_thread_count = 3      #主动测试扫描进程数


"""
路径：
        oneforall 路径(文件夹)
        dirsearch 路径（文件夹）
        xray      路径（exe文件）
"""
abs_oneforall_path = fr"C:\Users\Kitty\Desktop\HACK\渗透测试\信息收集\OneForAll-master"
abs_dirsearch_path = fr"C:\Users\Kitty\Desktop\HACK\渗透测试\信息收集\dirsearch"
abs_xray_path = fr"C:\Users\Kitty\Desktop\HACK\渗透测试\漏洞扫描\Xray\Xray高级版\xray.exe"


"""
黑名单：
        在黑名单列表里的url或关键字，将会不实施扫描和攻击
"""
black_list=["spider","org","gov"]


"""
随机请求头生成：
        发包时采用随机请求头
"""
useragent = UserAgent()
def get_headers():
    headers = {'User-Agent': useragent.random}
    return headers


"""
配置代理:
        根据需要自己添加，是个列表，元素为字典
        proxies_ip =  {
                            'https' : '127.0.0.1',
                            'http'  : '127.0.0.1'
                        }
"""
proxies_ip = [] #默认为空，即不设置代理


"""
运行别名:
        python MmpScan.py  则填python，  python3 MmpScan.py  则填python3
"""
python = 'python' #如果是 python3 运行命令请更改


"""
其他配置:
        绝对路径
        ip资产 - 集合 - 用于存放所有扫描得到的ip，自动去重
        域名资产 - 集合 - 用于存放所有扫描得到的域名，自动去重
"""
abs_path = os.path.dirname(os.path.abspath(__file__)) #绝对路径,请勿更改
save_path = abs_path + '\\final_result'
save_property_path = save_path + '\\property'

tmp_path = abs_path + '\\tmp'
tmp_property_path = tmp_path + '\\property'
tmp_property_oneforall_path = tmp_property_path + '\\oneforall'

ip_set = set()
domain_set = set()
