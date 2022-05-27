# -*- coding: utf-8 -*-
import csv
import os
import subprocess
from time import sleep,strftime,localtime,time,strptime,mktime
from loguru import logger
import Config

if not Config.python_venv_enable:
    python = Config.python_default

def http_delete(target):
    if r'http://' in target:
        target = ''.join(target.split(r'http://')[1])
    if r'https://' in target:
        target = ''.join(target.split(r'https://')[1])
    return target

def get_last_result(Script_name,target):
    file_name = []
    Script_name = Script_name
    target = target
    for i, j, k in os.walk(Config.result_scan_path):
        for name in k:
            if Script_name in name and target in name:
                file_name.append(name)
    last_date = 0
    last_date_file = ''
    for name in file_name:
        #转换为时间戳再做比较
        date = mktime(strptime(''.join(name.split('.')[-2].split('@')[-1]), '%Y-%m-%d-%H点%M分%S秒'))
        if date > last_date:
            last_date = date
            last_date_file = name
    return last_date_file

#切换工作目录到目标脚本，帮执行命令，最后切换回来
def chdir_script_path(path,command):
    # 保存当前脚本运行路径
    current_cwd = os.getcwd()
    if os.path.exists(path):
        os.chdir(path)
        try:
            # 创建venv环境
            logger.info(f"当前命令 : {command}")
            os.system(command)
        except Exception as e:
            logger.error(f"chdir_script_path 代执行命令失败，错误{e}")
    os.chdir(current_cwd)
class OneForAll():
    def __init__(self, target=''):
        # 格式： 2022-05-27-10点13分03秒
        now = strftime("%Y-%m-%d-%H点%M分%S秒", localtime(time()))
        script_name = Config.Mmpscan_scan_script_name['oneforall']
        self.target = target
        self.file_name = fr"{target}@{script_name}@{now}.csv"
        # 保存扫描结果的路径
        self.result_path = fr"{Config.result_scan_path}\{self.file_name}"
        # 上一个结果的路径
        self.last_result_path = fr'{Config.result_scan_path}\{get_last_result(script_name, target)}' if not Config.force_run_althought_exist else ''
        self.python = Config.python_venv_oneforall + Config.cmd_python_path_sufiix if Config.python_venv_enable else python

    def start(self):
        #强制调用一次。如果有该文件则不需要再次运行了
        if not Config.force_run_althought_exist:
            if self.get_result():
                return  Config.domain_set, Config.ip_set, Config.cip_set
            else:
                logger.info(f"OneForall 将重新扫描 {self.target}")
        command = f"{self.python} {Config.abs_oneforall_path}\oneforall.py --target {self.target} --path {self.result_path}   run"
        logger.info(f"OneForall 开始运行！！！\n target为：{self.target}")
        try:
            res = subprocess.Popen(command, stdout=None, stderr=None)
            output, error = res.communicate()
            logger.info("OneForall顺利结束了  ，目前保存文件中......")
        except KeyboardInterrupt(os.devnull, 'w'):
            logger.info("检测到Ctrl+c 主动退出本次扫描")
            pass
        except:
            logger.error("[-]OneForall 故障！！！")
            pass

        self.get_result()
        return Config.domain_set, Config.ip_set,Config.cip_set

    def get_result(self):  # 结果筛选另存为
        result_path = self.last_result_path if self.last_result_path else self.result_path
        try:
            self.csvFile = open(result_path, "r")
            self.reader = csv.reader(self.csvFile)
            for item in self.reader:
                if self.reader.line_num == 1:  # 忽略第一行
                    continue
                #后面用来可视化
                for ip in item[5].split(','):
                    Config.domain_set.add(ip.strip())  # 加载ip到集合
                for ip in item[8].split(','):
                    Config.ip_set.add(ip.strip())  # 加载ip到集合
                for ip in item[16].split(','):
                    Config.cip_set.add(ip.strip())  # 加载ip到集合
            return True
        except FileNotFoundError:
            if result_path:
                logger.error(f"Oneforall 找不到文件 {result_path}")
            else:
                pass
        except Exception as e:
            logger.error(f"oneforall结果另存为失败 {e}")
            sleep(3)

        return False

