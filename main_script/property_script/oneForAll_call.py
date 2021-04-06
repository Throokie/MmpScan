#-*- coding: utf-8 -*-
import os
import csv
import time
import config


result_path = config.abs_path + r'\tmp\property'


class OneForAll(object):
    def __init__(self, url=''):
        self.url = url
        self.run_path = config.abs_oneforall_path
        self.save_other_result_path = result_path + '\oneforall'
        self.python = config.python


    '''
    名称： __OneForAll_run
    功能： 运行扫描，一次一个url。
    '''
    def __OneForAll_run(self):
        self.command = f"{self.python} {self.run_path}\oneforall.py --target {self.url} run"
        print(f"[-]OneForall 开始运行！！！\n target为：{self.url}")
        try:
            os.system(self.command)
            print("[-]OneForall顺利结束了  ，目前保存文件中......")
        except KeyboardInterrupt:
            print("退出本次扫描")
            pass
        except:
            print("[-]OneForall 故障！！！")
            pass


    '''
    名称： __OneForAll_save
    功能： 对扫描结果进行文件处理。方便后续联动其他扫描器
    '''
    def __OneForAll_save(self): #结果筛选另存为
        time.sleep(3)
        try:
            print(f"开始将oneforal结果另存为  {self.url}.txt")
            self.url = self.url.split('.')
            self.url = '.'.join(self.url[-3:])
            self.result_file_path = fr"{self.run_path}\results\{self.url}.csv"
            self.csvFile = open(self.result_file_path, "r")
            self.reader = csv.reader(self.csvFile)
        except:
            print("打开csv文件错误")
        try:
            with open(fr'{self.save_other_result_path}\{self.url}.txt', 'w') as f:
                for item in self.reader:
                    if self.reader.line_num == 1:  # 忽略第一行
                        continue
                    f.write(item[5].strip() + "---") # 写入domain到tmp文件
                    f.write(item[8].strip() + "\n")  # 写入ip到tmp文件
                    config.domain_set.add(item[5].strip())   # 加载domain到集合
                    for ip in item[8].split(','):
                        config.ip_set.add(ip.strip())        # 加载ip到集合
            print("csv文件另存为成功!")
        except:
            print("oneforall结果另存为失败")


    '''
    名称： OneForAll_start
    功能： 启动一次完整扫描 + 扫描结果处理。是入口方法
    '''
    def OneForAll_start(self):
        self.__OneForAll_run()
        self.__OneForAll_save()

if __name__ == '__main__':
    OneForAll(url='www.cqut.edu.cn').OneForAll_start()
