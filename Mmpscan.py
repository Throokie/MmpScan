# -*- conding:utf-8 -*-
import os
from optparse import OptionParser
from loguru import logger
from time import sleep
import subprocess
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process,Queue
import threading

import Config
import Mmp_Script


banner ="""
@ Author : Throokie
@ Version : 0.5
@ Example : 
            python Mmpscan.py --target  target.com
            python Mmpscan.py --file    target.txt
            python Mmpscan.py --venv  True
@ 说明: 
        target   要攻击的目标
        file     保存要攻击的目标的文件
        venv  [True|Force]  是否创建虚拟目录
@ TODO   
    ①添加更多工具
    ②自动更换ip代理扫描
    ③web端（可能要很久）
 """

sleep(0.5)

def init():
    path = ''
    try:
        for path in Config.mkdir_path:
            # 路径初始化
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except Exception as e:
                    logger.info("目录初始化失败: ", e)


    except Exception as e:
        logger.warning(f"目录尚未初始化完成，错误path：{path}")
        sleep(10)


'''
名称：Before_Start
功能：启动脚本，配置任务,获取要扫描的目标
'''
class Before_Start(object):
    def __init__(self, options, args):
        self.targets_list = list()  #保存domain目标——有序版
        self.targets_set = set()  #保存domain目标——乱序版
        self.options = options
        self.args = args
        self.youxu_key = 'True'
    def start(self):
        self.venv_start()
        _list = self.get_domain()
        return _list
    #虚拟环境的使用。包括自动创建，执行pip install
    def venv_start(self):
        if (self.options.venv == 'True' and Config.python_venv_autoinstall_enable) or (self.options.venv == 'Force' and Config.python_venv_autoinstall_enable):
            logger.info('venv自动安装已开启')
            if (self.options.venv == 'Force'):
                logger.info('强制重新生成venv路径')
            logger.info(f'正在为每个venv路径进行venv初始化， 默认venv名称为：{Config.venv_name}')
            sleep(Config.logger_INFO_show_time)
            mmp_cwd = os.getcwd()
            # 保存当前脚本运行路径

            for path in Config.venv_path:
            #创建venv环境
            #TODO 兼容linux
                if not os.path.exists(path) or self.options.venv == 'Force':
                    os.chdir(path + '\\..\\')
                    cmd = fr'virtualenv  {Config.venv_name}'
                    try:
                    #创建venv环境
                        logger.info(f"当前命令 : {cmd}")
                        os.system(cmd)
                        logger.info(f"创建{path+Config.venv_name} 成功")
                    except Exception as e:
                        logger.error(f"执行创建命令错误:  {e}")


            for pip_cmd in Config.cmd_pip_venv:
            # 为venv环境执行pip install
                logger.info(pip_cmd)
                try:
                    res = subprocess.Popen(pip_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output, error = res.communicate()
                    if error:
                        logger.error(error)
                    if output:
                        logger.info(output)
                    logger.info(f"pip auto install 执行成功")
                except Exception as e:
                    logger.error(f"执行pip auto install失败: {e}")


            os.chdir(mmp_cwd)
            # 恢复原来脚本执行路径
            sleep(Config.logger_WARNNING_show_time)
    def get_domain(self):
        # 传入域名时的操作，保存域名到列表  targets_set
        if self.options.domain:
            for black in Config.black_list:
                if black in self.options.domain:
                    logger.warning(f"{self.options.domain}位于黑名单")
                    exit(0)
            self.targets_list.append(self.options.domain)
            logger.info(f"{self.options.domain}加载成功")
        # 传入文件时的操作，提取文件中的目标
        elif self.options.filename:
            try:
                fo = open(f"{self.options.filename}", "r")
                lines = fo.readlines()
                black_number = 0
                black_sign = False
                #判断是否命中黑名单
                for target in lines:
                    for black in Config.black_list:
                        if black in target:
                            black_number += 1
                            black_sign = True
                    if black_sign:
                        black_sign = False
                    else:
                        #自动去除http头
                        if r'http://' in target:
                            target = ''.join(target.split(r'http://')[1])
                        if r'https://' in target:
                            target = ''.join(target.split(r'https://')[1])
                        self.targets_list.append(target.strip())
                self.targets_set = list(self.targets_list)
                repeat_target = (len(self.targets_set) - len(self.targets_list))
                if repeat_target:
                    logger.info(f"目标target中有{repeat_target}个重复目标，有序模式为：{self.youxu_key}")
                    if self.youxu_key == 'True':
                        self.sort_targets_list = list(self.targets_set)
                        self.sort_targets_list.sort(key=self.targets_list.index)

                logger.info(f"{self.options.filename} 加载成功,共有{len(self.targets_list)}行不重复个目标,{black_number}个黑名单")

            except FileNotFoundError:
                logger.error("文件没有找到")
                exit(0)
            except Exception as e:
                logger.error(f"其他错误 : {e}")
                exit(0)

        else:
            logger.error("请传入目标参数！！!")

        return list(self.targets_list)


def Scan(target_list, target_queue, data_queue):
    data_dict = dict()
    for target in target_list:
        data_dict[target] = {
            'subdomain':set(),
            'ip':set(),
            'cip':set(),
        }
        try:
            #调用oneforall执行脚本
            sub_domain, ip, cip = Mmp_Script.OneForAll(target).start()
            data_dict[target]['subdomain'].update(sub_domain)
            data_dict[target]['ip'].update(ip)
            data_dict[target]['cip'].update(cip)
            #调用subfinder执行脚本
            sub_domain, ip = Mmp_Script.SubFinder(target).start()
            data_dict[target]['subdomain'].update(sub_domain)
            data_dict[target]['ip'].update(ip)
            #调用subDomainsBrute执行脚本
            sub_domain, ip = Mmp_Script.SubDomainsBrute(target).start()
            data_dict[target]['subdomain'].update(sub_domain)
            data_dict[target]['ip'].update(ip)

            target_queue.put(target)
            data_queue.put(data_dict)
        except Exception as e:
            target_queue.put(target)
            data_queue.put(data_dict)

            logger.info(f'Scan模块出现错误：{e}')

    #Scan发送扫描完毕信号，等到Crack取到该信号则退出
    target_queue.put('In the End')
    data_queue.put('error')


def Crack(target_queue,data_queue):
    while True:
        try:
            target = target_queue.get()
            if target == 'In the End':
                return
            data_dict = data_queue.get()
            print(len(data_dict[target]['subdomain']))
            print(len(data_dict[target]['ip']))
            print(list(data_dict[target]['ip']))
            print(list(data_dict[target]['cip']))
            # Mmp_Script.OneForAll(target)'
        except Exception as e:
            logger.info(f'Crack模块出现错误：{e}')


def main():
    print(banner)
    usage = "用法:  %prog -f <filename> | -u <domain>"
    parser = OptionParser(usage=usage)  # 若输入错误，则输出提示usage
    parser.add_option("-u", "--target", type="string", dest="domain", help="python MmpScan -u baidu.com")
    parser.add_option("-f", "--file", type="string", dest="filename", help="python MmpScan -f domains.txt")
    parser.add_option("--venv", type="string", dest="venv", help="python MmpScan --venv True")
    (options, args) = parser.parse_args()

    # 获取要扫描的目标
    targets_list = Before_Start(options, args).start()
    # 扫描目标，创建Scan、Crack模块的两个进程
    target_queue = Queue()
    data_queue = Queue()
    Scan_process = Process(target=Scan, args=(targets_list,target_queue,data_queue))
    Crack_process = Process(target=Crack, args=(target_queue,data_queue))
    Scan_process.start()
    Crack_process.start()
    Crack_process.join()
    Scan_process.join()
    logger.info(f"Congratulations !!! 扫描完成，本次扫描的目标有：{targets_list}")

if __name__ == '__main__':
    init()
    main()
