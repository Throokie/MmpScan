# -*- coding:utf-8 -*-
import config
from . import property_script

class Property(object):
    def __init__(self, targets_list = None):
        self.targets_list = targets_list
        print(targets_list)


    '''
    名称： start
    功能： 开启资产扫描，如果要添加新的资产扫描脚本，可以写在start里面。同时屏障数目应等于脚本数目
    '''
    def start(self):
        for url in self.targets_list:
             url = self.url_rule(url)
             print(f"property子模块正在对 '{url}' 进行资产扫描")
             property_script.OneForAll(url).OneForAll_start()
             self.save_txt(url)


    '''
    名称: save_txt
    功能：将本次扫描资产得到的域名、ip单独保存成txt文本。方便下次扫描使用
    '''
    def save_txt(self, name):
        with open(fr'{config.abs_path}\final_result\property\{name}_domain.txt', 'w') as f1:
            for domain in config.domain_set:
                f1.write(domain+'\n')

        with open(fr'{config.abs_path}\final_result\property\{name}_ip.txt', 'w') as f2:
            for domain in config.ip_set:
                f2.write(domain+'\n')


    '''
    名称：url_rule
    功能：将输入的url进行一定处理，防止用户输入'ttp://'导致保存final_result文件带有'http://'
    '''
    def url_rule(self, url):
        if 'https://' in url:
            url = url[8:]
        if 'http://' in url:
            url = url[7:]

        return url

if __name__ == '__main__':
    pass

