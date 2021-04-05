# *coding:UTF-8 *
import os
import config

class xrayScan(object):
    def __init__(self, targeturl):
        self.url = targeturl

    def start(self):
        try:
            scanCommand="{} webscan --url \"{}\" --html-output {}\\finarl_result\\xray\\{}.html".format(config.abs_xray_path, self.url, config.abs_path, self.url)
            print(scanCommand)
            os.system(scanCommand)
        except Exception as e:
            pass

xrayScan('www.baidu.com')