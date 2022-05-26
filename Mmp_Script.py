# -*- coding: utf-8 -*-
import csv
import os
import subprocess
from time import sleep
from loguru import logger
import Config


class OneForAll(object):
    def __init__(self, target=''):
        self.target = target
        # oneforall 的 csv文件路径
        self.save_path = fr"{Config.abs_oneforall_path}\results\{self.target}.csv"
        # 返回扫描数据给crack模块使用
        self.sub_domain = []
        self.ip = []
        self.python = Config.python_venv_oneforall if Config.python_venv_enable  else Config.python_default
        # 是否启用venv的python路径。还是使用默认本机物理python路径
    '''
    名称： __OneForAll_run
    功能： 运行扫描，一次一个url。
    '''

    def start(self):
        #强制调用一次。如果有该文件则不需要再次运行了
        if not Config.force_run_althought_exist:
            if self.OneForAll_save():
                return  self.sub_domain,self.ip
        command = f"{self.python} {Config.abs_oneforall_path}\oneforall.py --target {self.target}  run > nul "
        logger.info(f"OneForall 开始运行！！！\n target为：{self.target}")
        try:
            res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = res.communicate()
            logger.info("OneForall顺利结束了  ，目前保存文件中......")
        except KeyboardInterrupt(os.devnull, 'w'):
            logger.info("检测到Ctrl+c 主动退出本次扫描")
            pass
        except:
            logger.error("[-]OneForall 故障！！！")
            pass
        self.OneForAll_save()
        return self.sub_domain,self.ip

    '''
    名称： OneForAll_save
    功能： 对扫描结果进行文件处理。方便后续联动其他扫描器
    '''

    def OneForAll_save(self):  # 结果筛选另存为
        if os.path.exists(self.save_path):
            self.csvFile = open(self.save_path, "r")
            self.reader = csv.reader(self.csvFile)

            try:
                for item in self.reader:
                    if self.reader.line_num == 1:  # 忽略第一行
                        continue
                    self.sub_domain = item[5].strip()  # 保存此次得到的子域名sub.domain到data_dict
                    self.ip = item[8].strip()  # 保存此次得到的ip目标

                    #后面用来可视化
                    Config.domain_set.add(item[5].strip())  # 加载domain到集合
                    for ip in item[8].split(','):
                        Config.ip_set.add(ip.strip())  # 加载ip到集合
                logger.info("csv文件另存为成功!")
            except FileNotFoundError:
                logger.error("打开Oneforall 的 csv文件错误")
                sleep(3)
            except Exception as e:
                logger.error(f"oneforall结果另存为失败 {e}")
                sleep(3)

            return True
        return False

    '''
    名称： OneForAll_start
    功能： 启动一次完整扫描 + 扫描结果处理。是入口方法
    '''

    def OneForAll_start(self):
        self.__OneForAll_run()


if __name__ == '__main__':
    OneForAll(url='www.cqut.edu.cn').OneForAll_start()
