# -*- conding:utf-8 -*-
from optparse import OptionParser
import base
import os

import config

banner = """
@ Author : Ta_Tion
@ Version : 0.1
@ Example : 
            python MmpScan.py --target  target.com
            python MmpScan.py --file    target.txt
            
@ 说明: 该脚本功能还尚未完全，目前只是开发了半个框架。
        功能只有批量的oneforall资产扫描。
        后续我有空了再更新
         """
print(banner)


def init():
    print("初始化中")
    try:
        if not os.path.exists(config.save_path):
            os.makedirs(config.save_path)
            os.makedirs(config.save_property_path)
        if not os.path.exists(config.tmp_path):
            os.makedirs(config.tmp_path)
            os.makedirs(config.tmp_property_path)
            os.makedirs(config.tmp_property_oneforall_path)
        print("目录初始化完成")

    except Exception as e:
        print("初始化失败: ", e)


'''
名称：GetTarget
功能：获取待扫描的目标
'''


class GetTarget(object):
    def __init__(self, options, args):
        self.targets_set = set()
        self.options = options
        self.args = args

    def start(self):
        if self.options.domain:
            self.targets_set.add(self.options.domain)
            print(f"[+]{self.options.domain}加载成功")

        elif self.options.filename:
            try:
                fo = open(f"{self.options.filename}", "r")
                lines = fo.readlines()
                for i in lines:
                    self.targets_set.add(i.strip())

                self.targets_list = list(self.targets_set)  # 将集合化为list
                print(f"[+]{self.options.filename} 加载成功,共有{len(self.targets_list)}行不重复 target")

            except FileNotFoundError:
                exit("文件没有找到")

        else:
            print("请传入参数！！！")
        return list(self.targets_set)


def main():
    usage = "用法:  %prog -f <filename> | -u <domain>"
    parser = OptionParser(usage=usage)  # 若输入错误，则输出提示usage
    parser.add_option("-u", "--target", type="string", dest="domain", help="python MmpScan -u baidu.com")
    parser.add_option("-f", "--file", type="string", dest="filename", help="python MmpScan -f domains.txt")
    (options, args) = parser.parse_args()

    __targets_list = GetTarget(options, args).start()
    base.start(__targets_list)

if __name__ == '__main__':
    init()
    main()
