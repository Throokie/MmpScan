# *coding:UTF-8 *
import os

from fake_useragent import UserAgent

'''！！！以下配置因人而异。需要自己更改！！！'''

"""
python运行环境配置:
    python_default  物理机运行环境
            如你平时使用的： python Oneforall  则填python，  python3 Oneforall  则填python3， 
    python_venv_enable  启用venv运行环境
            如果不想用本机python环境启用。则设置为True
    python_venv_autoinstall_enable   自动帮安装venv环境
            如果本机python没有安装venv_name包，则会自动帮安装
    python_venv_pipinstall_enable    自动帮每个venv环境安装pip依赖
            原理:> (venv) pip install -r requirements.txt
"""
# 如果要使用本机python环境，则请将python_venv_enable改为 False。不然我编写的调用脚本会执行 python_venv_xxx
python_venv_enable = True
# 如果是本机python环境。 请更改成本机调用python的语句。或者本脚本venv的python路径  常用语句 py -3  |  python3  | python
python_default = 'python'
# 自动帮每个调用脚本安装venv环境，True为开启，False为关闭
python_venv_autoinstall_enable = False
# 自动帮在每个调用脚本在venv环境下安装pip依赖，True为开启，False为关闭
python_venv_pipinstall_enable = False
# 默认的venv模块名称
venv_name = 'Mmpscan_venv'
# 为每个脚本设置一个Mmpscan内部名称  !!!开发修改！！！
Mmpscan_scan_module_name = ['oneforall']
Mmpscan_crack_module_name = ['xray','dirsearch']


"""
脚本路径配置：
        oneforall 路径(文件夹)
        dirsearch 路径（文件夹）
        xray      路径（exe文件）

脚本路径, 顺序不要轻易修改
"""
#被调用脚本路径!!!开发修改！！！
abs_oneforall_path = fr"D:\长期桌面文件\MmpScan\Oneforall"
abs_dirsearch_path = fr"D:\长期桌面文件\MmpScan\dirsearch"
abs_xray_path = fr"C:\Users\花溪九尾\Xray_Rad_Fusion\xray.exe"

#venv虚拟环境路径!!!需要则修改！！！
python_venv_oneforall = fr'{abs_oneforall_path}\{venv_name}'
python_venv_dirsearch = fr'{abs_dirsearch_path}\{venv_name}'
venv_path = [python_venv_oneforall,python_venv_dirsearch]

"""
venv命令配置：
    生成venv环境
    自动调用pip install
"""
cmd_pip_venv = [path + r'\Scripts\pip.exe install -r requirements.txt' for path in venv_path]
__cmd_python_venv = [path + r'\Scripts\python.exe' for path in venv_path]
cmd_python_venv = zip(__cmd_python_venv)

'''以下配置可按照自己喜好运行。不用修改也能运行'''
"""
线程： #还没开发到
        扫描
        爆破
"""
scan_thread_count = 3
# 资产收集进程数
crack_thread_count = 3
# 资产爆破进程数


"""
保存文件路径：
        运行结果
"""
# 绝对路径
abs_path = os.path.dirname(os.path.abspath(__file__))
# 保存全部结果的路径
result_path = abs_path + '\\Result'
# 保存scan结果的路径
result_scan_path = result_path + '\\scan-info'
# 保存crack结果的路径
result_crack_path = result_path + '\\crack-info'

# 要创建的目录集合
mkdir_path = [result_path, result_scan_path, result_crack_path]


"""
黑名单：
    在黑名单列表里的url或关键字，将会不实施扫描和攻击
"""
black_list = ["spider", "org", "gov"]


"""
随机请求头生成：
        发包时采用随机请求头
"""
useragent = UserAgent()
def get_headers():
    headers = {'User-Agent': useragent.random}
    return headers


"""
配置代理: #功能未完成
        根据需要自己添加，是个列表，元素为字典
        proxies_ip =  {
                            'https' : '127.0.0.1',
                            'http'  : '127.0.0.1'
                        }
"""
proxies_ip = []
# 默认为空，即不设置代理


"""
其他配置:
        ip资产 - 集合 - 用于存放资产收集得到的ip，自动去重
        域名资产 - 集合 - 用于存放资产收集扫描得到的域名，自动去重
        logger_show_time - 单位秒（int) - 在屏幕显示信息，防止过快看不到（其实是鸡肋配置）
        domain_ip_split_sign - 字符串 - 保存成tmp文件时，分割domain和ip用的
        force_run_althought_exist - bool - 扫描过的情况下，再次运行脚本是否完全重新扫描
"""
# scan得到的ip
ip_set = set()
# scan得到的domain
domain_set = set()
# 部分关键信息停留在窗口的秒数。方便看清，如果程序能够稳定运行，则建议为0。默认为1
logger_INFO_show_time = 0
logger_WARNNING_show_time = 0
# 已经扫描过的domain,程序一开始就会保存当前目标到这里
already_scan_txt = 'already.txt'
# 若程序意外退出，从上一次already.txt最后一个domain开始扫描。（这是扫描到一半还没扫完意外退出的补救措施）。True为开启，则意外退出再次扫描从alredy最后一个取一目标
already_last_enable = False
force_run_althought_exist = False  #若对应的调用脚本之前执行过此次目标，是否强制重新执行覆盖，True为强制执行
