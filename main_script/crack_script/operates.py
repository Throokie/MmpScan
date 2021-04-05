# *coding:utf-8 *
from abc import ABCMeta, abstractmethod

class crack_operates(metaclass=ABCMeta): #定义一个抽象类，这些功能都要有，每个脚本实现的方法都不同。
    @abstractmethod
    def __init__(self): #脚本初始化赋值
        pass
    def work(self): #脚本运行
        pass
    def operates(self): #筛选出需要的信息
        pass
    def save(self): #将需要的信息保存到result目录
        pass