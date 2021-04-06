# *coding:utf-8 *
import main_script


'''
名称： PropertyProcess
功能： 启用资产扫描联动模块，通过联动其他优秀扫描脚本，再经过去重，最后获取目标更多资产信息。
'''
class PropertyProcess(object):
    def __init__(self, target_list):
        self.targets_list = target_list


    def run(self) -> None:
        main_script.Property(targets_list = self.targets_list).start()


'''
名称：CrackProcess
功能：对PropertyProcess获取到的资产信息进行漏洞扫描。目的是获取目标漏洞信息。  采用信号量
'''
class CrackProcess(object):
    def __init__(self):
        pass


    def run(self) -> None:
        main_script.Crack().start()


def start(targets_list):
    a = PropertyProcess(targets_list)
    a.run()
    a1 = CrackProcess()
    a1.run()


if __name__ == '__main__':
    start("http://baidu.com")
