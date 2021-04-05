# -*- coding:utf-8 -*-
import time
import config
from . import crack_script


class Crack(object):
    def __init__(self):
        pass


    def start(self):
        self.loophole_scan_by_domain()
        self.loophole_scan_by_ip()


    '''
    名称：loophole_scan_by_domain
    功能：从集合中取出域名，进行漏洞扫描。
    '''
    def loophole_scan_by_domain(self):
        for domain in config.domain_set:
            print(domain)
            pass
        config.domain_set.clear()


    '''
    名称：loophole_scan_by_ip
    功能：从集合中取出ip，进行漏洞扫描。
    '''
    def loophole_scan_by_ip(self):
        for ip in config.ip_set:
            print(ip)
            pass
        config.ip_set.clear()


if __name__ == '__main__':
    a = Crack()
    a.start()