class SubFinder():
    def __init__(self,target=''):
        #格式： 2022-05-27-10点13分03秒
        now = strftime("%Y-%m-%d-%H点%M分%S秒", localtime(time()))
        script_name = Config.Mmpscan_scan_script_name['subfinder']
        self.target = target
        self.file_name = fr"{target}@{script_name}@{now}.txt"
        #保存扫描结果的路径
        self.result_path = fr"{Config.result_scan_path}\{self.file_name}"
        #上一个结果的路径
        self.last_result_path = fr'{Config.result_scan_path}\{get_last_result(script_name,target)}' if not Config.force_run_althought_exist else ''
    def start(self):
        if not Config.force_run_althought_exist:
            if self.get_result():
                return Config.domain_set,Config.ip_set
        logger.info(f"subfinderScan 开始 ！当前的subdomain个数为{len(Config.domain_set)}")
        scanCommand = f"{Config.abs_subfinger_path} -d {self.target} -o {self.result_path}"
        os.system(scanCommand)
        self.get_result()
        return Config.domain_set, Config.ip_set
    def get_result(self):
        #是否开启了
        result_path = self.last_result_path if self.last_result_path else self.result_path
        try:
            f = open(result_path, 'r')
            lines = f.readlines()
            for line in lines:
                Config.domain_set.add(http_delete(line.rstrip('\n')))
            f.close()
            logger.info(f"subfinderScan 结束 ！当前的subdomain个数为{len(Config.domain_set)}")
            return True
        except FileNotFoundError:
            if result_path:
                logger.error(f"subfinder 找不到文件 {result_path}")
            else:
                pass
        except Exception as e:
            logger.error(f"subfinder 错误 {e}")

        return False

class SubDomainsBrute():
    def __init__(self,target):
        # 格式： 2022-05-27-10点13分03秒
        now = strftime("%Y-%m-%d-%H点%M分%S秒", localtime(time()))
        script_name = Config.Mmpscan_scan_script_name['subDomainsBrute']
        self.target = target
        self.file_name = fr"{target}@{script_name}@{now}.txt"
        # 保存扫描结果的路径
        self.result_path = fr"{Config.result_scan_path}\{self.file_name}"
        # 上一个结果的路径
        self.last_result_path = fr'{Config.result_scan_path}\{get_last_result(script_name, target)}' if not Config.force_run_althought_exist else ''
    def start(self):
        if not Config.force_run_althought_exist:
            if self.get_result():
                return Config.domain_set, Config.ip_set
            else:
                logger.info(f"subDomainsBrute 将重新扫描 {self.target}")
        logger.info(f"subDomainsBrute 开始 ！当前的subdomain个数为{len(Config.domain_set)}")
        command = fr"{python} {Config.abs_subDomainsBrute_path}\subDomainsBrute.py -t 10 --output {self.result_path} {self.target}"
        chdir_script_path(Config.abs_subDomainsBrute_path,command)

        return Config.domain_set, Config.ip_set
    def get_result(self):
        # 是否开启了
        result_path = self.last_result_path if self.last_result_path else self.result_path
        try:
            f = open(result_path, 'r')
            lines = f.readlines()
            for line in lines:
                Config.domain_set.add(http_delete(line.split()[0].strip('\n')))
                for i in (line.split(',')):
                    if len(i) > 16:
                        Config.ip_set.add(i.split()[-1].strip('\n'))
                    else:
                        Config.ip_set.add(i.strip('\n'))
            f.close()
            logger.info(f"subDomainsBruteScan 结束 ！当前的subdomain个数为{len(Config.domain_set)}")
            return True
        except FileNotFoundError:
            if result_path:
                logger.error(f"subDomainsBruteScan 找不到文件 {result_path}")
            else:
                pass
        except Exception as e:
            logger.error(f"subDomainsBruteScan 错误 {e}")

        return False
if __name__ == '__main__':
    OneForAll(target='www.cqut.edu.cn').start()
    SubFinder('baidu.com').start()